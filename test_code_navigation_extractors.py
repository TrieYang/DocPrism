"""Unit tests for definition/callee extraction helpers."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

from code_navigation_TypeScript import (
    Location,
    _definition_source_matches_symbol,
    _extract_commonjs_default_export_body,
    _extract_ts_enum_member_definition,
    _extract_ts_property_definition,
    _find_definition_via_imports,
    _find_commonjs_module_export_line,
    _lsp_range_is_complete_declaration,
    _resolve_node_module_entry,
    _symbol_identifier_pattern,
    _trim_trusted_lsp_snippet_to_symbol,
)
from run_n8n_code_navigation_eval import extract_all_callees


class TestSymbolPatterns(unittest.TestCase):
    def test_dollar_symbol_does_not_match_bare_name(self):
        text = "  $transaction<R>(fn: () => void): void"
        self.assertIsNotNone(re.search(_symbol_identifier_pattern("$transaction"), text))
        self.assertIsNone(re.search(_symbol_identifier_pattern("transaction"), text))

    def test_bare_transaction_not_inside_dollar(self):
        text = "await transaction(async () => {})"
        self.assertIsNotNone(re.search(_symbol_identifier_pattern("transaction"), text))

    def test_task_string_does_not_match_clean_type_pattern(self):
        src = "task('clean:output', cleanOutput);\ntask('clean:dirs', cleanDirs);"
        self.assertFalse(_definition_source_matches_symbol(src, "clean"))


class TestNodeModuleImportFollow(unittest.TestCase):
    def test_resolve_gulp_clean_entry(self):
        script = Path("nest/tools/gulp/tasks/clean.ts")
        if not script.exists():
            self.skipTest("nest clone not present")
        entry = _resolve_node_module_entry(script, "gulp-clean")
        self.assertIsNotNone(entry)
        self.assertTrue(str(entry).endswith("gulp-clean/index.js"))

    def test_find_definition_via_namespace_import(self):
        script = Path("nest/tools/gulp/tasks/clean.ts")
        if not script.exists():
            self.skipTest("nest clone not present")
        found = _find_definition_via_imports(script, "clean", Path("nest"))
        self.assertIsNotNone(found)
        path, line0 = found
        self.assertIn("gulp-clean", str(path))
        self.assertEqual(line0, _find_commonjs_module_export_line(path))

    def test_commonjs_export_body_is_complete(self):
        entry = Path("nest/node_modules/gulp-clean/index.js")
        if not entry.exists():
            self.skipTest("gulp-clean not installed")
        lines = entry.read_text(encoding="utf-8").splitlines()
        snippet, start = _extract_commonjs_default_export_body(lines, 6)
        self.assertIsNotNone(snippet)
        self.assertGreater(snippet.count("\n"), 10)
        self.assertIn("rimraf", snippet)
        self.assertTrue(snippet.rstrip().endswith("};"))


class TestEnumMemberExtraction(unittest.TestCase):
    LINES = [
        "export enum InfraConfigEnum {",
        "  ALLOW_ANALYTICS_COLLECTION = 'ALLOW_ANALYTICS_COLLECTION',",
        "  ANALYTICS_USER_ID = 'ANALYTICS_USER_ID',",
        "  IS_FIRST_TIME_INFRA_SETUP = 'IS_FIRST_TIME_INFRA_SETUP',",
        "}",
    ]

    def test_single_member(self):
        snippet, line = _extract_ts_enum_member_definition(
            self.LINES, "IS_FIRST_TIME_INFRA_SETUP", 3
        )
        self.assertEqual(
            snippet,
            "IS_FIRST_TIME_INFRA_SETUP = 'IS_FIRST_TIME_INFRA_SETUP',",
        )
        self.assertEqual(line, 3)


class TestClassFieldExtraction(unittest.TestCase):
    LINES = [
        "export class InfraTokenService {",
        "  constructor(private readonly prisma: PrismaService) {}",
        "",
        "  TITLE_LENGTH = 3;",
        "}",
    ]

    def test_field_initializer(self):
        snippet = _extract_ts_property_definition(self.LINES, "TITLE_LENGTH", 3)
        self.assertEqual(snippet, "TITLE_LENGTH = 3;")


class TestPrismaTransactionTrim(unittest.TestCase):
    PRISMA_LINES = [
        "  $queryRawUnsafe<T = unknown>(query: string, ...values: any[]): Prisma.PrismaPromise<T>;",
        "",
        "  /**",
        "   * Transaction docs",
        "   */",
        "  $transaction<P extends Prisma.PrismaPromise<any>[]>(arg: [...P]): $Utils.JsPromise<runtime.Types.Utils.UnwrapTuple<P>>",
        "",
        "  $transaction<R>(fn: (prisma: Omit<PrismaClient, runtime.ITXClientDenyList>) => $Utils.JsPromise<R>): $Utils.JsPromise<R>",
    ]

    def test_callback_overload_for_async_usage(self):
        loc = Location(
            uri="file:///fake.d.ts",
            start_line=6,
            start_char=0,
            end_line=7,
            end_char=80,
        )
        snippet, _ = _trim_trusted_lsp_snippet_to_symbol(
            self.PRISMA_LINES,
            loc,
            "$transaction",
            usage_hint="this.prisma.$transaction(async (tx) => {...})",
        )
        self.assertIn("fn:", snippet)
        self.assertNotIn("$queryRawUnsafe", snippet)
        self.assertIn("$transaction<R>", snippet)

    def test_collapsed_usage_includes_all_overloads(self):
        loc = Location(
            uri="file:///fake.d.ts",
            start_line=6,
            start_char=0,
            end_line=7,
            end_char=80,
        )
        snippet, _ = _trim_trusted_lsp_snippet_to_symbol(
            self.PRISMA_LINES,
            loc,
            "$transaction",
            usage_hint="this.prisma.$transaction(...)",
        )
        self.assertNotIn("$queryRawUnsafe", snippet)
        self.assertIn("$transaction<P extends", snippet)
        self.assertIn("$transaction<R>", snippet)


class TestLspRangeComplete(unittest.TestCase):
    def test_rejects_multi_enum_chunk(self):
        lines = [
            "  ANALYTICS_USER_ID = 'ANALYTICS_USER_ID',",
            "  IS_FIRST_TIME_INFRA_SETUP = 'IS_FIRST_TIME_INFRA_SETUP',",
        ]
        loc = Location(
            uri="file:///enum.ts",
            start_line=0,
            start_char=0,
            end_line=1,
            end_char=40,
        )
        self.assertFalse(
            _lsp_range_is_complete_declaration(lines, loc, "IS_FIRST_TIME_INFRA_SETUP")
        )

    def test_rejects_constructor_plus_field(self):
        lines = [
            "  ) {}",
            "",
            "  TITLE_LENGTH = 3;",
        ]
        loc = Location(
            uri="file:///svc.ts",
            start_line=0,
            start_char=0,
            end_line=2,
            end_char=10,
        )
        self.assertFalse(_lsp_range_is_complete_declaration(lines, loc, "TITLE_LENGTH"))


class TestCalleeExtraction(unittest.TestCase):
    CODE = """async updateMany(infraConfigs: InfraConfig[]) {
      await this.prisma.$transaction(async (tx) => {
        await tx.infraConfig.update({ where: { name: 'x' }, data: {} });
      });
    }"""

    def test_no_duplicate_transaction(self):
        callees = extract_all_callees(self.CODE, "updateMany")
        names = [c.split("(")[0] for c in callees if "(" in c]
        self.assertIn("this.prisma.$transaction", names)
        self.assertNotIn("transaction", names)

    def test_collapsed_arguments(self):
        callees = extract_all_callees(self.CODE, "updateMany")
        tx = [c for c in callees if "$transaction" in c][0]
        self.assertEqual(tx, "this.prisma.$transaction(...)")


class TestCollapseCallArguments(unittest.TestCase):
    def test_multiline_callback(self):
        from run_n8n_code_navigation_eval import _collapse_call_arguments

        full = "foo(async (x) => {\n  return x;\n})"
        self.assertEqual(_collapse_call_arguments(full), "foo(...)")


if __name__ == "__main__":
    unittest.main()
