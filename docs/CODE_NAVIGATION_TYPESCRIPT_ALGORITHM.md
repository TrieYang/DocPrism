# Code Navigation: TypeScript/JavaScript (FINDSOURCECODE)

This document describes only what **differs** in the TypeScript/JavaScript implementation of source-code resolution for callees. The high-level algorithm (parse snippet → find callee → get definition from LSP → select one → read source; handle nested callees similarly) is the same as the Python (Pyright) version; below is what is **specific to TypeScript**.

---

## 1. Callee and function location (no AST required)

- **Function range:** The tested function’s range is obtained from **document symbols** (`textDocument/documentSymbols`), not from an AST. The implementation walks the symbol tree to find a symbol whose name equals `tested_function` and uses its range. If that fails, the whole file is used.
- **Callee location:** The callee is located by **anchor search** in source text (substring match of the snippet), not by AST node lookup. Search order:
  1. Exact anchor in the tested-function range
  2. Exact anchor in the whole file
  3. **Core-pattern fallback:** search for the symbol name (e.g. `getHighestNode(` or `.getNodeParameter(`) in range, then in the whole file, so resolution still works when the full snippet does not match (e.g. formatting or multi-line).
- **Optional AST:** When `tree-sitter` and `tree-sitter-languages` are installed, the implementation may use a TypeScript/JavaScript AST to find the callee node first; if that yields a unique match, it is used for exact line/column. Otherwise it falls back to the anchor-based search above.

---

## 2. LSP and definition requests

- **Server:** A **TypeScript language server** (e.g. `typescript-language-server`) is used, not Pyright.
- **Document:** The file is opened with language ID `typescript` or `javascript`.
- **Request order:** The implementation requests definitions in this order:
  1. **GOTOIMPLEMENTATION** (`textDocument/implementation`)
  2. If empty, **GOTODEFINITION** (`textDocument/definition`)
  3. If empty, **GOTOTYPEDEFINITION** (`textDocument/typeDefinition`)  
  This order improves resolution for method calls and type-only references.

---

## 3. Filtering and selecting the definition

- **Filter:** Definitions whose range lies inside the tested function (same file, within the function range) are removed so the callee is not resolved to a local declaration.
- **Attribute fallback:** If no definition remains after filtering but the LSP returned at least one, and the usage is **attribute** access (e.g. `error.httpStatusCode`), the implementation may still use those definitions (including inside the tested function) so that a definition is shown when the LSP only returns in-function results.
- **Selection policy** (`_choose_one_definition`): Among remaining candidates, prefer:
  1. Non–`.d.ts` over `.d.ts`
  2. Repo-local paths over paths outside the repo
  3. Paths outside `node_modules` over inside
  4. For **call** snippets: definitions whose extracted source contains a `{` (implementation body) over declaration-only
  5. Tie-break by shorter path, then position

---

## 4. Wrong-symbol validation and implementation fallback

- **Symbol-in-source check:** The chosen definition’s extracted source must contain the resolved **symbol name** as a whole word (e.g. `\breject\b`). This rejects wrong LSP results (e.g. type alias `RejectFn` for method `reject`, or `interface Array<T>` for `getHighestNode`). If the current candidate fails, it is removed and the next candidate is chosen; this repeats until a matching definition is found or the list is exhausted.
- **Implementation-only retry:** If every candidate fails the symbol check, the implementation retries using **only** `textDocument/implementation`. If that returns locations that pass the symbol check, one of them is used. This fixes cases where definition/typeDefinition return only a type or interface and the real implementation is found only via implementation.

---

## 5. Reading definition source and callee documentation

- **READDEFINITIONSOURCE** uses the definition’s file and range to extract the full definition text. For functions/methods it uses **brace matching** from the symbol name; for classes/interfaces it extracts the full class or interface body. This is tuned for TypeScript/JavaScript syntax.
- **Preceding JSDoc:** The extracted source **includes** any comment/JSDoc block immediately above the definition (e.g. `/** ... */` or `//` lines). Those lines are collected by walking backward from the definition line and prepended to the definition snippet.
- **Callee documentation (hover):** The implementation requests **textDocument/hover** at the definition position and stores the result as `callee_documentation` on the definition object (and on each nested definition). This is the LSP’s formatted documentation (e.g. from JSDoc). If the server returns no hover or the request fails, `callee_documentation` is set to `null`.

---

## 6. Nested callees (argument usages)

- Nested attribute accesses and calls inside the snippet are found with **regex** (`_nested_usages_in_snippet`), not via AST. For each nested usage, the same pipeline (GOTODEFINITION, filter, select, read source) is applied at the corresponding character offset.
- **TypeScript-specific:** For attribute usages that resolve to a single-line property with a type annotation, the implementation may additionally resolve the **referenced type** and use that type’s source as `full_def_source`, so the structural type is shown instead of a one-line declaration.
