# DocPrism

Code navigation and callee-definition resolution for DocPrism false-positive analysis. Resolves call sites in Python, TypeScript/JavaScript, and C++ to implementation source using LSP, the TypeScript compiler API, and heuristic runtime upgrades for `node_modules` `.d.ts` surfaces.

## Contents

- **Navigators:** `code_navigation_Python.py`, `code_navigation_TypeScript.py`, `code_navigation_Cpp.py`
- **LSP client:** `lsp_client.py`
- **TS compiler helper:** `ts_navigation.js`
- **External runtime upgrade:** `ts_external_runtime_impl.py` (`.d.ts` → sibling `.js` / re-export chains)
- **Eval runners:** `run_n8n_code_navigation_eval.py`, `analyze_hoppscotch_eval_results.py`
- **Docs:** `docs/`, `README_code_navigation.md`

## Setup

```bash
pip install -r requirements-code-navigation.txt
npm install   # pyright (Python) + typescript-language-server (TS)
```

Evaluation repos (`hoppscotch/`, `n8n/`) are not included — clone them locally next to this project when running evals.

## Quick start (TypeScript)

```bash
python code_navigation_TypeScript.py \
  --repo-root /path/to/hoppscotch \
  --script-path packages/foo/src/bar.ts \
  --tested-function myFn \
  --snippet "this.service.call(...)"
```

See `README_code_navigation.md` for Python usage and CLI details.
