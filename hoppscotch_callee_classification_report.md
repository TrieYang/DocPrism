# Hoppscotch Eval — Callee Resolution Classification

**Eval status:** 547 / 547 ok callee rows (94 samples)



---

## 1. Excluding Prisma, lib.es5.d.ts & const/enum members

**Denominator: 425** ok callee rows

| Metric | Count | % |
|--------|------:|--:|
| External libraries | 201 | **47.3%** |
| Declaration / interface level retrieved | 21 | **4.9%** |
| Runtime implementation retrieved | 404 | **95.1%** |

### Cross-tab (origin × resolution quality)

| Origin | Declaration only | Runtime impl | Total |
|--------|-----------------:|-------------:|------:|
| **External** (node_modules) | 20 (4.7%) | 181 (42.6%) | 201 (47.3%) |
| **Internal** (repo source) | 1 (0.2%) | 223 (52.5%) | 224 (52.7%) |

### Runtime retrieval breakdown (404 rows)

| Mechanism | Count |
|-----------|------:|
| Direct hit on implementation source (`.ts` / `.js` with body) | 237 |
| `.d.ts` upgraded via `runtime_implementation` bundle | 167 |

### Remaining declaration-only rows (21) — examples

- **TypeScript builtins** (not lib.es5): `Promise.all`, `Set.add`, `Map.get`, `Array.includes`, `Object.entries`
- **@types only:** `console.error` → `@types/node/console.d.ts`, `URL` → `@types/node/url.d.ts`
- **Vue reactivity getter:** `navStack.value` → `reactivity.d.ts` (`get value(): T`)
- **Package .d.ts:** `response.originalRequest` → `hoppscotch-data/dist/.../13.d.ts`

---

## 2. All callees (excl. const/enum members only)

**Denominator: 532** ok callee rows

| Metric | Count | % |
|--------|------:|--:|
| External libraries | 308 | **57.9%** |
| Declaration / interface level retrieved | 128 | **24.1%** |
| Runtime implementation retrieved | 404 | **75.9%** |

### Cross-tab (origin × resolution quality)

| Origin | Declaration only | Runtime impl | Total |
|--------|-----------------:|-------------:|------:|
| **External** (node_modules) | 127 (23.9%) | 181 (34.0%) | 308 (57.9%) |
| **Internal** (repo source) | 1 (0.2%) | 223 (41.9%) | 224 (42.1%) |

### Impact of Prisma + lib.es5 on declaration rate

| Group | Rows | Declaration-only |
|-------|-----:|-----------------:|
| Prisma (`.prisma/client`) | 85 | 85 (100%) |
| `lib.es5.d.ts` builtins | 22 | 22 (100%) |
| Everything else | 425 | 21 (4.9%) |

Prisma and `lib.es5.d.ts` account for **107 / 128** (84%) of all declaration-only resolutions (among non-const/enum callees).  
Neither group receives a `runtime_implementation` upgrade (generated types / V8 natives).

---

## 3. % with interface — excluding Prisma, lib.es5 & const/enum

**425 callees**

| Scope | Has interface | % |
|-------|-------------:|--:|
| **Internal** (224) | 107 | **47.8%** |
| **External** (201) | 187 | **93.0%** |
| **All** | 294 | **69.2%** |

Internal without interface (~52%): method bodies in repo `.ts` where the snippet is the function itself (`this.cast(...)`, `isValidLength(...)`).  
Internal with interface (~48%): typed fields/deps (`this.userService: UserService`) — type annotation, no separate `.d.ts`.

---

## 4. % with interface — all callees (excl. const/enum only)

**532 callees**

| Scope | Has interface | % |
|-------|-------------:|--:|
| **Internal** (224) | 107 | **47.8%** |
| **External** (308) | 294 | **95.5%** |
| **All** | 401 | **75.4%** |

Prisma (85) and lib.es5 (22) always resolve to `.d.ts` type surfaces.

---

*Generated from `hoppscotch_navigation_results.json`. 
