
from __future__ import annotations

import ast
import json
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# clean up expressions
def _strip_outer_parens(s: str) -> str:
    s = s.strip()
    while len(s) >= 2 and s[0] == "(" and s[-1] == ")":
        depth = 0
        ok = True
        for i, ch in enumerate(s):
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0 and i != len(s) - 1:
                    ok = False
                    break
        if ok:
            s = s[1:-1].strip()
        else:
            break
    return s


def _normalize_expr(s: str) -> str:
    s = _strip_outer_parens(s)
    return "".join(s.split())


def _safe_source_segment(src: str, node: ast.AST) -> Optional[str]:
    try:
        seg = ast.get_source_segment(src, node)
        if seg is not None:
            return seg
    except Exception:
        pass
    if hasattr(ast, "unparse"):
        try:
            return ast.unparse(node)  
        except Exception:
            return None
    return None


def _match_receiver_text(receiver_arg: Optional[str], actual_receiver_src: Optional[str]) -> bool:
    if receiver_arg is None or actual_receiver_src is None:
        return False
    return _normalize_expr(receiver_arg) == _normalize_expr(actual_receiver_src)


def _file_uri(path: Path) -> str:
    return path.resolve().as_uri()


def _uri_to_path(uri: str) -> Path:
    if not uri.startswith("file://"):
        raise ValueError(f"Unsupported URI: {uri}")
    from urllib.parse import urlparse, unquote
    parsed = urlparse(uri)
    return Path(unquote(parsed.path))


def _in_repo(repo_root: Path, p: Path) -> bool:
    try:
        p.resolve().relative_to(repo_root.resolve())
        return True
    except Exception:
        return False


def _repo_relative(repo_root: Path, p: Path) -> Optional[str]:
    try:
        return p.resolve().relative_to(repo_root.resolve()).as_posix()
    except Exception:
        return None


def _is_typeshed_path(p: Path) -> bool:
    s = str(p).replace("\\", "/")
    return "/typeshed/" in s or s.endswith("/typeshed") or "site-packages/typeshed" in s


