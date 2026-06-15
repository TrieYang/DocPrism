# Multi-Language Code Navigation for DocPrism

DocPrism’s “lack of API knowledge” fix (resolving a code snippet to its definition) is implemented for **Python** in `code_navigation_Python.py`. This doc explains how to support **other languages** (TypeScript, Java, C++, etc.) without duplicating everything.

## Is there one library that does all languages?

**No.** You do need **some** per-language code, but you can share a lot:

- **Shared:** LSP protocol (JSON-RPC, `initialize` / `textDocument/didOpen` / `textDocument/definition`), result shape, and a generic LSP client that talks to any LSP server.
- **Per-language:** (1) which LSP server to run, (2) how to find the **position** of the snippet inside the function (parsing/AST or heuristics), (3) optional definition filtering (e.g. prefer implementation over `.d.ts`).

So the plan is: **one generic LSP client + one small “navigator” per language** that finds the position and configures the server.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  DocPrism (or caller)                                             │
│  Input: repo_root, file, function_name, snippet (e.g. "info()")  │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  Language-specific navigator (e.g. code_navigation_TypeScript)   │
│  1. Find (line, col) of snippet in function  ← language-specific  │
│  2. Start LSP server for that language                            │
│  3. Call generic_lsp_client.goto_definition(uri, line, col)      │
│  4. Optionally filter definition (e.g. prefer .ts over .d.ts)    │
│  5. Return same JSON shape as Python                             │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  Generic LSP client (lsp_client.py)                              │
│  - Spawn server (command from navigator)                         │
│  - initialize(root_uri, init_options)                            │
│  - textDocument/didOpen(uri, text, languageId)                   │
│  - textDocument/definition(uri, line, character)                 │
│  - Parse result → List[Location]                                │
└─────────────────────────────────────────────────────────────────┘
```

Each language has an LSP server that already implements “go to definition”; the navigator’s job is to **find the position** and **call** that server via the shared client.

---

## What each language module must implement

| Responsibility | Python (current) | TypeScript example | Java / C++ |
|----------------|-------------------|--------------------|------------|
| **Find snippet position** | AST: find call/attr, match anchor | AST (e.g. tree-sitter) or regex search for identifier in function range | Same idea: AST or search |
| **LSP server command** | `pyright-langserver --stdio` | `typescript-language-server --stdio` (or node tsserver) | `jdtls` / `clangd` etc. |
| **Language ID** | `python` | `typescript` / `javascript` | `java` / `cpp` |
| **Init options** | `pythonPath` | (optional) `preferences` | (optional) |
| **Filter definition** | Prefer repo, drop stubs, drop overloads | Prefer `.ts` over `.d.ts` | Prefer repo, drop generated |

The **output format** should be the same for all languages so DocPrism can consume it uniformly: e.g. `ok`, `error`, `definitions[].outer_definition` with `path`, `range`, `full_def_source`.

---

## LSP servers by language (reference)

| Language   | Typical LSP server              | Install / command |
|-----------|----------------------------------|-------------------|
| Python    | Pyright                          | `npm install pyright` → `pyright-langserver --stdio` |
| TypeScript| TypeScript language server      | `npm install typescript-language-server typescript` → `typescript-language-server --stdio` |
| JavaScript| Same as TypeScript              | Same server, `languageId`: `javascript` |
| Java      | Eclipse JDT LS (jdtls)           | Download / run `jdtls` with workspace |
| C++       | clangd / ccls                   | `clangd` or `ccls` on PATH |
| Go        | gopls                            | `go install golang.org/x/tools/gopls@latest` |
| Rust      | rust-analyzer                    | `rustup component add rust-analyzer` |

All of these support `textDocument/definition`. You only need to (1) run the right server, (2) open the file with the right `languageId`, (3) call definition at the position you found.

---

## Implementing a new language (checklist)

1. **Add a new file**  
   e.g. `code_navigation_TypeScript.py` (or `.ts`/Node if you prefer).

2. **Implement “find position of snippet in function”.**  
   Options:
   - **AST:** Use a parser for that language (e.g. `tree-sitter` with `tree-sitter-typescript`, or a TypeScript API) to find the call/identifier in the function body and get (line, col).
   - **Heuristic:** Get the function’s line range (e.g. from a simple regex or from LSP “symbols”), then search for the snippet text or identifier in that range and take the first or best match. Less accurate but no extra deps.

3. **Use the generic LSP client**  
   - Build the server command and init options for that language.
   - Open the document with the correct `languageId`.
   - Call `goto_definition(uri, line0, col0)` with the position from step 2.
   - Map the LSP response to your common `Location` / `outer_definition` format.

4. **Optional: filter definitions**  
   e.g. prefer implementation file over declaration (`.ts` over `.d.ts`), prefer repo-local over `node_modules`, etc.

5. **Expose the same API as Python**  
   e.g. `resolve_from_snippet(repo_root, script_path, tested_function, snippet, ...)` returning the same JSON shape so DocPrism can call any language the same way.

---

## What’s in this repo

- **`lsp_client.py`** – Generic LSP client (any language). Use this in every language module.
- **`code_navigation_Python.py`** – Full Python implementation (AST + Pyright).
- **`code_navigation_TypeScript.py`** – TypeScript/JS implementation (heuristic position + TypeScript LSP).  
  Install: `npm install typescript-language-server typescript`.  
  Run: `python code_navigation_TypeScript.py --repo-root . --script-path test_demo.ts --tested-function main --callee "getBugInfo()"`

- **`code_navigation_Cpp.py`** – C++/C implementation (heuristic position + clangd).  
  Install: clangd (e.g. `brew install llvm` or `apt install clangd`).  
  Run: `python code_navigation_Cpp.py --repo-root . --script-path test_demo.cpp --tested-function main --callee "get_value()"`

---

## Summary

- There is **no single multi-language library** that gives “go to definition for any language” in one drop-in; **finding the position of the snippet** is language-specific (parsing or heuristics).
- You **do** implement something per language, but you **share**:
  - A **generic LSP client** (protocol, `definition` request, result parsing).
  - A **common result format** and API for DocPrism.
- Per-language work is: **snippet position finding** + **LSP server config** + optional **definition filtering**. The rest is reuse.
