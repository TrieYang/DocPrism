# Go to Source Definition — sample cases

Three call-site examples from the full Hoppscotch eval (`hoppscotch_eval_results_full_source_def.json`).
Run from the DocPrism repo root.

**Prerequisites:** `hoppscotch` clone at `./hoppscotch`, `typescript-language-server` on PATH, Node deps installed.

---

## 1. Improved: `bcrypt.genSalt` (declaration → implementation)

**Sample 22, idx 0** — Go to Source Definition jumps from `@types/bcrypt/index.d.ts` to `bcrypt/bcrypt.js` with a real function body.

| | Before (no source-def path) | After |
|---|---|---|
| File | `@types/bcrypt/index.d.ts` | `bcrypt/bcrypt.js` |
| Snippet | `export declare function genSalt(...)` | `function genSalt(rounds, minor, cb) { ... }` |

**Script:** `hoppscotch/packages/hoppscotch-backend/src/auth/auth.service.ts`  
**Tested function:** `generateMagicLinkTokens`

**Terminal commands (same callee, toggle with `--no-go-to-source-definition`):**

WITHOUT Go to Source Definition (legacy — expect `@types/bcrypt`):

```bash
cd /Users/trieyang/Desktop/DocPrism

python3 code_navigation_TypeScript.py \
  --repo-root "$(pwd)/hoppscotch" \
  --script-path "$(pwd)/hoppscotch/packages/hoppscotch-backend/src/auth/auth.service.ts" \
  --tested-function generateMagicLinkTokens \
  --no-go-to-source-definition \
  --callee 'bcrypt.genSalt(
      parseInt(this.configService.get('\''TOKEN_SALT_COMPLEXITY'\'')),
    )'
```

WITH Go to Source Definition (default — expect `bcrypt/bcrypt.js`):

```bash
cd /Users/trieyang/Desktop/DocPrism

python3 code_navigation_TypeScript.py \
  --repo-root "$(pwd)/hoppscotch" \
  --script-path "$(pwd)/hoppscotch/packages/hoppscotch-backend/src/auth/auth.service.ts" \
  --tested-function generateMagicLinkTokens \
  --callee 'bcrypt.genSalt(
      parseInt(this.configService.get('\''TOKEN_SALT_COMPLEXITY'\'')),
    )'
```

**What to look for in JSON output:**
- `chosen_definition_reason.note` contains `go_to_source_definition`
- `outer_definition.repo_relative_path` ends with `bcrypt/bcrypt.js`
- `full_def_source` contains `function genSalt`

---

## 2. Still declaration: `personalAccessToken.create` (Prisma `.d.ts`)

**Sample 2, idx 3** — Go to Source Definition returns no locations; stays on `.prisma/client/index.d.ts`.

| | Result |
|---|---|
| File | `.prisma/client/index.d.ts` |
| Snippet | Typed `create(...)` JSDoc / signature |
| `source_definition_locations` | `[]` (empty) |

**Script:** `hoppscotch/packages/hoppscotch-backend/src/access-token/access-token.service.ts`  
**Tested function:** `createPAT`

**Terminal command:**

```bash
cd /Users/trieyang/Desktop/DocPrism

python3 code_navigation_TypeScript.py \
  --repo-root "$(pwd)/hoppscotch" \
  --script-path "$(pwd)/hoppscotch/packages/hoppscotch-backend/src/access-token/access-token.service.ts" \
  --tested-function createPAT \
  --callee 'this.prisma.personalAccessToken.create({
      data: {
        userUid: user.uid,
        label: createAccessTokenDto.label,
        expiresOn: calculateExpirationDate(createAccessTokenDto.expiryInDays),
      },
    })'
```

**What to look for:**
- `repo_relative_path` contains `.prisma/client/index.d.ts`
- `chosen_definition_reason.note` is `fast_path_runtime_unresolved_fell_back_to_declaration` (or similar)
- No `go_to_source_definition: true`

---

## 3. Weak source-def: `DateTime.now()` (`.d.ts` → `luxon.js`, but wrong line)

**Sample 22, idx 2** — Go to Source Definition runs and leaves `.d.ts`, but the snippet is a weak internal helper, not `DateTime.now` itself.

| | Before | After |
|---|---|---|
| File | `datetime.d.ts` | `luxon/build/node/luxon.js` |
| Snippet | `static now(): DateTime` | `let now = () => Date.now(),` |

**Script:** `hoppscotch/packages/hoppscotch-backend/src/auth/auth.service.ts`  
**Tested function:** `generateMagicLinkTokens`

**Terminal command:**

```bash
cd /Users/trieyang/Desktop/DocPrism

python3 code_navigation_TypeScript.py \
  --repo-root "$(pwd)/hoppscotch" \
  --script-path "$(pwd)/hoppscotch/packages/hoppscotch-backend/src/auth/auth.service.ts" \
  --tested-function generateMagicLinkTokens \
  --callee 'DateTime.now()'
```

**What to look for:**
- `go_to_source_definition: true` in `chosen_definition_reason`
- Path ends with `luxon.js` (not `.d.ts`)
- `full_def_source` is only `let now = () => Date.now(),` — heuristic miss

---

## Run all three (pretty-printed)

```bash
cd /Users/trieyang/Desktop/DocPrism
bash samples.sh
```

Or pipe one command through `jq` for just the definition:

```bash
python3 code_navigation_TypeScript.py \
  --repo-root "$(pwd)/hoppscotch" \
  --script-path "$(pwd)/hoppscotch/packages/hoppscotch-backend/src/auth/auth.service.ts" \
  --tested-function generateMagicLinkTokens \
  --callee 'DateTime.now()' \
  | python3 -c "import json,sys; d=json.load(sys.stdin); od=d['definitions'][0]['outer_definition']; print(od.get('repo_relative_path')); print('---'); print(od.get('full_def_source')[:500])"
```

---

## Compare before vs after (optional)

Re-run the same command against the codebase **without** Go to Source Definition by checking out an older commit, or diff against saved eval rows in:

- `hoppscotch_eval_results_full_postfix_final.json` (before)
- `hoppscotch_eval_results_full_source_def.json` (after)

```bash
python3 - <<'PY'
import json
for label, path, sid, idx in [
    ("before", "hoppscotch_eval_results_full_postfix_final.json", 22, 0),
    ("after",  "hoppscotch_eval_results_full_source_def.json", 22, 0),
]:
    r = next(x for x in json.load(open(path))["results"]
             if x["sample_id"]==sid and x["callee_index"]==idx)
    od = r["definitions"][0]["outer_definition"]
    print(label, od["repo_relative_path"])
    print(od["full_def_source"][:200], "\n")
PY
```