def _is_typing_cast_call(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    f = node.func
    if isinstance(f, ast.Name) and f.id == "cast":
        return True
    if isinstance(f, ast.Attribute) and f.attr == "cast":
        if isinstance(f.value, ast.Name) and f.value.id == "typing":
            return True
    return False


def _is_super_call(node: ast.AST) -> bool:
    return isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "super"


def _unwrap_receiver_node(
    node: ast.AST,
    *,
    unwrap_cast: bool,
    unwrap_await: bool,
) -> Tuple[ast.AST, List[str]]:
    steps: List[str] = []
    cur = node

    changed = True
    while changed:
        changed = False

        if unwrap_await and isinstance(cur, ast.Await):
            steps.append("unwrap_await")
            cur = cur.value
            changed = True
            continue

        if unwrap_cast and _is_typing_cast_call(cur):
            call = cur
            if len(call.args) >= 2:
                steps.append("unwrap_cast")
                cur = call.args[1]
                changed = True
                continue

    return cur, steps


def _receiver_equivalent_match(
    receiver_arg: Optional[str],
    receiver_node: ast.AST,
    src: str,
    *,
    unwrap_cast: bool,
    unwrap_await: bool,
    allow_super: bool,
) -> Tuple[bool, Dict[str, Any]]:
    meta: Dict[str, Any] = {"receiver_expr": None, "receiver_expr_unwrapped": None, "unwrap_steps": []}

    if receiver_arg is None:
        return False, meta

    recv_src = _safe_source_segment(src, receiver_node)
    meta["receiver_expr"] = recv_src

    if _match_receiver_text(receiver_arg, recv_src):
        return True, meta

    if allow_super and receiver_arg in {"self", "cls"} and _is_super_call(receiver_node):
        meta["receiver_expr_unwrapped"] = recv_src
        meta["unwrap_steps"] = ["allow_super(self/cls_matches_super_call)"]
        return True, meta

    unwrapped, steps = _unwrap_receiver_node(receiver_node, unwrap_cast=unwrap_cast, unwrap_await=unwrap_await)
    if steps:
        meta["unwrap_steps"] = steps
        recv_src2 = _safe_source_segment(src, unwrapped)
        meta["receiver_expr_unwrapped"] = recv_src2

        if _match_receiver_text(receiver_arg, recv_src2):
            return True, meta

        if allow_super and receiver_arg in {"self", "cls"} and _is_super_call(unwrapped):
            meta["unwrap_steps"] = steps + ["allow_super(self/cls_matches_super_call_after_unwrap)"]
            return True, meta

    return False, meta


def _function_range_for_node(fn: ast.AST) -> Optional[Tuple[int, int, int, int]]:
    if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return None

    start_line0 = getattr(fn, "lineno", 1) - 1
    start_col0 = getattr(fn, "col_offset", 0)

    end_lineno = getattr(fn, "end_lineno", None)
    end_col = getattr(fn, "end_col_offset", None)

    if end_lineno is None or end_col is None:
        body = getattr(fn, "body", None) or []
        if body:
            last = body[-1]
            end_lineno = getattr(last, "end_lineno", getattr(last, "lineno", None))
            end_col = getattr(last, "end_col_offset", None)
        if end_lineno is None:
            end_lineno = getattr(fn, "lineno", 1)
        if end_col is None:
            end_col = 0

    end_line0 = int(end_lineno) - 1
    end_col0 = int(end_col)

    return (start_line0, start_col0, end_line0, end_col0)

def _pos_leq(a_line: int, a_col: int, b_line: int, b_col: int) -> bool:
    return (a_line < b_line) or (a_line == b_line and a_col <= b_col)


def _location_start_within(loc_start_line: int, loc_start_col: int, rng: Tuple[int, int, int, int]) -> bool:
    rs_l, rs_c, re_l, re_c = rng
    return _pos_leq(rs_l, rs_c, loc_start_line, loc_start_col) and _pos_leq(loc_start_line, loc_start_col, re_l, re_c)


def _filter_out_defs_inside_tested_fn(
    locs: List["Location"],
    *,
    doc_uri: str,
    tested_rng: Optional[Tuple[int, int, int, int]],
) -> List["Location"]:

    if tested_rng is None:
        return locs
    kept: List[Location] = []
    for L in locs:
        if L.uri == doc_uri and _location_start_within(L.start_line, L.start_char, tested_rng):
            continue
        kept.append(L)
    return kept

_ALIAS_ASSIGN_RE = re.compile(r"^\s*([A-Za-z_]\w*)\s*=\s*([A-Za-z_]\w*)\s*(#.*)?$")


def _detect_assignment_alias(line: str, expected_lhs: str) -> Optional[str]:
    m = _ALIAS_ASSIGN_RE.match(line)
    if not m:
        return None
    lhs, rhs = m.group(1), m.group(2)
    if lhs != expected_lhs:
        return None
    return rhs

def _encode_lsp(msg: Dict[str, Any]) -> bytes:
    body = json.dumps(msg, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    header = f"Content-Length: {len(body)}\r\n\r\n".encode("ascii")
    return header + body


def _read_lsp_message(stream) -> Dict[str, Any]:
    headers: Dict[str, str] = {}
    while True:
        line = stream.readline()
        if not line:
            raise EOFError("LSP server closed the stream.")
        line = line.decode("ascii", errors="replace").strip()
        if line == "":
            break
        if ":" in line:
            k, v = line.split(":", 1)
            headers[k.strip().lower()] = v.strip()

    if "content-length" not in headers:
        raise ValueError(f"Missing Content-Length header. Got headers={headers}")

    length = int(headers["content-length"])
    body = stream.read(length)
    if not body:
        raise EOFError("No body received from LSP server.")
    return json.loads(body.decode("utf-8"))


@dataclass(frozen=True)
class Location:
    uri: str
    start_line: int
    start_char: int
    end_line: int
    end_char: int

    def to_json(self) -> Dict[str, Any]:
        return {
            "uri": self.uri,
            "path": str(_uri_to_path(self.uri)),
            "range": {
                "start": {"line0": self.start_line, "col0": self.start_char},
                "end": {"line0": self.end_line, "col0": self.end_char},
            },
        }


def _parse_location_or_link(x: Dict[str, Any]) -> Location:
    if "targetUri" in x:
        uri = x["targetUri"]
        rng = x.get("targetSelectionRange") or x.get("targetRange")
    else:
        uri = x["uri"]
        rng = x["range"]
    return Location(
        uri=uri,
        start_line=rng["start"]["line"],
        start_char=rng["start"]["character"],
        end_line=rng["end"]["line"],
        end_char=rng["end"]["character"],
    )


def _as_locations(result: Any) -> List[Location]:
    if result is None:
        return []
    if isinstance(result, dict):
        return [_parse_location_or_link(result)]
    if isinstance(result, list):
        return [_parse_location_or_link(x) for x in result]
    return []


# ----------------------------
# Pyright LSP client
# ----------------------------

class PyrightLSP:
    def __init__(self, repo_root: Path, python_path: Optional[str] = None):
        self.repo_root = repo_root.resolve()
        self.python_path = python_path

        self.proc = subprocess.Popen(
            ["pyright-langserver", "--stdio"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        assert self.proc.stdin and self.proc.stdout
        self._id = 0
        self._initialize()

    def close(self) -> None:
        if self.proc.poll() is None:
            try:
                self._notify("exit", {})
            except Exception:
                pass
            try:
                self.proc.kill()
            except Exception:
                pass

    def _next_id(self) -> int:
        self._id += 1
        return self._id

    def _send(self, msg: Dict[str, Any]) -> None:
        assert self.proc.stdin
        self.proc.stdin.write(_encode_lsp(msg))
        self.proc.stdin.flush()

    def _request(self, method: str, params: Dict[str, Any]) -> Any:
        req_id = self._next_id()
        self._send({"jsonrpc": "2.0", "id": req_id, "method": method, "params": params})
        while True:
            msg = _read_lsp_message(self.proc.stdout)
            if "id" in msg and msg.get("id") == req_id:
                if "error" in msg:
                    raise RuntimeError(f"LSP error: {msg['error']}")
                return msg.get("result")

    def _notify(self, method: str, params: Dict[str, Any]) -> None:
        self._send({"jsonrpc": "2.0", "method": method, "params": params})

    def _initialize(self) -> None:
        init_opts: Dict[str, Any] = {}
        if self.python_path:
            init_opts["python"] = {"pythonPath": self.python_path}
            init_opts["pythonPath"] = self.python_path

        self._request(
            "initialize",
            {
                "rootUri": self.repo_root.as_uri(),
                "capabilities": {},
                "initializationOptions": init_opts,
                "workspaceFolders": [{"uri": self.repo_root.as_uri(), "name": self.repo_root.name}],
            },
        )
        self._notify("initialized", {})

    def open_document(self, file_path: Path, text: str) -> str:
        uri = _file_uri(file_path)
        self._notify(
            "textDocument/didOpen",
            {
                "textDocument": {
                    "uri": uri,
                    "languageId": "python",
                    "version": 1,
                    "text": text,
                }
            },
        )
        return uri

    def goto_definition(self, doc_uri: str, line0: int, col0: int) -> List[Location]:
        result = self._request(
            "textDocument/definition",
            {"textDocument": {"uri": doc_uri}, "position": {"line": line0, "character": col0}},
        )
        return _as_locations(result)


# ----------------------------
# AST matching
# ----------------------------

@dataclass(frozen=True)
class Match:
    kind: str
    line0: int
    col0: int
    pretty: str
    node_line0: int
    meta: Optional[Dict[str, Any]] = None
    node: Optional[ast.AST] = field(compare=False, repr=False, default=None)
    expr_src: Optional[str] = field(compare=False, repr=False, default=None)  


def _find_function_node(tree: ast.Module, name: str) -> List[ast.AST]:
    seen = set()
    out: List[ast.AST] = []
    for n in ast.walk(tree):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and getattr(n, "name", None) == name:
            key = (type(n), getattr(n, "lineno", None), getattr(n, "col_offset", None))
            if key not in seen:
                seen.add(key)
                out.append(n)
    return out


def _leaf_identifier_position(expr: ast.AST) -> Tuple[int, int]:
    if isinstance(expr, ast.Name):
        return (expr.lineno - 1, expr.col_offset)
    if isinstance(expr, ast.Attribute):
        end_col = getattr(expr, "end_col_offset", None)
        if end_col is None:
            raise ValueError("AST node missing end_col_offset. Use Python 3.8+.")
        start_col = end_col - len(expr.attr)
        return (expr.lineno - 1, start_col)
    raise ValueError(f"Unsupported leaf position expr type: {type(expr)}")


def _const_str(x: ast.AST) -> Optional[str]:
    if isinstance(x, ast.Constant) and isinstance(x.value, str):
        return x.value
    return None


def find_candidates(
    func_node: ast.AST,
    kind: str,
    receiver: Optional[str],
    name: str,
    full_source_text: str,
    *,
    allow_super: bool,
    unwrap_cast: bool,
    unwrap_await: bool,
    allow_attr_calls_without_receiver: bool = True,
) -> List[Match]:
    out: List[Match] = []

    for n in ast.walk(func_node):
        # ATTR: receiver.<name>
        if kind == "attr" and isinstance(n, ast.Attribute):
            if n.attr != name or receiver is None:
                continue

            ok, meta = _receiver_equivalent_match(
                receiver_arg=receiver,
                receiver_node=n.value,
                src=full_source_text,
                unwrap_cast=unwrap_cast,
                unwrap_await=unwrap_await,
                allow_super=allow_super,
            )
            if ok:
                line0, col0 = _leaf_identifier_position(n)
                recv_src = meta.get("receiver_expr_unwrapped") or meta.get("receiver_expr")
                out.append(
                    Match(
                        kind="attr",
                        line0=line0,
                        col0=col0,
                        pretty=f"{recv_src}.{name}" if recv_src else name,
                        node_line0=n.lineno - 1,
                        meta={**meta, "pattern": "attr_expr"},
                        node=n,
                        expr_src=_safe_source_segment(full_source_text, n),
                    )
                )

        # CALL
        elif kind == "call" and isinstance(n, ast.Call):
            callee = n.func

            # (A) bare call: name(...)
            if receiver is None and isinstance(callee, ast.Name) and callee.id == name:
                line0, col0 = _leaf_identifier_position(callee)
                out.append(
                    Match(
                        kind="call",
                        line0=line0,
                        col0=col0,
                        pretty=callee.id,
                        node_line0=callee.lineno - 1,
                        meta={"pattern": "bare_call"},
                        node=n,
                        expr_src=_safe_source_segment(full_source_text, n),
                    )
                )
                continue

            # (B) receiver.<name>(...)
            if isinstance(callee, ast.Attribute) and callee.attr == name:
                if receiver is not None:
                    ok, meta = _receiver_equivalent_match(
                        receiver_arg=receiver,
                        receiver_node=callee.value,
                        src=full_source_text,
                        unwrap_cast=unwrap_cast,
                        unwrap_await=unwrap_await,
                        allow_super=allow_super,
                    )
                    if ok:
                        line0, col0 = _leaf_identifier_position(callee)
                        recv_src = meta.get("receiver_expr_unwrapped") or meta.get("receiver_expr")
                        out.append(
                            Match(
                                kind="call",
                                line0=line0,
                                col0=col0,
                                pretty=f"{recv_src}.{name}" if recv_src else name,
                                node_line0=callee.lineno - 1,
                                meta={**meta, "pattern": "attr_call_expr"},
                                node=n,
                                expr_src=_safe_source_segment(full_source_text, n),
                            )
                        )
                else:
                    if allow_attr_calls_without_receiver:
                        line0, col0 = _leaf_identifier_position(callee)
                        recv_src = _safe_source_segment(full_source_text, callee.value)
                        out.append(
                            Match(
                                kind="call",
                                line0=line0,
                                col0=col0,
                                pretty=f"{recv_src}.{name}" if recv_src else name,
                                node_line0=callee.lineno - 1,
                                meta={"pattern": "attr_call_expr", "receiver_unconstrained": True, "receiver_expr": recv_src},
                                node=n,
                                expr_src=_safe_source_segment(full_source_text, n),
                            )
                        )
                continue

            # (C) getattr(receiver_expr, "name")(...)
            if isinstance(callee, ast.Call):
                inner = callee
                if isinstance(inner.func, ast.Name) and inner.func.id == "getattr" and len(inner.args) >= 2:
                    recv_expr = inner.args[0]
                    attr_name = _const_str(inner.args[1])
                    if attr_name == name:
                        if receiver is not None:
                            ok, meta = _receiver_equivalent_match(
                                receiver_arg=receiver,
                                receiver_node=recv_expr,
                                src=full_source_text,
                                unwrap_cast=unwrap_cast,
                                unwrap_await=unwrap_await,
                                allow_super=allow_super,
                            )
                            if not ok:
                                continue
                            recv_src = meta.get("receiver_expr_unwrapped") or meta.get("receiver_expr")
                            meta_out = {**meta, "pattern": "getattr_call"}
                        else:
                            recv_src = _safe_source_segment(full_source_text, recv_expr)
                            meta_out = {"pattern": "getattr_call", "receiver_unconstrained": True, "receiver_expr": recv_src}

                        arg = inner.args[1]  
                        out.append(
                            Match(
                                kind="call",
                                line0=arg.lineno - 1,
                                col0=arg.col_offset,
                                pretty=f"getattr({recv_src}, {name!r})(...)" if recv_src else f"getattr(<expr>, {name!r})(...)",
                                node_line0=n.lineno - 1,
                                meta=meta_out,
                                node=n,
                                expr_src=_safe_source_segment(full_source_text, n),
                            )
                        )
                continue

            if isinstance(callee, ast.Call):
                inner = callee
                if isinstance(inner.func, ast.Attribute) and inner.func.attr == "__getattribute__" and len(inner.args) >= 1:
                    recv_expr = inner.func.value
                    attr_name = _const_str(inner.args[0])
                    if attr_name == name:
                        if receiver is not None:
                            ok, meta = _receiver_equivalent_match(
                                receiver_arg=receiver,
                                receiver_node=recv_expr,
                                src=full_source_text,
                                unwrap_cast=unwrap_cast,
                                unwrap_await=unwrap_await,
                                allow_super=allow_super,
                            )
                            if not ok:
                                continue
                            recv_src = meta.get("receiver_expr_unwrapped") or meta.get("receiver_expr")
                            meta_out = {**meta, "pattern": "__getattribute___call"}
                        else:
                            recv_src = _safe_source_segment(full_source_text, recv_expr)
                            meta_out = {"pattern": "__getattribute___call", "receiver_unconstrained": True, "receiver_expr": recv_src}

                        arg = inner.args[0]
                        out.append(
                            Match(
                                kind="call",
                                line0=arg.lineno - 1,
                                col0=arg.col_offset,
                                pretty=f"{recv_src}.__getattribute__({name!r})(...)" if recv_src else f"<expr>.__getattribute__({name!r})(...)",
                                node_line0=n.lineno - 1,
                                meta=meta_out,
                                node=n,
                                expr_src=_safe_source_segment(full_source_text, n),
                            )
                        )
                continue

    return out


# ----------------------------
# anchor filtering
# ----------------------------

def _normalize_anchor_for_exact_node_match(s: str) -> str:
    s = s.strip()
    s = re.sub(r"\s+", "", s)
    s = re.sub(r",\)", ")", s)
    s = re.sub(r",\]", "]", s)
    s = re.sub(r",\}", "}", s)
    s = _strip_outer_parens(s)
    return s


def filter_by_anchor_strict(
    script_lines: List[str],
    candidates: List[Match],
    anchor: str,
    window: int,
    *,
    allow_fallback_block_contains: bool = True,
) -> List[Match]:
    anchor_n = _normalize_anchor_for_exact_node_match(anchor)

    exact: List[Match] = []
    for m in candidates:
        if not m.expr_src:
            continue
        expr_n = _normalize_anchor_for_exact_node_match(m.expr_src)
        if anchor_n == expr_n:
            exact.append(m)
    if exact:
        return exact

    contained: List[Match] = []
    for m in candidates:
        if not m.expr_src:
            continue
        expr_n = _normalize_anchor_for_exact_node_match(m.expr_src)
        if anchor_n and anchor_n in expr_n:
            contained.append(m)
    if contained:
        return contained
    
    if allow_fallback_block_contains:
        def _normalize_ws(s: str) -> str:
            return re.sub(r"\s+", "", s)

        kept: List[Match] = []
        a2 = _normalize_ws(anchor)
        for m in candidates:
            lo = max(0, m.node_line0 - window)
            hi = min(len(script_lines), m.node_line0 + window + 1)
            block = "\n".join(script_lines[lo:hi])
            if a2 in _normalize_ws(block):
                kept.append(m)
        return kept

    return []


def extract_full_def_source(def_path: Path, start_line0: int) -> Optional[str]:
    src = def_path.read_text(encoding="utf-8", errors="replace")
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return None

    lines = src.splitlines(True)
    target_lineno = start_line0 + 1

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            lineno = getattr(node, "lineno", None)
            end_lineno = getattr(node, "end_lineno", None)
            if lineno == target_lineno and end_lineno is not None:
                return "".join(lines[lineno - 1: end_lineno])
    return None


def _is_overload_decorated(func: ast.AST) -> bool:
    if not isinstance(func, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return False
    for d in func.decorator_list:
        if isinstance(d, ast.Name) and d.id == "overload":
            return True
        if isinstance(d, ast.Attribute) and d.attr == "overload":
            return True
    return False


def _strip_docstring(body: List[ast.stmt]) -> List[ast.stmt]:
    if not body:
        return body
    first = body[0]
    if isinstance(first, ast.Expr) and isinstance(getattr(first, "value", None), ast.Constant):
        if isinstance(first.value.value, str):
            return body[1:]
    return body


def _is_non_implementation_block(def_source: str) -> bool:
    try:
        mod = ast.parse(def_source)
    except SyntaxError:
        ellipsis_re = re.compile(r'^\s*def\s+\w+\s*\([^)]*\)\s*(?:->\s*[^:]+)?\s*:\s*\.\.\.')
        return bool(ellipsis_re.search(def_source))

    if not mod.body:
        return True

    top = mod.body[0]
    if isinstance(top, ast.ClassDef):
        return False
    if not isinstance(top, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return False
    if _is_overload_decorated(top):
        return True

    body = _strip_docstring(top.body)
    if not body:
        return True

    if len(body) == 1:
        st = body[0]
        if isinstance(st, ast.Pass):
            return True
        if isinstance(st, ast.Expr) and isinstance(getattr(st, "value", None), ast.Constant) and st.value.value is Ellipsis:
            return True
        if isinstance(st, ast.Raise):
            exc = st.exc
            if isinstance(exc, ast.Name) and exc.id == "NotImplementedError":
                return True
            if isinstance(exc, ast.Call) and isinstance(exc.func, ast.Name) and exc.func.id == "NotImplementedError":
                return True

    return False


@dataclass(frozen=True)
class DefCandidate:
    loc: Location
    path: Path
    full_source: Optional[str]
    is_stub: bool
    is_non_impl: bool
    is_repo_local: bool
    is_init_py: bool
    path_len: int


def _build_def_candidate(repo_root: Path, loc: Location) -> DefCandidate:
    p = _uri_to_path(loc.uri)

    is_stub = (p.suffix == ".pyi") or _is_typeshed_path(p)
    full_src: Optional[str] = None
    is_non_impl = False

    if p.exists() and p.suffix == ".py":
        full_src = extract_full_def_source(p, loc.start_line)
        if full_src is not None:
            is_non_impl = _is_non_implementation_block(full_src)

    return DefCandidate(
        loc=loc,
        path=p,
        full_source=full_src,
        is_stub=is_stub,
        is_non_impl=is_non_impl,
        is_repo_local=_in_repo(repo_root, p),
        is_init_py=(p.name == "__init__.py"),
        path_len=len(str(p)),
    )


def choose_one_definition(repo_root: Path, locs: List[Location]) -> Tuple[Optional[DefCandidate], Dict[str, Any]]:
    debug: Dict[str, Any] = {
        "policy": [
            "drop_stubs",
            "drop_non_implementations",
            "prefer_repo_local",
            "tie_break_non_init_then_shorter_path_then_position",
        ],
        "dropped": {"stubs": [], "non_implementations": []},
        "note": None,
        "ambiguity": None,
    }

    if not locs:
        debug["note"] = "no_definitions_from_pyright"
        return None, debug

    candidates = [_build_def_candidate(repo_root, loc) for loc in locs]

    non_stub = [c for c in candidates if not c.is_stub]
    debug["dropped"]["stubs"] = [c.path.as_posix() for c in candidates if c.is_stub]
    if not non_stub:
        debug["note"] = "only_stubs_found"
        return None, debug

    implemented = [c for c in non_stub if not c.is_non_impl]
    debug["dropped"]["non_implementations"] = [c.path.as_posix() for c in non_stub if c.is_non_impl]
    if not implemented:
        debug["note"] = "no_nontrivial_implementations_found"
        return None, debug

    pool = implemented
    repo_local = [c for c in pool if c.is_repo_local]
    if repo_local:
        pool = repo_local
        debug["note"] = f"preferred_repo_local_kept={len(pool)}"
    else:
        debug["note"] = f"no_repo_local_candidates_kept={len(pool)}"

    pool_sorted = sorted(
        pool,
        key=lambda c: (c.is_init_py, c.path_len, c.path.as_posix(), c.loc.start_line, c.loc.start_char),
    )
    chosen = pool_sorted[0]

    if len(pool_sorted) > 1:
        debug["ambiguity"] = {
            "remaining": len(pool_sorted),
            "chosen": chosen.path.as_posix(),
            "others": [c.path.as_posix() for c in pool_sorted[1:]],
        }
    else:
        debug["ambiguity"] = {"remaining": 1}

    return chosen, debug


# ----------------------------
# Snippet parsing
# ----------------------------

@dataclass(frozen=True)
class SnippetSelector:
    kind: str
    receiver: Optional[str]
    name: str
    anchor: str


def _snippet_to_selector(snippet: str) -> SnippetSelector:
    s = snippet.strip()
    anchor = s

    try:
        expr = ast.parse(s, mode="eval").body
    except SyntaxError:
        if "(" in s and ")" in s:
            left = s.split("(", 1)[0].strip()
            if "." in left:
                recv, nm = left.rsplit(".", 1)
                return SnippetSelector(kind="call", receiver=recv.strip(), name=nm.strip(), anchor=anchor)
            return SnippetSelector(kind="call", receiver=None, name=left.strip(), anchor=anchor)
        if "." in s:
            recv, nm = s.rsplit(".", 1)
            return SnippetSelector(kind="attr", receiver=recv.strip(), name=nm.strip(), anchor=anchor)
        return SnippetSelector(kind="call", receiver=None, name=s, anchor=anchor)

    if isinstance(expr, ast.Call):
        f = expr.func
        if isinstance(f, ast.Name):
            return SnippetSelector(kind="call", receiver=None, name=f.id, anchor=anchor)
        if isinstance(f, ast.Attribute):
            recv_src = None
            if hasattr(ast, "unparse"):
                try:
                    recv_src = ast.unparse(f.value) 
                except Exception:
                    recv_src = None
            return SnippetSelector(kind="call", receiver=recv_src, name=f.attr, anchor=anchor)
        if isinstance(f, ast.Call):
            inner = f
            if isinstance(inner.func, ast.Name) and inner.func.id == "getattr" and len(inner.args) >= 2:
                recv_expr = inner.args[0]
                nm = _const_str(inner.args[1])
                recv_src = None
                if hasattr(ast, "unparse"):
                    try:
                        recv_src = ast.unparse(recv_expr)  
                    except Exception:
                        recv_src = None
                if nm is not None:
                    return SnippetSelector(kind="call", receiver=recv_src, name=nm, anchor=anchor)
        return SnippetSelector(kind="call", receiver=None, name=s, anchor=anchor)

    if isinstance(expr, ast.Attribute):
        recv_src = None
        if hasattr(ast, "unparse"):
            try:
                recv_src = ast.unparse(expr.value)
            except Exception:
                recv_src = None
        return SnippetSelector(kind="attr", receiver=recv_src or None, name=expr.attr, anchor=anchor)

    if isinstance(expr, ast.Name):
        return SnippetSelector(kind="call", receiver=None, name=expr.id, anchor=anchor)

    return SnippetSelector(kind="call", receiver=None, name=s, anchor=anchor)


def _nested_usages_in_call_args(call_node: ast.Call, src: str, *, max_nested: int = 50) -> List[Dict[str, Any]]:
    exprs: List[ast.AST] = list(call_node.args) + [kw.value for kw in call_node.keywords if kw.value is not None]
    out: List[Dict[str, Any]] = []

    def add_call(func_expr: ast.AST, node_line0: int) -> None:
        if isinstance(func_expr, ast.Name):
            line0, col0 = _leaf_identifier_position(func_expr)
            out.append({
                "kind": "call",
                "name": func_expr.id,
                "receiver": None,
                "line0": line0,
                "col0": col0,
                "node_line0": node_line0,
                "pattern": "nested_bare_call",
            })
        elif isinstance(func_expr, ast.Attribute):
            line0, col0 = _leaf_identifier_position(func_expr)
            recv = _safe_source_segment(src, func_expr.value)
            out.append({
                "kind": "call",
                "name": func_expr.attr,
                "receiver": recv,
                "line0": line0,
                "col0": col0,
                "node_line0": node_line0,
                "pattern": "nested_attr_call",
            })

    for e in exprs:
        for n in ast.walk(e):
            if isinstance(n, ast.Call):
                add_call(n.func, n.lineno - 1)
            elif isinstance(n, ast.Attribute):
                line0, col0 = _leaf_identifier_position(n)
                recv = _safe_source_segment(src, n.value)
                out.append({
                    "kind": "attr",
                    "name": n.attr,
                    "receiver": recv,
                    "line0": line0,
                    "col0": col0,
                    "node_line0": n.lineno - 1,
                    "pattern": "nested_attr",
                })

    # de-dup by (kind,line0,col0)
    seen = set()
    uniq: List[Dict[str, Any]] = []
    for u in out:
        k = (u["kind"], u["line0"], u["col0"])
        if k not in seen:
            seen.add(k)
            uniq.append(u)

    call_pos = {(u["line0"], u["col0"]) for u in uniq if u["kind"] == "call"}
    filtered = [u for u in uniq if not (u["kind"] == "attr" and (u["line0"], u["col0"]) in call_pos)]

    return filtered[:max_nested]


# ----------------------------
# Core
# ----------------------------

def resolve_usage(
    *,
    repo_root: Path,
    script_path: Path,
    tested_function: str,
    kind: str,  # "attr" | "call"
    receiver: Optional[str],
    name: str,
    anchor: str,
    window: int = 0,
    python_path: Optional[str] = None,
    allow_super: bool = False,
    unwrap_cast: bool = False,
    unwrap_await: bool = False,
    include_full_def_source: bool = True,
    resolve_argument_usages: bool = True,
    max_argument_usages: int = 50,
) -> Dict[str, Any]:
    repo_root = repo_root.resolve()
    script_path = script_path.resolve()

    result: Dict[str, Any] = {
        "ok": False,
        "input": {
            "repo_root": str(repo_root),
            "script_path": str(script_path),
            "tested_function": tested_function,
            "usage": {"kind": kind, "receiver": receiver, "name": name},
            "selector": {"anchor": anchor, "window": window},
            "python_path": python_path,
            "flags": {"allow_super": allow_super, "unwrap_cast": unwrap_cast, "unwrap_await": unwrap_await},
        },
        "error": None,
        "matches": {"candidates": [], "anchored": [], "chosen": None},
        "definitions_all": [],
        "definitions_all_filtered": [], 
        "chosen_definition_reason": None,
        "definitions": [],
    }

    if not repo_root.exists():
        result["error"] = f"repo-root not found: {repo_root}"
        return result
    if not script_path.exists():
        result["error"] = f"script-path not found: {script_path}"
        return result

    text = script_path.read_text(encoding="utf-8", errors="replace")
    script_lines = text.splitlines()

    try:
        tree = ast.parse(text)
    except SyntaxError as e:
        result["error"] = f"Failed to parse {script_path}: {e}"
        return result

    func_nodes = _find_function_node(tree, tested_function)
    if not func_nodes:
        result["error"] = f"Function not found: {tested_function}"
        return result   

    usage_candidates: List[Match] = []
    chosen_func_node = None
    for fn in func_nodes:
        usage_candidates = find_candidates(
            func_node=fn,
            kind=kind,
            receiver=receiver or None,
            name=name,
            full_source_text=text,
            allow_super=allow_super,
            unwrap_cast=unwrap_cast,
            unwrap_await=unwrap_await,
            allow_attr_calls_without_receiver=True,
        )
        if usage_candidates:
            chosen_func_node = fn
            break

    tested_rng = _function_range_for_node(chosen_func_node) if chosen_func_node is not None else None

    result["matches"]["candidates"] = [
        {
            "kind": c.kind,
            "pretty": c.pretty,
            "expr_src": c.expr_src,
            "ref": {"path": str(script_path), "line1": c.line0 + 1, "col1": c.col0 + 1, "line0": c.line0, "col0": c.col0},
            "line_text": script_lines[c.node_line0] if 0 <= c.node_line0 < len(script_lines) else "",
            "meta": c.meta,
        }
        for c in usage_candidates
    ]

    if not usage_candidates:
        result["error"] = "No candidates found by (kind, receiver, name) under matcher."
        return result

    anchored = filter_by_anchor_strict(script_lines, usage_candidates, anchor, window)
    result["matches"]["anchored"] = [
        {
            "kind": c.kind,
            "pretty": c.pretty,
            "expr_src": c.expr_src,
            "ref": {"path": str(script_path), "line1": c.line0 + 1, "col1": c.col0 + 1, "line0": c.line0, "col0": c.col0},
            "line_text": script_lines[c.node_line0] if 0 <= c.node_line0 < len(script_lines) else "",
            "meta": c.meta,
        }
        for c in anchored
    ]

    if len(anchored) != 1:
        result["error"] = f"Anchor did not uniquely identify a single occurrence (anchored={len(anchored)})."
        if len(anchored) < 1:
            return result

    chosen_usage = anchored[0]
    result["matches"]["chosen"] = {
        "kind": chosen_usage.kind,
        "pretty": chosen_usage.pretty,
        "expr_src": chosen_usage.expr_src,
        "ref": {"path": str(script_path), "line1": chosen_usage.line0 + 1, "col1": chosen_usage.col0 + 1, "line0": chosen_usage.line0, "col0": chosen_usage.col0},
        "line_text": script_lines[chosen_usage.node_line0] if 0 <= chosen_usage.node_line0 < len(script_lines) else "",
        "meta": chosen_usage.meta,
    }

    lsp = PyrightLSP(repo_root=repo_root, python_path=python_path)
    try:
        doc_uri = lsp.open_document(script_path, text)

        def _resolve_argument_usages() -> List[Dict[str, Any]]:
            if not resolve_argument_usages:
                return []
            if not isinstance(chosen_usage.node, ast.Call):
                return []
            nested = _nested_usages_in_call_args(chosen_usage.node, text, max_nested=max_argument_usages)
            out: List[Dict[str, Any]] = []

            for u in nested:
                u_locs = lsp.goto_definition(doc_uri, u["line0"], u["col0"])

                u_locs = _filter_out_defs_inside_tested_fn(u_locs, doc_uri=doc_uri, tested_rng=tested_rng)

                chosen_u, debug_u = choose_one_definition(repo_root, u_locs)

                rec: Dict[str, Any] = {
                    "usage": u,
                    "definitions_all": [L.to_json() for L in u_locs],
                    "chosen_definition_reason": debug_u,
                    "definition": None,
                    "ok": False,
                    "error": None,
                }

                if not u_locs:
                    rec["error"] = "no_definitions_from_pyright_or_filtered_inside_tested_fn"
                elif chosen_u is None:
                    rec["error"] = "no_valid_implementation_after_filtering"
                else:
                    uloc = chosen_u.loc
                    up = chosen_u.path
                    ddef: Dict[str, Any] = {**uloc.to_json()}
                    ddef["path"] = up.as_posix()
                    ddef["directory"] = up.parent.as_posix()

                    urel = _repo_relative(repo_root, up)
                    if urel is not None:
                        ddef["repo_relative_path"] = urel
                        ddef["repo_relative_dir"] = str(Path(urel).parent)

                    ddef["full_def_source"] = (
                        (chosen_u.full_source or extract_full_def_source(up, uloc.start_line))
                        if include_full_def_source else None
                    )

                    rec["definition"] = ddef
                    rec["ok"] = True

                out.append(rec)

            return out

        locs = lsp.goto_definition(doc_uri, chosen_usage.line0, chosen_usage.col0)
        result["definitions_all"] = [loc.to_json() for loc in locs]

        locs = _filter_out_defs_inside_tested_fn(locs, doc_uri=doc_uri, tested_rng=tested_rng)
        result["definitions_all_filtered"] = [loc.to_json() for loc in locs]

        outer_item: Dict[str, Any] = {
            "outer_ok": False,
            "outer_error": None,
            "outer_definition": None,
            "argument_usages_resolved": [],
        }

        outer_item["argument_usages_resolved"] = _resolve_argument_usages()

        if not locs:
            outer_item["outer_error"] = "No definition found (pyright could not resolve it, or it resolved inside tested function)."
            result["definitions"] = [outer_item]
            result["error"] = outer_item["outer_error"]
            result["ok"] = False
            return result

        chosen_def, debug = choose_one_definition(repo_root, locs)
        result["chosen_definition_reason"] = debug

        if chosen_def is None:
            outer_item["outer_error"] = "No valid implementation found after filtering (stubs/non-implementations removed)."
            result["definitions"] = [outer_item]
            result["error"] = outer_item["outer_error"]
            result["ok"] = False
            return result

        loc = chosen_def.loc
        def_path = chosen_def.path

        outer: Dict[str, Any] = {**loc.to_json()}
        outer["path"] = def_path.as_posix()
        outer["directory"] = def_path.parent.as_posix()

        rel_path = _repo_relative(repo_root, def_path)
        if rel_path is not None:
            outer["repo_relative_path"] = rel_path
            outer["repo_relative_dir"] = str(Path(rel_path).parent)

        outer["full_def_source"] = (
            (chosen_def.full_source or extract_full_def_source(def_path, loc.start_line))
            if include_full_def_source else None
        )

        if include_full_def_source and outer.get("full_def_source") is None and def_path.exists() and def_path.suffix == ".py":
            try:
                def_text = def_path.read_text(encoding="utf-8", errors="replace")
                def_lines = def_text.splitlines()
                if 0 <= loc.start_line < len(def_lines):
                    rhs = _detect_assignment_alias(def_lines[loc.start_line], expected_lhs=name)
                    if rhs:
                        def_doc_uri = lsp.open_document(def_path, def_text)
                        col_rhs = def_lines[loc.start_line].find(rhs)
                        if col_rhs < 0:
                            col_rhs = 0

                        rhs_locs = lsp.goto_definition(def_doc_uri, loc.start_line, col_rhs)

                        outer["alias_followed"] = True
                        outer["alias_line0"] = loc.start_line
                        outer["alias_lhs"] = name
                        outer["alias_rhs"] = rhs
                        outer["alias_definitions_all"] = [L.to_json() for L in rhs_locs]

                        chosen2, debug2 = choose_one_definition(repo_root, rhs_locs)
                        outer["alias_chosen_definition_reason"] = debug2

                        if chosen2 is not None:
                            loc2 = chosen2.loc
                            p2 = chosen2.path
                            outer["alias_ultimate"] = {
                                "uri": loc2.uri,
                                "path": p2.as_posix(),
                                "range": {
                                    "start": {"line0": loc2.start_line, "col0": loc2.start_char},
                                    "end": {"line0": loc2.end_line, "col0": loc2.end_char},
                                },
                            }
                            outer["full_def_source"] = chosen2.full_source or extract_full_def_source(p2, loc2.start_line)
                        else:
                            outer["alias_ultimate"] = None
                    else:
                        outer["alias_followed"] = False
            except Exception as e:
                outer["alias_followed_error"] = f"{type(e).__name__}: {e}"

        outer_item["outer_ok"] = True
        outer_item["outer_definition"] = outer
        result["definitions"] = [outer_item]
        result["ok"] = True
        return result

    finally:
        lsp.close()


def resolve_from_snippet(
    *,
    repo_root: Path,
    script_path: Path,
    tested_function: str,
    snippet: str,
    anchor: Optional[str] = None,
    window: int = 3,
    python_path: Optional[str] = None,
    allow_super: bool = False,
    unwrap_cast: bool = False,
    unwrap_await: bool = False,
    include_full_def_source: bool = True,
    resolve_argument_usages: bool = True,
    max_argument_usages: int = 50,
) -> Dict[str, Any]:
    sel = _snippet_to_selector(snippet)
    return resolve_usage(
        repo_root=repo_root,
        script_path=script_path,
        tested_function=tested_function,
        kind=sel.kind,
        receiver=sel.receiver,
        name=sel.name,
        anchor=anchor or sel.anchor,
        window=window,
        python_path=python_path,
        allow_super=allow_super,
        unwrap_cast=unwrap_cast,
        unwrap_await=unwrap_await,
        include_full_def_source=include_full_def_source,
        resolve_argument_usages=resolve_argument_usages,
        max_argument_usages=max_argument_usages,
    )



if __name__ == "__main__":
    import argparse
    import sys

    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", required=True)
    ap.add_argument("--script-path", required=True)
    ap.add_argument("--tested-function", required=True)
    ap.add_argument("--callee", required=True)
    args = ap.parse_args()

    res = resolve_from_snippet(
        repo_root=Path(args.repo_root),
        script_path=Path(args.script_path),
        tested_function=args.tested_function,
        snippet=args.callee,
        anchor=args.callee,
        window=2,
        python_path=sys.executable,
    )

    print(json.dumps(res, indent=2, ensure_ascii=False))
