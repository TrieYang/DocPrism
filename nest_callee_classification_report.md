# Nest Eval — Callee Resolution Classification

**Source:** eval JSON  
**Repo commit:** `cfa2cac53`  
**Eval status:** 205 / 209 ok callee rows (88 samples with callees, 6 skipped)

## Classification rules

| Metric | Rule |
|--------|------|
| **External libraries** | Definition path contains `node_modules/` |
| **Declaration / interface level** | Outer hit is `.d.ts` or type-only signature, **and** no `runtime_implementation` upgrade |
| **Runtime implementation** | Non-`.d.ts` source with a body, **or** `runtime_implementation.full_def_source` present |

---

## 1. Excluding Prisma, lib.es5.d.ts & const/enum members

**Denominator: 186** ok callee rows

| Metric | Count | % |
|--------|------:|--:|
| External libraries | 26 | **14.0%** |
| Declaration / interface level retrieved | 81 | **43.5%** |
| Runtime implementation retrieved | 105 | **56.5%** |

### Cross-tab (origin × resolution quality)

| Origin | Declaration only | Runtime impl | Total |
|--------|-----------------:|-------------:|------:|
| **External** (node_modules) | 17 (65.4%) | 9 (34.6%) | 26 (14.0%) |
| **Internal** (repo source) | 64 (40.0%) | 96 (60.0%) | 160 (86.0%) |

### Runtime retrieval breakdown (105 rows)

| Mechanism | Count |
|-----------|------:|
| Direct hit on implementation source (`.ts` / `.js` with body) | 90 |
| `.d.ts` upgraded via `runtime_implementation` bundle | 0 |

### Remaining declaration-only rows — examples

- `this.cause` → `ang/Desktop/DocPrism/nest/packages/common/exceptions/http.exception.ts`
- `this.validators` → `ng/Desktop/DocPrism/nest/packages/common/pipes/file/parse-file.pipe.ts`
- `this.exceptionFactory(VALIDATION_ERROR_MESSAGE)` → `ieyang/Desktop/DocPrism/nest/packages/common/pipes/parse-array.pipe.ts`
- `Array.isArray(value)` → `ers/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es5.d.ts`
- `JSON.parse(item)` → `ers/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es5.d.ts`
- `Array.isArray(response.message)` → `ers/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es5.d.ts`
- `this.exceptionFactory(errors as any)` → `ieyang/Desktop/DocPrism/nest/packages/common/pipes/parse-array.pipe.ts`
- `Promise.all(value.map(toClassInstance))` → `/Desktop/DocPrism/node_modules/typescript/lib/lib.es2015.iterable.d.ts`
- `isNil(value)` → `s/trieyang/Desktop/DocPrism/nest/packages/common/utils/shared.utils.ts`
- `isString(value)` → `s/trieyang/Desktop/DocPrism/nest/packages/common/utils/shared.utils.ts`
- `this.validationPipe` → `ieyang/Desktop/DocPrism/nest/packages/common/pipes/parse-array.pipe.ts`
- `this.exceptionFactory(...)` → `rieyang/Desktop/DocPrism/nest/packages/common/pipes/parse-enum.pipe.ts`

---

## 2. All callees (excl. const/enum members only)

**Denominator: 204** ok callee rows

| Metric | Count | % |
|--------|------:|--:|
| External libraries | 44 | **21.6%** |
| Declaration / interface level retrieved | 99 | **48.5%** |
| Runtime implementation retrieved | 105 | **51.5%** |

### Cross-tab (origin × resolution quality)

| Origin | Declaration only | Runtime impl | Total |
|--------|-----------------:|-------------:|------:|
| **External** (node_modules) | 35 (79.5%) | 9 (20.5%) | 44 (21.6%) |
| **Internal** (repo source) | 64 (40.0%) | 96 (60.0%) | 160 (78.4%) |

### Impact of Prisma + lib.es5 on declaration rate

| Group | Rows | Declaration-only |
|-------|-----:|-----------------:|
| `lib.es5.d.ts` builtins | 18 | 18 (100%) |
| Everything else | 186 | 81 (43.5%) |

---

## 3. % with interface — excluding Prisma, lib.es5 & const/enum

**186 callees**

| Scope | Has interface | % |
|-------|-------------:|--:|
| **Internal** (160) | 42 | **26.2%** |
| **External** (26) | 17 | **65.4%** |
| **All** (186) | 59 | **31.7%** |

---

## 4. % with interface — all callees (excl. const/enum only)

**204 callees**

| Scope | Has interface | % |
|-------|-------------:|--:|
| **Internal** (160) | 42 | **26.2%** |
| **External** (44) | 35 | **79.5%** |
| **All** (204) | 77 | **37.7%** |

---

## 5. Failed rows (navigation errors)

**4** failed callee rows across **4** samples:

- `could not extract tested_function` — 2
- `No definition found from TypeScript LSP.` — 1
- `No candidates found by anchor inside tested_function (or file if range` — 1

- sample 5 · `err.getResponse()` — No definition found from TypeScript LSP.
- sample 26 · `` — could not extract tested_function
- sample 57 · `` — could not extract tested_function
- sample 94 · `package.json` — No candidates found by anchor inside tested_function (or file if range unknown).

*Generated at commit `cfa2cac53`.*
