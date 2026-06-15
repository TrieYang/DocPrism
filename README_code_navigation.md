# Running the Python code navigation script

The script `code_navigation_Python.py` resolves a code snippet (e.g. a function call) inside a given function to its definition, using the Pyright language server. This is used to address DocPrism’s “lack of API knowledge” false positives.

## 1. Install Pyright (required)

The script runs `pyright-langserver` (stdio). Install it so it’s on your PATH.

**Option A – local install (no global install):**
```bash
cd /Users/trieyang/Desktop/DocPrism
npm install pyright
```
Then run the script with the local langserver on PATH:
```bash
PATH="$(pwd)/node_modules/.bin:$PATH" python code_navigation_Python.py ...
```

**Option B – global npm:**
```bash
npm install -g pyright
```
Then ensure the npm global `bin` directory is on your PATH (where `pyright-langserver` lives).

**Option C – pip (pyright as a wrapper):**
```bash
pip install pyright
```
Some setups expose the langserver as `pyright-langserver`; if not, you may need to use the full path or symlink it.

Check that the langserver is available:
```bash
pyright-langserver --version
# or
pyright --version
```

## 2. Run from the command line

Usage:
```bash
python code_navigation_Python.py \
  --repo-root   <path-to-repo-root> \
  --script-path <path-to-file-containing-the-function> \
  --tested-function <function-name> \
  --callee "<snippet-to-resolve>"
```

**Example**:

- Repo: e.g. the Requests library or any repo with a `main()` that calls `info()`.
- File: path to the module containing the function under analysis.
- Function: the name of the function (e.g. `main`).
- Callee: the exact call/snippet you want to resolve (e.g. `info()`).

```bash
cd /Users/trieyang/Desktop/DocPrism
python code_navigation_Python.py \
  --repo-root . \
  --script-path test_demo.py \
  --tested-function main \
  --callee "get_bug_info()"
```

Output is JSON: `ok: true` and a `definitions` entry with the resolved definition path and (if available) `full_def_source` means the resolution worked.

## 3. Quick sanity check (after installing Pyright)

A minimal test file is included. With `pyright-langserver` on your PATH, run:

```bash
cd /Users/trieyang/Desktop/DocPrism
python code_navigation_Python.py \
  --repo-root . \
  --script-path test_demo.py \
  --tested-function main \
  --callee "get_bug_info()"
```

You should see JSON with `"ok": true` and the definition of `get_bug_info` (file path and source). If you see `"ok": false` and an error about `pyright-langserver`, install Pyright as in step 1.

## 4. Using it from Python

```python
from pathlib import Path
from code_navigation_Python import resolve_from_snippet

result = resolve_from_snippet(
    repo_root=Path("/path/to/repo"),
    script_path=Path("/path/to/repo/module.py"),
    tested_function="main",
    snippet="info()",
    anchor="info()",
    window=2,
)

if result["ok"]:
    definition = result["definitions"][0]["outer_definition"]
    print("Resolved to:", definition["path"])
    print("Source:", definition.get("full_def_source"))
else:
    print("Error:", result["error"])
```

## 5. How you know it works

- **Command line:** Exit code 0 and JSON with `"ok": true`, and `definitions[0].outer_definition` containing:
  - `path`: path to the file where the callee is defined
  - `full_def_source`: source code of that definition (if available)
- **From Python:** `result["ok"]` is `True` and `result["definitions"]` is non-empty with the above fields.

If resolution fails, the JSON will have `"ok": false` and `"error"` (and possibly `definitions[0].outer_error`) describing why (e.g. “No definition found”, “No valid implementation after filtering”, or Pyright/LSP not available).
