# Puppeteer — Callee Resolution Classification

**Source:** eval JSON  
**Repo commit:** `4bd8319`  
**Eval status:** 203 / 215 ok callee rows (79 samples with callees, 21 skipped)

## Classification rules

| Metric | Rule |
|--------|------|
| **External libraries** | Definition path contains `node_modules/` |
| **Declaration / interface level** | Outer hit is `.d.ts` or type-only signature, **and** no `runtime_implementation` upgrade |
| **Runtime implementation** | Non-`.d.ts` source with a body, **or** `runtime_implementation.full_def_source` present |

---

## 1. Excluding Prisma, lib.es5.d.ts & const/enum members

**Denominator: 178** ok callee rows

| Metric | Count | % |
|--------|------:|--:|
| External libraries | 40 | **22.5%** |
| Declaration / interface level retrieved | 58 | **32.6%** |
| Runtime implementation retrieved | 120 | **67.4%** |

### Cross-tab (origin × resolution quality)

| Origin | Declaration only | Runtime impl | Total |
|--------|-----------------:|-------------:|------:|
| **External** (node_modules) | 35 (87.5%) | 5 (12.5%) | 40 (22.5%) |
| **Internal** (repo source) | 23 (16.7%) | 115 (83.3%) | 138 (77.5%) |

### Runtime retrieval breakdown (120 rows)

| Mechanism | Count |
|-----------|------:|
| Direct hit on implementation source (`.ts` / `.js` with body) | 111 |
| `.d.ts` upgraded via `runtime_implementation` bundle | 3 |

### Remaining declaration-only rows — examples

- `this.browser` → `ers/trieyang/Desktop/DocPrism/puppeteer/packages/browsers/src/Cache.ts`
- `this.platform` → `ers/trieyang/Desktop/DocPrism/puppeteer/packages/browsers/src/Cache.ts`
- `this.buildId` → `ers/trieyang/Desktop/DocPrism/puppeteer/packages/browsers/src/Cache.ts`
- `path.join(options.path, 'prefs.js')` → `trieyang/Desktop/DocPrism/puppeteer/node_modules/@types/node/path.d.ts`
- `path.join(options.path, 'user.js')` → `trieyang/Desktop/DocPrism/puppeteer/node_modules/@types/node/path.d.ts`
- `Object.entries(options.preferences)` → `ng/Desktop/DocPrism/node_modules/typescript/lib/lib.es2017.object.d.ts`
- `JSON.stringify(key)` → `ers/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es5.d.ts`
- `JSON.stringify(value)` → `ers/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es5.d.ts`
- `Promise.allSettled(...)` → `g/Desktop/DocPrism/node_modules/typescript/lib/lib.es2020.promise.d.ts`
- `fs.promises.writeFile(userPath, lines.join('\n'))` → `g/Desktop/DocPrism/puppeteer/node_modules/@types/node/fs/promises.d.ts`
- `fs.promises` → `s/trieyang/Desktop/DocPrism/puppeteer/node_modules/@types/node/fs.d.ts`
- `Promise.all(...)` → `g/Desktop/DocPrism/node_modules/typescript/lib/lib.es2015.promise.d.ts`

---

## 2. All callees (excl. const/enum members only)

**Denominator: 203** ok callee rows

| Metric | Count | % |
|--------|------:|--:|
| External libraries | 65 | **32.0%** |
| Declaration / interface level retrieved | 83 | **40.9%** |
| Runtime implementation retrieved | 120 | **59.1%** |

### Cross-tab (origin × resolution quality)

| Origin | Declaration only | Runtime impl | Total |
|--------|-----------------:|-------------:|------:|
| **External** (node_modules) | 60 (92.3%) | 5 (7.7%) | 65 (32.0%) |
| **Internal** (repo source) | 23 (16.7%) | 115 (83.3%) | 138 (68.0%) |

### Impact of Prisma + lib.es5 on declaration rate

| Group | Rows | Declaration-only |
|-------|-----:|-----------------:|
| `lib.es5.d.ts` builtins | 25 | 25 (100%) |
| Everything else | 178 | 58 (32.6%) |

---

## 3. % with interface — excluding Prisma, lib.es5 & const/enum

**178 callees**

| Scope | Has interface | % |
|-------|-------------:|--:|
| **Internal** (138) | 49 | **35.5%** |
| **External** (40) | 40 | **100.0%** |
| **All** (178) | 89 | **50.0%** |

---

## 4. % with interface — all callees (excl. const/enum only)

**203 callees**

| Scope | Has interface | % |
|-------|-------------:|--:|
| **Internal** (138) | 49 | **35.5%** |
| **External** (65) | 65 | **100.0%** |
| **All** (203) | 114 | **56.2%** |

---

## 5. Failed rows (navigation errors)

**12** failed callee rows across **9** samples:

- `could not extract tested_function` — 8
- `No definition found from TypeScript LSP.` — 2
- `Chosen definition source does not reference symbol 'detectBrowserPlatf` — 1
- `Chosen definition source does not reference symbol 'resolveBuildId'.` — 1

- sample 45 · `` — could not extract tested_function
- sample 52 · `` — could not extract tested_function
- sample 55 · `` — could not extract tested_function
- sample 56 · `` — could not extract tested_function
- sample 57 · `` — could not extract tested_function
- sample 82 · `` — could not extract tested_function
- sample 88 · `detectBrowserPlatform()` — Chosen definition source does not reference symbol 'detectBrowserPlatform'.
- sample 88 · `resolveBuildId(item.browser, platform, tag)` — Chosen definition source does not reference symbol 'resolveBuildId'.
- sample 88 · `browsers_SupportedBrowser.CHROME` — No definition found from TypeScript LSP.
- sample 88 · `browsers_SupportedBrowser.FIREFOX` — No definition found from TypeScript LSP.
- sample 93 · `` — could not extract tested_function
- sample 98 · `` — could not extract tested_function

*Generated at commit `4bd8319`.*
