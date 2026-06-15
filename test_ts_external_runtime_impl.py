#!/usr/bin/env python3
"""Tests for cross-module export alias following in ts_external_runtime_impl."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from lsp_client import Location, file_uri, uri_to_path
from lsp_client import uri_to_path
from ts_external_runtime_impl import (
    _collect_module_bindings,
    _follow_module_export_alias,
    _line_declares_symbol,
    _line_is_export_alias,
    _location_for_export_surface_in_file,
    _location_for_symbol_in_file,
    _parse_export_alias_from_line,
    _regex_location_for_symbol,
    _resolve_export_surface_and_implementation,
    _resolve_relative_module,
    symbol_located_in_file,
)


class TestExportAliasParsing(unittest.TestCase):
    def test_member_reexport(self) -> None:
        alias = _parse_export_alias_from_line("exports.left = _.left;", "left")
        self.assertEqual(alias, ("_", "left"))

    def test_ts_emit_reexport(self) -> None:
        alias = _parse_export_alias_from_line(
            "exports.left = (0, internal_1.left);", "left"
        )
        self.assertEqual(alias, ("internal_1", "left"))

    def test_inline_function_is_not_alias(self) -> None:
        self.assertFalse(
            _line_is_export_alias(
                "exports.left = function (e) { return { _tag: 'Left', left: e }; };",
                "left",
            )
        )


class TestModuleAliasFollowing(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _write(self, rel: str, content: str) -> Path:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_follows_require_star_to_internal_module(self) -> None:
        facade = self._write(
            "Either.js",
            """\
var _ = __importStar(require("./internal"));
exports.left = _.left;
""",
        )
        self._write(
            "internal.js",
            """\
var left = function (e) { return ({ _tag: 'Left', left: e }); };
exports.left = left;
""",
        )
        surface, implementation = _resolve_export_surface_and_implementation(
            facade, "left"
        )
        self.assertEqual(uri_to_path(surface.uri).name, "Either.js")
        self.assertIsNotNone(implementation)
        assert implementation is not None
        resolved = uri_to_path(implementation.uri)
        self.assertEqual(resolved.name, "internal.js")
        text = resolved.read_text(encoding="utf-8")
        self.assertIn("function (e)", text.splitlines()[implementation.start_line])

    def test_implementation_follow_still_available_via_symbol_in_file(self) -> None:
        facade = self._write(
            "Either.js",
            "var _ = __importStar(require('./internal'));\nexports.left = _.left;\n",
        )
        self._write(
            "internal.js",
            "var left = function (e) { return e; };\nexports.left = left;\n",
        )
        loc = _location_for_symbol_in_file(facade, "left")
        self.assertEqual(uri_to_path(loc.uri).name, "internal.js")

    def test_keeps_inline_export_in_same_file(self) -> None:
        path = self._write(
            "mod.js",
            """\
exports.left = function (e) { return e; };
""",
        )
        surface, implementation = _resolve_export_surface_and_implementation(path, "left")
        self.assertEqual(uri_to_path(surface.uri), path.resolve())
        self.assertIsNone(implementation)

    def test_prefers_local_implementation_over_export_alias(self) -> None:
        path = self._write(
            "mod.js",
            """\
function left(e) { return e; }
exports.left = left;
""",
        )
        loc = _location_for_export_surface_in_file(path, "left")
        self.assertEqual(uri_to_path(loc.uri), path.resolve())
        self.assertIn("function left", path.read_text().splitlines()[loc.start_line])

    def test_regex_skips_bulk_emit_prefers_dedicated_export_line(self) -> None:
        """fp-ts-style: mid-line ``exports.none = … = void 0`` must not beat line-start definition."""
        path = self._write(
            "internal.js",
            """\
exports.flatMap = exports.none = exports.isSome = void 0;
exports.none = { _tag: 'None' };
""",
        )
        loc = _location_for_export_surface_in_file(path, "none")
        self.assertEqual(loc.start_line, 1)
        self.assertIn("_tag: 'None'", path.read_text().splitlines()[loc.start_line])
        regex_loc = _regex_location_for_symbol(path, "none")
        self.assertIsNotNone(regex_loc)
        assert regex_loc is not None
        self.assertEqual(regex_loc.start_line, 1)

    def test_chained_reexports(self) -> None:
        a = self._write(
            "a.js",
            """\
var b = require("./b");
exports.left = b.left;
""",
        )
        self._write(
            "b.js",
            """\
var core = require("./core");
exports.left = core.left;
""",
        )
        self._write(
            "core.js",
            """\
exports.left = function (x) { return x; };
""",
        )
        surface, implementation = _resolve_export_surface_and_implementation(a, "left")
        self.assertIsNotNone(implementation)
        assert implementation is not None
        self.assertEqual(uri_to_path(implementation.uri).name, "core.js")

    def test_esm_import_star_binding(self) -> None:
        self._write("internal.mjs", "export const left = (x) => x;\n")
        facade = self._write(
            "api.mjs",
            """\
import * as internal from "./internal.mjs";
export const left = internal.left;
""",
        )
        bindings = _collect_module_bindings(facade)
        self.assertIn("internal", bindings)
        self.assertEqual(bindings["internal"].name, "internal.mjs")


class TestClassMethodDetection(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _write(self, rel: str, content: str) -> Path:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_detects_transpiled_class_method(self) -> None:
        path = self._write(
            "service.js",
            """\
let Service = class Service {
    sign(payload, options) {
        return payload;
    }
};
""",
        )
        loc = _location_for_symbol_in_file(path, "sign")
        self.assertIn("sign(payload, options)", path.read_text().splitlines()[loc.start_line])
        self.assertTrue(symbol_located_in_file(path, loc, "sign"))

    def test_line_declares_symbol_for_class_method(self) -> None:
        self.assertTrue(_line_declares_symbol("    sign(payload, options) {", "sign"))
        self.assertFalse(_line_declares_symbol("    this.sign(payload)", "sign"))


class TestModuleResolution(unittest.TestCase):
    def test_resolve_relative_js(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            internal = root / "internal.js"
            internal.write_text("// x", encoding="utf-8")
            resolved = _resolve_relative_module(root, "./internal")
            self.assertEqual(resolved, internal.resolve())


if __name__ == "__main__":
    unittest.main()
