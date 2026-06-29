# puppeteer code navigation results

Generated from `code_navigation_TypeScript.resolve_from_snippet` on samples in `puppeteer.json`.

## Summary

- Runtime: 263.88s
- Samples with at least one callee: 78
- Callee rows evaluated: 246 (246 ok, 0 failed)
- Samples skipped (no extractable callees): 22
- Unique resolved definitions shown below: 164 (deduped from 246 callee rows)

---

## 1. Sample 1 · callee #0

- **Function:** `path`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/browsers/src/Cache.ts`
- **Callee:** `cache.installationDir(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 59, col 24 — pattern `core_fallback`

```typescript
cache.installationDir(...)
```

### Resolved definition

- **Path:** `packages/browsers/src/Cache.ts`
- **Range:** line 165, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  installationDir(
    browser: Browser,
    platform: BrowserPlatform,
    buildId: string,
  ): string {
    return path.join(this.browserRoot(browser), `${platform}-${buildId}`);
  }
```

---

## 2. Sample 1 · callee #1

- **Function:** `path`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/browsers/src/Cache.ts`
- **Callee:** `this.browser`
- **Status:** OK

### Usage site (matched in test file)

Line 60, col 7 — pattern `anchor_substring`

```typescript
this.browser
```

### Resolved definition

- **Path:** `packages/browsers/src/Cache.ts`
- **Range:** line 26, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  browser: Browser;
```

---

## 3. Sample 1 · callee #2

- **Function:** `path`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/browsers/src/Cache.ts`
- **Callee:** `this.platform`
- **Status:** OK

### Usage site (matched in test file)

Line 61, col 7 — pattern `anchor_substring`

```typescript
this.platform
```

### Resolved definition

- **Path:** `packages/browsers/src/Cache.ts`
- **Range:** line 28, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  platform: BrowserPlatform;
```

---

## 4. Sample 1 · callee #3

- **Function:** `path`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/browsers/src/Cache.ts`
- **Callee:** `this.buildId`
- **Status:** OK

### Usage site (matched in test file)

Line 62, col 7 — pattern `anchor_substring`

```typescript
this.buildId
```

### Resolved definition

- **Path:** `packages/browsers/src/Cache.ts`
- **Range:** line 27, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  buildId: string;
```

---

## 5. Sample 2 · callee #0

- **Function:** `syncPreferences`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/browsers/src/browser-data/firefox.ts`
- **Callee:** `path.join(options.path, 'prefs.js')`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 431, col 21 — pattern `anchor_substring`

```typescript
path.join(options.path, 'prefs.js')
```

### Resolved definition

- **Path:** `node_modules/@types/node/path.d.ts`
- **Range:** line 74, col 44

```typescript
/**
             * Join all arguments together and normalize the resulting path.
             *
             * @param paths paths to join.
             * @throws {TypeError} if any of the path segments is not a string.
             */
            join(...paths: string[]): string;
```

---

## 6. Sample 2 · callee #2

- **Function:** `syncPreferences`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/browsers/src/browser-data/firefox.ts`
- **Callee:** `Object.entries(options.preferences)`
- **Status:** OK

### Usage site (matched in test file)

Line 434, col 17 — pattern `anchor_substring`

```typescript
Object.entries(options.preferences)
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es2017.object.d.ts`
- **Range:** line 27, col 25

```typescript
/**
     * Returns an array of key/values of the enumerable own properties of an object
     * @param o Object that contains the properties and methods. This can be an object that you created or an existing Document Object Model (DOM) object.
     */
    entries<T>(o: { [s: string]: T; } | ArrayLike<T>): [string, T][];
```

---

## 7. Sample 2 · callee #3

- **Function:** `syncPreferences`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/browsers/src/browser-data/firefox.ts`
- **Callee:** `JSON.stringify(key)`
- **Status:** OK
- **Also seen in:** 2 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 435, col 25 — pattern `anchor_substring`

```typescript
JSON.stringify(key)
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es5.d.ts`
- **Range:** line 1160, col 84

```typescript
/**
     * Converts a JavaScript value to a JavaScript Object Notation (JSON) string.
     * @param value A JavaScript value, usually an object or array, to be converted.
     * @param replacer A function that transforms the results.
     * @param space Adds indentation, white space, and line break characters to the return-value JSON text to make it easier to read.
     * @throws {TypeError} If a circular reference or a BigInt value is found.
     */
    stringify(value: any, replacer?: (this: any, key: string, value: any) => any, space?: string | number): string;
```

---

## 8. Sample 2 · callee #5

- **Function:** `syncPreferences`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/browsers/src/browser-data/firefox.ts`
- **Callee:** `Promise.allSettled(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 439, col 32 — pattern `core_fallback`

```typescript
Promise.allSettled(...)
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es2020.promise.d.ts`
- **Range:** line 28, col 30

```typescript
/**
     * Creates a Promise that is resolved with an array of results when all
     * of the provided Promises resolve or reject.
     * @param values An array of Promises.
     * @returns A new Promise.
     */
    allSettled<T extends readonly unknown[] | []>(values: T): Promise<{ -readonly [P in keyof T]: PromiseSettledResult<Awaited<T[P]>>; }>;
```

---

## 9. Sample 2 · callee #6

- **Function:** `syncPreferences`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/browsers/src/browser-data/firefox.ts`
- **Callee:** `fs.promises.writeFile(userPath, lines.join('\n'))`
- **Status:** OK

### Usage site (matched in test file)

Line 441, col 13 — pattern `anchor_substring`

```typescript
fs.promises.writeFile(userPath, lines.join('\n'))
```

### Resolved definition

- **Path:** `node_modules/@types/node/fs/promises.d.ts`
- **Range:** line 961, col 120

```typescript
/**
     * Asynchronously writes data to a file, replacing the file if it already exists. `data` can be a string, a buffer, an
     * [AsyncIterable](https://tc39.github.io/ecma262/#sec-asynciterable-interface), or an
     * [Iterable](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Iteration_protocols#The_iterable_protocol) object.
     *
     * The `encoding` option is ignored if `data` is a buffer.
     *
     * If `options` is a string, then it specifies the encoding.
     *
     * The `mode` option only affects the newly created file. See `fs.open()` for more details.
     *
     * Any specified `FileHandle` has to support writing.
     *
     * It is unsafe to use `fsPromises.writeFile()` multiple times on the same file
     * without waiting for the promise to be settled.
     *
     * Similarly to `fsPromises.readFile` \- `fsPromises.writeFile` is a convenience
     * method that performs multiple `write` calls internally to write the buffer
     * passed to it. For performance sensitive code consider using `fs.createWriteStream()` or `filehandle.createWriteStream()`.
     *
     * It is possible to use an `AbortSignal` to cancel an `fsPromises.writeFile()`.
     * Cancelation is "best effort", and some amount of data is likely still
     * to be written.
     *
     * ```js
     * import { writeFile } from 'node:fs/promises';
     * import { Buffer } from 'node:buffer';
     *
     * try {
     *   const controller = new AbortController();
     *   const { signal } = controller;
     *   const data = new Uint8Array(Buffer.from('Hello Node.js'));
     *   const promise = writeFile('message.txt', data, { signal });
```

---

## 10. Sample 2 · callee #7

- **Function:** `syncPreferences`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/browsers/src/browser-data/firefox.ts`
- **Callee:** `backupFile(userPath)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 440, col 5 — pattern `anchor_substring`

```typescript
backupFile(userPath)
```

### Resolved definition

- **Path:** `packages/browsers/src/browser-data/firefox.ts`
- **Range:** line 415, col 15
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
async function backupFile(input: string): Promise<void> {
  if (!fs.existsSync(input)) {
    return;
  }
  await fs.promises.copyFile(input, input + '.puppeteer');
}
```

---

## 11. Sample 2 · callee #9

- **Function:** `syncPreferences`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/browsers/src/browser-data/firefox.ts`
- **Callee:** `fs.promises`
- **Status:** OK

### Usage site (matched in test file)

Line 441, col 13 — pattern `anchor_substring`

```typescript
fs.promises
```

### Resolved definition

- **Path:** `node_modules/@types/node/fs.d.ts`
- **Range:** line 24, col 49

```typescript
    import * as promises from "node:fs/promises";
    export { promises };
```

---

## 12. Sample 3 · callee #0

- **Function:** `pages`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/Browser.ts`
- **Callee:** `Promise.all(...)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 383, col 40 — pattern `core_fallback`

```typescript
Promise.all(...)
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es2015.iterable.d.ts`
- **Range:** line 245, col 30

```typescript
/**
     * Creates a Promise that is resolved with an array of results when all of the provided Promises
     * resolve, or rejected when any Promise is rejected.
     * @param values An iterable of Promises.
     * @returns A new Promise.
     */
    all<T>(values: Iterable<T | PromiseLike<T>>): Promise<Awaited<T>[]>;
```

---

## 13. Sample 3 · callee #1

- **Function:** `pages`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/Browser.ts`
- **Callee:** `this.browserContexts()`
- **Status:** OK

### Usage site (matched in test file)

Line 384, col 7 — pattern `anchor_substring`

```typescript
this.browserContexts()
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/bidi/Browser.ts`
- **Range:** line 228, col 3
- **Selection:** `all_implementations`

```typescript
  override browserContexts(): BidiBrowserContext[] {
    return [...this.#browserCore.userContexts].map(context => {
      return this.#browserContexts.get(context)!;
    });
  }
```

### All implementations (2)

#### 1. `packages/puppeteer-core/src/bidi/Browser.ts`

```typescript
  override browserContexts(): BidiBrowserContext[] {
    return [...this.#browserCore.userContexts].map(context => {
      return this.#browserContexts.get(context)!;
    });
  }
```

#### 2. `packages/puppeteer-core/src/cdp/Browser.ts`

```typescript
  override browserContexts(): CdpBrowserContext[] {
    return [this.#defaultContext, ...Array.from(this.#contexts.values())];
  }
```

---

## 14. Sample 3 · callee #2

- **Function:** `pages`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/Browser.ts`
- **Callee:** `context.pages()`
- **Status:** OK

### Usage site (matched in test file)

Line 385, col 16 — pattern `anchor_substring`

```typescript
context.pages()
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/bidi/BrowserContext.ts`
- **Range:** line 221, col 3
- **Selection:** `all_implementations`

```typescript
  override async pages(): Promise<BidiPage[]> {
    return [...this.userContext.browsingContexts].map(context => {
      return this.#pages.get(context)!;
    });
  }
```

### All implementations (2)

#### 1. `packages/puppeteer-core/src/bidi/BrowserContext.ts`

```typescript
  override async pages(): Promise<BidiPage[]> {
    return [...this.userContext.browsingContexts].map(context => {
      return this.#pages.get(context)!;
    });
  }
```

#### 2. `packages/puppeteer-core/src/cdp/BrowserContext.ts`

```typescript
  override async pages(): Promise<Page[]> {
    const pages = await Promise.all(
      this.targets()
        .filter(target => {
          return (
            target.type() === 'page' ||
            (target.type() === 'other' &&
              this.#browser._getIsPageTargetCallback()?.(target))
          );
        })
        .map(target => {
          return target.page();
        }),
    );
    return pages.filter((page): page is Page => {
      return !!page;
    });
  }
```

---

## 15. Sample 4 · callee #0

- **Function:** `cookies`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/Browser.ts`
- **Callee:** `this.defaultBrowserContext()`
- **Status:** OK

### Usage site (matched in test file)

Line 437, col 18 — pattern `anchor_substring`

```typescript
this.defaultBrowserContext()
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/bidi/Browser.ts`
- **Range:** line 234, col 3
- **Selection:** `all_implementations`

```typescript
  override defaultBrowserContext(): BidiBrowserContext {
    return this.#browserContexts.get(this.#browserCore.defaultUserContext)!;
  }
```

### All implementations (2)

#### 1. `packages/puppeteer-core/src/bidi/Browser.ts`

```typescript
  override defaultBrowserContext(): BidiBrowserContext {
    return this.#browserContexts.get(this.#browserCore.defaultUserContext)!;
  }
```

#### 2. `packages/puppeteer-core/src/cdp/Browser.ts`

```typescript
  override defaultBrowserContext(): CdpBrowserContext {
    return this.#defaultContext;
  }
```

---

## 16. Sample 5 · callee #0

- **Function:** `isConnected`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/Browser.ts`
- **Callee:** `this.connected`
- **Status:** OK

### Usage site (matched in test file)

Line 484, col 12 — pattern `anchor_substring`

```typescript
this.connected
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/bidi/Browser.ts`
- **Range:** line 46, col 1
- **Selection:** `all_implementations`

```typescript
  override get connected(): boolean {
    return !this.#browserCore.disconnected;
  }
```

### All implementations (2)

#### 1. `packages/puppeteer-core/src/bidi/Browser.ts`

```typescript
  override get connected(): boolean {
    return !this.#browserCore.disconnected;
  }
```

#### 2. `packages/puppeteer-core/src/cdp/Browser.ts`

```typescript
  override get connected(): boolean {
    return !this.#connection._closed;
  }
```

---

## 17. Sample 6 · callee #0

- **Function:** `deleteCookie`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/BrowserContext.ts`
- **Callee:** `this.setCookie(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 262, col 23 — pattern `core_fallback`

```typescript
this.setCookie(...)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/bidi/BrowserContext.ts`
- **Range:** line 297, col 17
- **Selection:** `all_implementations`

```typescript
  override async setCookie(...cookies: CookieData[]): Promise<void> {
    await Promise.all(
      cookies.map(async cookie => {
        const bidiCookie: Bidi.Storage.PartialCookie = {
          domain: cookie.domain,
          name: cookie.name,
          value: {
            type: 'string',
            value: cookie.value,
          },
          ...(cookie.path !== undefined ? {path: cookie.path} : {}),
          ...(cookie.httpOnly !== undefined ? {httpOnly: cookie.httpOnly} : {}),
          ...(cookie.secure !== undefined ? {secure: cookie.secure} : {}),
          ...(cookie.sameSite !== undefined
            ? {sameSite: convertCookiesSameSiteCdpToBiDi(cookie.sameSite)}
            : {}),
          ...{expiry: convertCookiesExpiryCdpToBiDi(cookie.expires)},
          // Chrome-specific properties.
          ...cdpSpecificCookiePropertiesFromPuppeteerToBidi(
            cookie,
            'sameParty',
            'sourceScheme',
            'priority',
            'url',
          ),
        };
        return await this.userContext.setCookie(
          bidiCookie,
          convertCookiesPartitionKeyFromPuppeteerToBiDi(cookie.partitionKey),
        );
      }),
    );
  }
```

### All implementations (2)

#### 1. `packages/puppeteer-core/src/bidi/BrowserContext.ts`

```typescript
  override async setCookie(...cookies: CookieData[]): Promise<void> {
    await Promise.all(
      cookies.map(async cookie => {
        const bidiCookie: Bidi.Storage.PartialCookie = {
          domain: cookie.domain,
          name: cookie.name,
          value: {
            type: 'string',
            value: cookie.value,
          },
          ...(cookie.path !== undefined ? {path: cookie.path} : {}),
          ...(cookie.httpOnly !== undefined ? {httpOnly: cookie.httpOnly} : {}),
          ...(cookie.secure !== undefined ? {secure: cookie.secure} : {}),
          ...(cookie.sameSite !== undefined
            ? {sameSite: convertCookiesSameSiteCdpToBiDi(cookie.sameSite)}
            : {}),
          ...{expiry: convertCookiesExpiryCdpToBiDi(cookie.expires)},
          // Chrome-specific properties.
          ...cdpSpecificCookiePropertiesFromPuppeteerToBidi(
            cookie,
            'sameParty',
            'sourceScheme',
            'priority',
            'url',
          ),
        };
        return await this.userContext.setCookie(
          bidiCookie,
          convertCookiesPartitionKeyFromPuppeteerToBiDi(cookie.partitionKey),
        );
      }),
    );
  }
```

#### 2. `packages/puppeteer-core/src/cdp/BrowserContext.ts`

```typescript
  override async setCookie(...cookies: CookieData[]): Promise<void> {
    return await this.#connection.send('Storage.setCookies', {
      browserContextId: this.#id,
      cookies: cookies.map(cookie => {
        return {
          ...cookie,
          partitionKey: convertCookiesPartitionKeyFromPuppeteerToCdp(
            cookie.partitionKey,
          ),
        };
      }),
    });
  }
```

---

## 18. Sample 7 · callee #0

- **Function:** `closed`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/BrowserContext.ts`
- **Callee:** `this.browser()`
- **Status:** OK

### Usage site (matched in test file)

Line 276, col 13 — pattern `anchor_substring`

```typescript
this.browser()
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/bidi/BrowserContext.ts`
- **Range:** line 217, col 3
- **Selection:** `all_implementations`

```typescript
  override browser(): BidiBrowser {
    return this.#browser;
  }
```

### All implementations (2)

#### 1. `packages/puppeteer-core/src/bidi/BrowserContext.ts`

```typescript
  override browser(): BidiBrowser {
    return this.#browser;
  }
```

#### 2. `packages/puppeteer-core/src/cdp/BrowserContext.ts`

```typescript
  override browser(): CdpBrowser {
    return this.#browser;
  }
```

---

## 19. Sample 12 · callee #0

- **Function:** `accept`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/Dialog.ts`
- **Callee:** `this.handle(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 97, col 16 — pattern `core_fallback`

```typescript
this.handle(...)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/bidi/Dialog.ts`
- **Range:** line 22, col 17
- **Selection:** `all_implementations`

```typescript
  override async handle(options: {
    accept: boolean;
    text?: string;
  }): Promise<void> {
    await this.#prompt.handle({
      accept: options.accept,
      userText: options.text,
    });
  }
```

### All implementations (2)

#### 1. `packages/puppeteer-core/src/bidi/Dialog.ts`

```typescript
  override async handle(options: {
    accept: boolean;
    text?: string;
  }): Promise<void> {
    await this.#prompt.handle({
      accept: options.accept,
      userText: options.text,
    });
  }
```

#### 2. `packages/puppeteer-core/src/cdp/Dialog.ts`

```typescript
  override async handle(options: {
    accept: boolean;
    text?: string;
  }): Promise<void> {
    await this.#client.send('Page.handleJavaScriptDialog', {
      accept: options.accept,
      promptText: options.text,
    });
  }
```

---

## 20. Sample 12 · callee #1

- **Function:** `accept`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/Dialog.ts`
- **Callee:** `assert(!this.handled, 'Cannot accept dialog which is already handled!')`
- **Status:** OK
- **Also seen in:** 11 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 95, col 5 — pattern `anchor_substring`

```typescript
assert(!this.handled, 'Cannot accept dialog which is already handled!')
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/util/assert.ts`
- **Range:** line 13, col 13
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
 * @license
 * Copyright 2020 Google Inc.
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * Asserts that the given value is truthy.
 * @param value - some conditional statement
 * @param message - the error message to throw if the value is not truthy.
 *
 * @internal
 */
export const assert: (value: unknown, message?: string) => asserts value = (
  value,
  message,
) => {
  if (!value) {
    throw new Error(message);
  }
};
```

---

## 21. Sample 12 · callee #2

- **Function:** `accept`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/Dialog.ts`
- **Callee:** `this.handled`
- **Status:** OK

### Usage site (matched in test file)

Line 95, col 13 — pattern `anchor_substring`

```typescript
this.handled
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/api/Dialog.ts`
- **Range:** line 37, col 24

```typescript
/**
   * @internal
   */
protected handled = false;
```

---

## 22. Sample 14 · callee #1

- **Function:** `continueRequestOverrides`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/HTTPRequest.ts`
- **Callee:** `this.interception`
- **Status:** OK
- **Also seen in:** 4 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 177, col 12 — pattern `anchor_substring`

```typescript
this.interception
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/api/HTTPRequest.ts`
- **Range:** line 133, col 12
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
   * @internal
   */
protected interception: {
```

---

## 23. Sample 16 · callee #1

- **Function:** `interceptResolutionState`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/HTTPRequest.ts`
- **Callee:** `InterceptResolutionAction.Disabled`
- **Status:** OK

### Usage site (matched in test file)

Line 211, col 23 — pattern `anchor_substring`

```typescript
InterceptResolutionAction.Disabled
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/api/HTTPRequest.ts`
- **Range:** line 585, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
Disabled = 'disabled',
```

---

## 24. Sample 16 · callee #2

- **Function:** `interceptResolutionState`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/HTTPRequest.ts`
- **Callee:** `InterceptResolutionAction.AlreadyHandled`
- **Status:** OK

### Usage site (matched in test file)

Line 214, col 23 — pattern `anchor_substring`

```typescript
InterceptResolutionAction.AlreadyHandled
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/api/HTTPRequest.ts`
- **Range:** line 587, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
AlreadyHandled = 'already-handled',
```

---

## 25. Sample 18 · callee #0

- **Function:** `finalizeInterceptions`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/HTTPRequest.ts`
- **Callee:** `this.interception.handlers.reduce(...)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 261, col 38 — pattern `core_fallback`

```typescript
this.interception.handlers.reduce(...)
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es5.d.ts`
- **Range:** line 1479, col 92

```typescript
/**
     * Calls the specified callback function for all the elements in an array. The return value of the callback function is the accumulated result, and is provided as an argument in the next call to the callback function.
     * @param callbackfn A function that accepts up to four arguments. The reduce method calls the callbackfn function one time for each element in the array.
     * @param initialValue If initialValue is specified, it is used as the initial value to start the accumulation. The first call to the callbackfn function provides this value as an argument instead of an array value.
     */
    reduce(callbackfn: (previousValue: T, currentValue: T, currentIndex: number, array: T[]) => T): T;
    reduce(callbackfn: (previousValue: T, currentValue: T, currentIndex: number, array: T[]) => T, initialValue: T): T;
```

---

## 26. Sample 18 · callee #1

- **Function:** `finalizeInterceptions`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/HTTPRequest.ts`
- **Callee:** `Promise.resolve()`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 263, col 8 — pattern `anchor_substring`

```typescript
Promise.resolve()
```

### Resolved definition

- **Path:** `node_modules/typescript/lib/lib.es2015.promise.d.ts`
- **Range:** line 65, col 4
- **Selection:** `dropped_import_export_sites_kept=3`

```typescript

    /**
     * Creates a new resolved promise.
     * @returns A resolved promise.
     */
    resolve(): Promise<void>;
```

---

## 27. Sample 18 · callee #2

- **Function:** `finalizeInterceptions`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/HTTPRequest.ts`
- **Callee:** `this.interceptResolutionState()`
- **Status:** OK

### Usage site (matched in test file)

Line 265, col 22 — pattern `anchor_substring`

```typescript
this.interceptResolutionState()
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/api/HTTPRequest.ts`
- **Range:** line 208, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
   * An InterceptResolutionState object describing the current resolution
   * action and priority.
   *
   * InterceptResolutionState contains:
   * action: InterceptResolutionAction
   * priority?: number
   *
   * InterceptResolutionAction is one of: `abort`, `respond`, `continue`,
   * `disabled`, `none`, or `already-handled`.
   */
  interceptResolutionState(): InterceptResolutionState {
    if (!this.interception.enabled) {
      return {action: InterceptResolutionAction.Disabled};
    }
    if (this.interception.handled) {
      return {action: InterceptResolutionAction.AlreadyHandled};
    }
    return {...this.interception.resolutionState};
  }
```

---

## 28. Sample 18 · callee #3

- **Function:** `finalizeInterceptions`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/HTTPRequest.ts`
- **Callee:** `this._abort(this.interception.abortReason)`
- **Status:** OK

### Usage site (matched in test file)

Line 268, col 22 — pattern `anchor_substring`

```typescript
this._abort(this.interception.abortReason)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/bidi/HTTPRequest.ts`
- **Range:** line 239, col 17
- **Selection:** `all_implementations`

```typescript
  override async _abort(): Promise<void> {
    this.interception.handled = true;
    return await this.#request.failRequest().catch(error => {
      this.interception.handled = false;
      throw error;
    });
  }
```

### All implementations (2)

#### 1. `packages/puppeteer-core/src/bidi/HTTPRequest.ts`

```typescript
  override async _abort(): Promise<void> {
    this.interception.handled = true;
    return await this.#request.failRequest().catch(error => {
      this.interception.handled = false;
      throw error;
    });
  }
```

#### 2. `packages/puppeteer-core/src/cdp/HTTPRequest.ts`

```typescript
  async _abort(
    errorReason: Protocol.Network.ErrorReason | null,
  ): Promise<void> {
    this.interception.handled = true;
    if (this._interceptionId === undefined) {
      throw new Error(
        'HTTPRequest is missing _interceptionId needed for Fetch.failRequest',
      );
    }
    await this.#client
      .send('Fetch.failRequest', {
        requestId: this._interceptionId,
        errorReason: errorReason || 'Failed',
      })
      .catch(handleError);
  }
```

---

## 29. Sample 18 · callee #4

- **Function:** `finalizeInterceptions`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/HTTPRequest.ts`
- **Callee:** `this._respond(this.interception.response)`
- **Status:** OK

### Usage site (matched in test file)

Line 273, col 22 — pattern `anchor_substring`

```typescript
this._respond(this.interception.response)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/bidi/HTTPRequest.ts`
- **Range:** line 247, col 17
- **Selection:** `all_implementations`

```typescript
  override async _respond(
    response: Partial<ResponseForRequest>,
    _priority?: number,
  ): Promise<void> {
    this.interception.handled = true;

    let parsedBody:
      | {
          contentLength: number;
          base64: string;
        }
      | undefined;
    if (response.body) {
      parsedBody = HTTPRequest.getResponse(response.body);
    }

    const headers: Bidi.Network.Header[] = getBidiHeaders(response.headers);
    const hasContentLength = headers.some(header => {
      return header.name === 'content-length';
    });

    if (response.contentType) {
      headers.push({
        name: 'content-type',
        value: {
          type: 'string',
          value: response.contentType,
        },
      });
    }

    if (parsedBody?.contentLength && !hasContentLength) {
      headers.push({
        name: 'content-length',
        value: {
          type: 'string',
          value: String(parsedBody.contentLength),
        },
      });
    }
    const status = response.status || 200;

    return await this.#request
      .provideResponse({
        statusCode: status,
        headers: headers.length > 0 ? headers : undefined,
        reasonPhrase: STATUS_TEXTS[status],
        body: parsedBody?.base64
          ? {
              type: 'base64',
              value: parsedBody?.base64,
            }
          : undefined,
      })
      .catch(error => {
        this.interception.handled = false;
        throw error;
      });
  }
```

### All implementations (2)

#### 1. `packages/puppeteer-core/src/bidi/HTTPRequest.ts`

```typescript
  override async _respond(
    response: Partial<ResponseForRequest>,
    _priority?: number,
  ): Promise<void> {
    this.interception.handled = true;

    let parsedBody:
      | {
          contentLength: number;
          base64: string;
        }
      | undefined;
    if (response.body) {
      parsedBody = HTTPRequest.getResponse(response.body);
    }

    const headers: Bidi.Network.Header[] = getBidiHeaders(response.headers);
    const hasContentLength = headers.some(header => {
      return header.name === 'content-length';
    });

    if (response.contentType) {
      headers.push({
        name: 'content-type',
        value: {
          type: 'string',
          value: response.contentType,
        },
      });
    }

    if (parsedBody?.contentLength && !hasContentLength) {
      headers.push({
        name: 'content-length',
        value: {
          type: 'string',
          value: String(parsedBody.contentLength),
        },
      });
    }
    const status = response.status || 200;

    return await this.#request
      .provideResponse({
        statusCode: status,
        headers: headers.length > 0 ? headers : undefined,
        reasonPhrase: STATUS_TEXTS[status],
        body: parsedBody?.base64
          ? {
              type: 'base64',
              value: parsedBody?.base64,
            }
          : undefined,
      })
      .catch(error => {
        this.interception.handled = false;
        throw error;
      });
  }
```

#### 2. `packages/puppeteer-core/src/cdp/HTTPRequest.ts`

```typescript
  async _respond(response: Partial<ResponseForRequest>): Promise<void> {
    this.interception.handled = true;

    let parsedBody:
      | {
          contentLength: number;
          base64: string;
        }
      | undefined;
    if (response.body) {
      parsedBody = HTTPRequest.getResponse(response.body);
    }

    const responseHeaders: Record<string, string | string[]> = {};
    if (response.headers) {
      for (const header of Object.keys(response.headers)) {
        const value = response.headers[header];

        responseHeaders[header.toLowerCase()] = Array.isArray(value)
          ? value.map(item => {
              return String(item);
            })
          : String(value);
      }
    }
    if (response.contentType) {
      responseHeaders['content-type'] = response.contentType;
    }
    if (parsedBody?.contentLength && !('content-length' in responseHeaders)) {
      responseHeaders['content-length'] = String(parsedBody.contentLength);
    }

    const status = response.status || 200;
    if (this._interceptionId === undefined) {
      throw new Error(
        'HTTPRequest is missing _interceptionId needed for Fetch.fulfillRequest',
      );
    }
    await this.#client
      .send('Fetch.fulfillRequest', {
        requestId: this._interceptionId,
        responseCode: status,
        responsePhrase: STATUS_TEXTS[status],
        responseHeaders: headersArray(responseHeaders),
        body: parsedBody?.base64,
      })
      .catch(error => {
        this.interception.handled = false;
        return handleError(error);
      });
  }
```

---

## 30. Sample 18 · callee #5

- **Function:** `finalizeInterceptions`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/HTTPRequest.ts`
- **Callee:** `this._continue(this.interception.requestOverrides)`
- **Status:** OK

### Usage site (matched in test file)

Line 275, col 22 — pattern `anchor_substring`

```typescript
this._continue(this.interception.requestOverrides)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/bidi/HTTPRequest.ts`
- **Range:** line 215, col 17
- **Selection:** `all_implementations`

```typescript
  override async _continue(
    overrides: ContinueRequestOverrides = {},
  ): Promise<void> {
    const headers: Bidi.Network.Header[] = getBidiHeaders(overrides.headers);
    this.interception.handled = true;

    return await this.#request
      .continueRequest({
        url: overrides.url,
        method: overrides.method,
        body: overrides.postData
          ? {
              type: 'base64',
              value: stringToBase64(overrides.postData),
            }
          : undefined,
        headers: headers.length > 0 ? headers : undefined,
      })
      .catch(error => {
        this.interception.handled = false;
        return handleError(error);
      });
  }
```

### All implementations (2)

#### 1. `packages/puppeteer-core/src/bidi/HTTPRequest.ts`

```typescript
  override async _continue(
    overrides: ContinueRequestOverrides = {},
  ): Promise<void> {
    const headers: Bidi.Network.Header[] = getBidiHeaders(overrides.headers);
    this.interception.handled = true;

    return await this.#request
      .continueRequest({
        url: overrides.url,
        method: overrides.method,
        body: overrides.postData
          ? {
              type: 'base64',
              value: stringToBase64(overrides.postData),
            }
          : undefined,
        headers: headers.length > 0 ? headers : undefined,
      })
      .catch(error => {
        this.interception.handled = false;
        return handleError(error);
      });
  }
```

#### 2. `packages/puppeteer-core/src/cdp/HTTPRequest.ts`

```typescript
/**
   * @internal
   */
  async _continue(overrides: ContinueRequestOverrides = {}): Promise<void> {
    const {url, method, postData, headers} = overrides;
    this.interception.handled = true;

    const postDataBinaryBase64 = postData
      ? stringToBase64(postData)
      : undefined;

    if (this._interceptionId === undefined) {
      throw new Error(
        'HTTPRequest is missing _interceptionId needed for Fetch.continueRequest',
      );
    }
    await this.#client
      .send('Fetch.continueRequest', {
        requestId: this._interceptionId,
        url,
        method,
        postData: postDataBinaryBase64,
        headers: headers ? headersArray(headers) : undefined,
      })
      .catch(error => {
        this.interception.handled = false;
        return handleError(error);
      });
  }
```

---

## 31. Sample 18 · callee #6

- **Function:** `finalizeInterceptions`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/HTTPRequest.ts`
- **Callee:** `Error('Response is missing for the interception')`
- **Status:** OK
- **Also seen in:** 8 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 271, col 21 — pattern `anchor_substring`

```typescript
Error('Response is missing for the interception')
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es5.d.ts`
- **Range:** line 1070, col 38

```typescript
declare var Error: ErrorConstructor;
```

---

## 32. Sample 19 · callee #0

- **Function:** `ok`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/HTTPResponse.ts`
- **Callee:** `this.status()`
- **Status:** OK

### Usage site (matched in test file)

Line 50, col 20 — pattern `anchor_substring`

```typescript
this.status()
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/bidi/HTTPResponse.ts`
- **Range:** line 78, col 11
- **Selection:** `all_implementations`

```typescript
  override status(): number {
    return this.#data.status;
  }
```

### All implementations (2)

#### 1. `packages/puppeteer-core/src/bidi/HTTPResponse.ts`

```typescript
  override status(): number {
    return this.#data.status;
  }
```

#### 2. `packages/puppeteer-core/src/cdp/HTTPResponse.ts`

```typescript
  override status(): number {
    return this.#status;
  }
```

---

## 33. Sample 20 · callee #0

- **Function:** `text`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/HTTPResponse.ts`
- **Callee:** `this.content()`
- **Status:** OK

### Usage site (matched in test file)

Line 105, col 27 — pattern `anchor_substring`

```typescript
this.content()
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/bidi/HTTPResponse.ts`
- **Range:** line 148, col 11
- **Selection:** `all_implementations`

```typescript
  override content(): never {
    throw new UnsupportedOperation();
  }
```

### All implementations (2)

#### 1. `packages/puppeteer-core/src/bidi/HTTPResponse.ts`

```typescript
  override content(): never {
    throw new UnsupportedOperation();
  }
```

#### 2. `packages/puppeteer-core/src/cdp/HTTPResponse.ts`

```typescript
  override content(): Promise<Uint8Array> {
    if (!this.#contentPromise) {
      this.#contentPromise = this.#bodyLoadedDeferred
        .valueOrThrow()
        .then(async () => {
          try {
            // Use CDPSession from corresponding request to retrieve body, as it's client
            // might have been updated (e.g. for an adopted OOPIF).
            const response = await this.#request.client.send(
              'Network.getResponseBody',
              {
                requestId: this.#request.id,
              },
            );

            return stringToTypedArray(response.body, response.base64Encoded);
          } catch (error) {
            if (
              error instanceof ProtocolError &&
              error.originalMessage ===
                'No resource with given identifier found'
            ) {
              throw new ProtocolError(
                'Could not load body for this request. This might happen if the request is a preflight request.',
              );
            }

            throw error;
          }
        });
    }
    return this.#contentPromise;
  }
```

---

## 34. Sample 20 · callee #1

- **Function:** `text`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/HTTPResponse.ts`
- **Callee:** `TextDecoder()`
- **Status:** OK

### Usage site (matched in test file)

Line 106, col 16 — pattern `anchor_substring`

```typescript
TextDecoder()
```

### Resolved definition

- **Path:** `node_modules/@types/node/util.d.ts`
- **Range:** line 1510, col 11

```typescript
/**
     * An implementation of the [WHATWG Encoding Standard](https://encoding.spec.whatwg.org/) `TextDecoder` API.
     *
     * ```js
     * const decoder = new TextDecoder();
     * const u8arr = new Uint8Array([72, 101, 108, 108, 111]);
     * console.log(decoder.decode(u8arr)); // Hello
     * ```
     * @since v8.3.0
     */
    export class TextDecoder {
        /**
         * The encoding supported by the `TextDecoder` instance.
         */
        readonly encoding: string;
        /**
         * The value will be `true` if decoding errors result in a `TypeError` being
         * thrown.
         */
        readonly fatal: boolean;
        /**
         * The value will be `true` if the decoding result will include the byte order
         * mark.
         */
        readonly ignoreBOM: boolean;
        constructor(
            encoding?: string,
            options?: {
                fatal?: boolean | undefined;
                ignoreBOM?: boolean | undefined;
            },
        );
        /**
         * Decodes the `input` and returns a string. If `options.stream` is `true`, any
         * incomplete byte sequences occurring at the end of the `input` are buffered
         * internally and emitted after the next call to `textDecoder.decode()`.
         *
         * If `textDecoder.fatal` is `true`, decoding errors that occur will result in a `TypeError` being thrown.
         * @param input An `ArrayBuffer`, `DataView`, or `TypedArray` instance containing the encoded data.
         */
        decode(
            input?: NodeJS.ArrayBufferView | ArrayBuffer | null,
            options?: {
                stream?: boolean | undefined;
            },
        ): string;
    }
```

---

## 35. Sample 21 · callee #0

- **Function:** `json`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/HTTPResponse.ts`
- **Callee:** `this.text()`
- **Status:** OK

### Usage site (matched in test file)

Line 118, col 27 — pattern `anchor_substring`

```typescript
this.text()
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/api/HTTPResponse.ts`
- **Range:** line 103, col 8
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
   * Promise which resolves to a text (utf8) representation of response body.
   */
  async text(): Promise<string> {
    const content = await this.content();
    return new TextDecoder().decode(content);
  }
```

---

## 36. Sample 21 · callee #1

- **Function:** `json`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/HTTPResponse.ts`
- **Callee:** `JSON.parse(content)`
- **Status:** OK

### Usage site (matched in test file)

Line 119, col 12 — pattern `anchor_substring`

```typescript
JSON.parse(content)
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es5.d.ts`
- **Range:** line 1152, col 16

```typescript
/**
     * Converts a JavaScript Object Notation (JSON) string into an object.
     * @param text A valid JSON string.
     * @param reviver A function that transforms the results. This function is called for each member of the object.
     * If a member contains nested objects, the nested objects are transformed before the parent object is.
     * @throws {SyntaxError} If `text` is not valid JSON.
     */
    parse(text: string, reviver?: (this: any, key: string, value: any) => any): any;
```

---

## 37. Sample 22 · callee #0

- **Function:** `touchMove`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/Input.ts`
- **Callee:** `TouchError('Must start a new Touch first')`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 552, col 17 — pattern `anchor_substring`

```typescript
TouchError('Must start a new Touch first')
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/common/Errors.ts`
- **Range:** line 15, col 2
- **Selection:** `preferred_implementation_over_declaration_kept=2`

```typescript
/**
 * TouchError is thrown when an attempt is made to move or end a touch that does
 * not exist.
 * @public
 */
export class TouchError extends PuppeteerError {}
```

---

## 38. Sample 22 · callee #1

- **Function:** `touchMove`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/Input.ts`
- **Callee:** `this.touches`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 550, col 19 — pattern `anchor_substring`

```typescript
this.touches
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/api/Input.ts`
- **Range:** line 501, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  /**
   * @internal
   */
  touches: TouchHandle[] = [];
```

---

## 39. Sample 23 · callee #0

- **Function:** `touchEnd`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/Input.ts`
- **Callee:** `this.touches.shift()`
- **Status:** OK

### Usage site (matched in test file)

Line 561, col 19 — pattern `anchor_substring`

```typescript
this.touches.shift()
```

### Resolved definition

- **Path:** `node_modules/typescript/lib/lib.es5.d.ts`
- **Range:** line 1370, col 4
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
    /**
     * Removes the first element from an array and returns it.
     * If the array is empty, undefined is returned and the array is not modified.
     */
    shift(): T | undefined;
```

### Nested usages resolved

- `touches` → `packages/puppeteer-core/src/api/Input.ts`

---

## 40. Sample 24 · callee #0

- **Function:** `url`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/Page.ts`
- **Callee:** `this.mainFrame()`
- **Status:** OK
- **Also seen in:** 5 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 1706, col 12 — pattern `anchor_substring`

```typescript
this.mainFrame()
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/bidi/Page.ts`
- **Range:** line 235, col 11
- **Selection:** `all_implementations`

```typescript
  override mainFrame(): BidiFrame {
    return this.#frame;
  }
```

### All implementations (2)

#### 1. `packages/puppeteer-core/src/bidi/Page.ts`

```typescript
  override mainFrame(): BidiFrame {
    return this.#frame;
  }
```

#### 2. `packages/puppeteer-core/src/cdp/Page.ts`

```typescript
  override mainFrame(): CdpFrame {
    return this.#frameManager.mainFrame();
  }
```

---

## 41. Sample 26 · callee #0

- **Function:** `waitForNetworkIdle`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/Page.ts`
- **Callee:** `this.waitForNetworkIdle$(options)`
- **Status:** OK

### Usage site (matched in test file)

Line 1886, col 27 — pattern `anchor_substring`

```typescript
this.waitForNetworkIdle$(options)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/api/Page.ts`
- **Range:** line 1891, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
   * @internal
   */
  waitForNetworkIdle$(
    options: WaitForNetworkIdleOptions = {},
  ): Observable<void> {
    const {
      timeout: ms = this._timeoutSettings.timeout(),
      idleTime = NETWORK_IDLE_TIME,
      concurrency = 0,
      signal,
    } = options;

    return this.#inflight$.pipe(
      switchMap(inflight => {
        if (inflight > concurrency) {
          return EMPTY;
        }
        return timer(idleTime);
      }),
      map(() => {}),
      raceWith(
        timeout(ms),
        fromAbortSignal(signal),
        fromEmitterEvent(this, PageEvent.Close).pipe(
          map(() => {
            throw new TargetCloseError('Page closed!');
          }),
        ),
      ),
    );
  }
```

---

## 42. Sample 26 · callee #1

- **Function:** `waitForNetworkIdle`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/Page.ts`
- **Callee:** `firstValueFrom(this.waitForNetworkIdle$(options))`
- **Status:** OK
- **Also seen in:** 2 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 1886, col 12 — pattern `anchor_substring`

```typescript
firstValueFrom(this.waitForNetworkIdle$(options))
```

### Resolved definition

- **Path:** `node_modules/rxjs/src/internal/firstValueFrom.ts`
- **Range:** line 9, col 16
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
export function firstValueFrom<T>(source: Observable<T>): Promise<T>;
```

---

## 43. Sample 27 · callee #1

- **Function:** `emulate`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/Page.ts`
- **Callee:** `this.setUserAgent(device.userAgent)`
- **Status:** OK

### Usage site (matched in test file)

Line 2025, col 7 — pattern `anchor_substring`

```typescript
this.setUserAgent(device.userAgent)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/bidi/Page.ts`
- **Range:** line 143, col 17
- **Selection:** `all_implementations`

```typescript
  override async setUserAgent(
    userAgent: string,
    userAgentMetadata?: Protocol.Emulation.UserAgentMetadata,
  ): Promise<void> {
    if (!this.#browserContext.browser().cdpSupported && userAgentMetadata) {
      throw new UnsupportedOperation(
        'Current Browser does not support `userAgentMetadata`',
      );
    } else if (
      this.#browserContext.browser().cdpSupported &&
      userAgentMetadata
    ) {
      return await this._client().send('Network.setUserAgentOverride', {
        userAgent: userAgent,
        userAgentMetadata: userAgentMetadata,
      });
    }
    const enable = userAgent !== '';
    userAgent = userAgent ?? (await this.#browserContext.browser().userAgent());

    this._userAgentHeaders = enable
      ? {
          'User-Agent': userAgent,
        }
      : {};

    this.#userAgentInterception = await this.#toggleInterception(
      [Bidi.Network.InterceptPhase.BeforeRequestSent],
      this.#userAgentInterception,
      enable,
    );

    const changeUserAgent = (userAgent: string) => {
      Object.defineProperty(navigator, 'userAgent', {
        value: userAgent,
        configurable: true,
      });
    };

    const frames = [this.#frame];
    for (const frame of frames) {
      frames.push(...frame.childFrames());
    }

    if (this.#userAgentPreloadScript) {
      await this.removeScriptToEvaluateOnNewDocument(
        this.#userAgentPreloadScript,
      );
    }
    const [evaluateToken] = await Promise.all([
      enable
        ? this.evaluateOnNewDocument(changeUserAgent, userAgent)
        : undefined,
      // When we disable the UserAgent we want to
      // evaluate the original value in all Browsing Contexts
      ...frames.map(frame => {
        return frame.evaluate(changeUserAgent, userAgent);
      }),
    ]);
    this.#userAgentPreloadScript = evaluateToken?.identifier;
  }
```

### All implementations (2)

#### 1. `packages/puppeteer-core/src/bidi/Page.ts`

```typescript
  override async setUserAgent(
    userAgent: string,
    userAgentMetadata?: Protocol.Emulation.UserAgentMetadata,
  ): Promise<void> {
    if (!this.#browserContext.browser().cdpSupported && userAgentMetadata) {
      throw new UnsupportedOperation(
        'Current Browser does not support `userAgentMetadata`',
      );
    } else if (
      this.#browserContext.browser().cdpSupported &&
      userAgentMetadata
    ) {
      return await this._client().send('Network.setUserAgentOverride', {
        userAgent: userAgent,
        userAgentMetadata: userAgentMetadata,
      });
    }
    const enable = userAgent !== '';
    userAgent = userAgent ?? (await this.#browserContext.browser().userAgent());

    this._userAgentHeaders = enable
      ? {
          'User-Agent': userAgent,
        }
      : {};

    this.#userAgentInterception = await this.#toggleInterception(
      [Bidi.Network.InterceptPhase.BeforeRequestSent],
      this.#userAgentInterception,
      enable,
    );

    const changeUserAgent = (userAgent: string) => {
      Object.defineProperty(navigator, 'userAgent', {
        value: userAgent,
        configurable: true,
      });
    };

    const frames = [this.#frame];
    for (const frame of frames) {
      frames.push(...frame.childFrames());
    }

    if (this.#userAgentPreloadScript) {
      await this.removeScriptToEvaluateOnNewDocument(
        this.#userAgentPreloadScript,
      );
    }
    const [evaluateToken] = await Promise.all([
      enable
        ? this.evaluateOnNewDocument(changeUserAgent, userAgent)
        : undefined,
      // When we disable the UserAgent we want to
      // evaluate the original value in all Browsing Contexts
      ...frames.map(frame => {
        return frame.evaluate(changeUserAgent, userAgent);
      }),
    ]);
    this.#userAgentPreloadScript = evaluateToken?.identifier;
  }
```

#### 2. `packages/puppeteer-core/src/cdp/Page.ts`

```typescript
  override async setUserAgent(
    userAgent: string,
    userAgentMetadata?: Protocol.Emulation.UserAgentMetadata,
  ): Promise<void> {
    return await this.#frameManager.networkManager.setUserAgent(
      userAgent,
      userAgentMetadata,
    );
  }
```

---

## 44. Sample 27 · callee #2

- **Function:** `emulate`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/Page.ts`
- **Callee:** `this.setViewport(device.viewport)`
- **Status:** OK

### Usage site (matched in test file)

Line 2026, col 7 — pattern `anchor_substring`

```typescript
this.setViewport(device.viewport)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/bidi/Page.ts`
- **Range:** line 379, col 3
- **Selection:** `all_implementations`

```typescript
  override async setViewport(viewport: Viewport | null): Promise<void> {
    if (!this.browser().cdpSupported) {
      await this.#frame.browsingContext.setViewport({
        viewport:
          viewport?.width && viewport?.height
            ? {
                width: viewport.width,
                height: viewport.height,
              }
            : null,
        devicePixelRatio: viewport?.deviceScaleFactor
          ? viewport.deviceScaleFactor
          : null,
      });
      this.#viewport = viewport;
      return;
    }
    const needsReload =
      await this.#cdpEmulationManager.emulateViewport(viewport);
    this.#viewport = viewport;
    if (needsReload) {
      await this.reload();
    }
  }
```

### All implementations (2)

#### 1. `packages/puppeteer-core/src/bidi/Page.ts`

```typescript
  override async setViewport(viewport: Viewport | null): Promise<void> {
    if (!this.browser().cdpSupported) {
      await this.#frame.browsingContext.setViewport({
        viewport:
          viewport?.width && viewport?.height
            ? {
                width: viewport.width,
                height: viewport.height,
              }
            : null,
        devicePixelRatio: viewport?.deviceScaleFactor
          ? viewport.deviceScaleFactor
          : null,
      });
      this.#viewport = viewport;
      return;
    }
    const needsReload =
      await this.#cdpEmulationManager.emulateViewport(viewport);
    this.#viewport = viewport;
    if (needsReload) {
      await this.reload();
    }
  }
```

#### 2. `packages/puppeteer-core/src/cdp/Page.ts`

```typescript
  override async setViewport(viewport: Viewport | null): Promise<void> {
    const needsReload = await this.#emulationManager.emulateViewport(viewport);
    this.#viewport = viewport;
    if (needsReload) {
      await this.reload();
    }
  }
```

---

## 45. Sample 35 · callee #0

- **Function:** `waitHandle`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/locators/locators.ts`
- **Callee:** `this._wait(options)`
- **Status:** OK

### Usage site (matched in test file)

Line 629, col 7 — pattern `anchor_substring`

```typescript
this._wait(options)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/api/locators/locators.ts`
- **Range:** line 772, col 2
- **Selection:** `all_implementations`

```typescript
  _wait(options?: Readonly<ActionOptions>): Observable<HandleFor<T>> {
    const signal = options?.signal;
    return defer(() => {
      return from(
        this.#pageOrFrame.waitForFunction(this.#func, {
          timeout: this.timeout,
          signal,
        }),
      );
    }).pipe(throwIfEmpty());
  }
```

### All implementations (5)

#### 1. `packages/puppeteer-core/src/api/locators/locators.ts`

```typescript
  _wait(options?: Readonly<ActionOptions>): Observable<HandleFor<T>> {
    const signal = options?.signal;
    return defer(() => {
      return from(
        this.#pageOrFrame.waitForFunction(this.#func, {
          timeout: this.timeout,
          signal,
        }),
      );
    }).pipe(throwIfEmpty());
  }
```

#### 2. `packages/puppeteer-core/src/api/locators/locators.ts`

```typescript
  override _wait(options?: Readonly<ActionOptions>): Observable<HandleFor<To>> {
    return this.delegate._wait(options).pipe(
      mergeMap(handle => {
        return from(
          Promise.resolve(this.#predicate(handle, options?.signal)),
        ).pipe(
          filter(value => {
            return value;
          }),
          map(() => {
            // SAFETY: It passed the predicate, so this is correct.
            return handle as HandleFor<To>;
          }),
        );
      }),
      throwIfEmpty(),
    );
  }
```

#### 3. `packages/puppeteer-core/src/api/locators/locators.ts`

```typescript
  override _wait(options?: Readonly<ActionOptions>): Observable<HandleFor<To>> {
    return this.delegate._wait(options).pipe(
      mergeMap(handle => {
        return from(Promise.resolve(this.#mapper(handle, options?.signal)));
      }),
    );
  }
```

#### 4. `packages/puppeteer-core/src/api/locators/locators.ts`

```typescript
  override _wait(options?: Readonly<ActionOptions>): Observable<HandleFor<T>> {
    const signal = options?.signal;
    return defer(() => {
      return from(
        this.#pageOrFrame.waitForSelector(this.#selector, {
          visible: false,
          timeout: this._timeout,
          signal,
        }) as Promise<HandleFor<T> | null>,
      );
    }).pipe(
      filter((value): value is NonNullable<typeof value> => {
        return value !== null;
      }),
      throwIfEmpty(),
      this.operators.conditions([this.#waitForVisibilityIfNeeded], signal),
    );
  }
```

#### 5. `packages/puppeteer-core/src/api/locators/locators.ts`

```typescript
  override _wait(options?: Readonly<ActionOptions>): Observable<HandleFor<T>> {
    return race(
      ...this.#locators.map(locator => {
        return locator._wait(options);
      }),
    );
  }
```

---

## 46. Sample 35 · callee #1

- **Function:** `waitHandle`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/locators/locators.ts`
- **Callee:** `this.operators.retryAndRaceWithSignalAndTimer(options?.signal, cause)`
- **Status:** OK

### Usage site (matched in test file)

Line 630, col 9 — pattern `anchor_substring`

```typescript
this.operators.retryAndRaceWithSignalAndTimer(options?.signal, cause)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/api/locators/locators.ts`
- **Range:** line 148, col 4
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
retryAndRaceWithSignalAndTimer: <T>(
      signal?: AbortSignal,
      cause?: Error,
    ): OperatorFunction<T, T> => {
      const candidates = [];
      if (signal) {
        candidates.push(fromAbortSignal(signal, cause));
      }
      candidates.push(timeout(this._timeout, cause));
      return pipe(
        retry({delay: RETRY_DELAY}),
        raceWith<T, never[]>(...candidates),
      );
    },
```

---

## 47. Sample 35 · callee #4

- **Function:** `waitHandle`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/locators/locators.ts`
- **Callee:** `this.operators`
- **Status:** OK

### Usage site (matched in test file)

Line 630, col 9 — pattern `anchor_substring`

```typescript
this.operators
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/api/locators/locators.ts`
- **Range:** line 130, col 35

```typescript
/**
   * @internal
   */
protected operators = {
    conditions: (
      conditions: Array<Action<T, never>>,
      signal?: AbortSignal,
    ): OperatorFunction<HandleFor<T>, HandleFor<T>> => {
      return mergeMap((handle: HandleFor<T>) => {
        return merge(
          ...conditions.map(condition => {
            return condition(handle, signal);
          }),
        ).pipe(defaultIfEmpty(handle));
      });
    },
    retryAndRaceWithSignalAndTimer: <T>(
      signal?: AbortSignal,
      cause?: Error,
    ): OperatorFunction<T, T> => {
      const candidates = [];
      if (signal) {
        candidates.push(fromAbortSignal(signal, cause));
      }
      candidates.push(timeout(this._timeout, cause));
      return pipe(
        retry({delay: RETRY_DELAY}),
        raceWith<T, never[]>(...candidates),
      );
    },
  };
```

---

## 48. Sample 36 · callee #0

- **Function:** `map`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/locators/locators.ts`
- **Callee:** `this._clone()`
- **Status:** OK
- **Also seen in:** 2 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 653, col 30 — pattern `anchor_substring`

```typescript
this._clone()
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/api/locators/locators.ts`
- **Range:** line 768, col 11
- **Selection:** `all_implementations`

```typescript
  override _clone(): FunctionLocator<T> {
    return new FunctionLocator(this.#pageOrFrame, this.#func);
  }
```

### All implementations (5)

#### 1. `packages/puppeteer-core/src/api/locators/locators.ts`

```typescript
  override _clone(): FunctionLocator<T> {
    return new FunctionLocator(this.#pageOrFrame, this.#func);
  }
```

#### 2. `packages/puppeteer-core/src/api/locators/locators.ts`

```typescript
  override _clone(): FilteredLocator<From, To> {
    return new FilteredLocator(
      this.delegate.clone(),
      this.#predicate,
    ).copyOptions(this);
  }
```

#### 3. `packages/puppeteer-core/src/api/locators/locators.ts`

```typescript
  override _clone(): MappedLocator<From, To> {
    return new MappedLocator(this.delegate.clone(), this.#mapper).copyOptions(
      this,
    );
  }
```

#### 4. `packages/puppeteer-core/src/api/locators/locators.ts`

```typescript
  override _clone(): NodeLocator<T> {
    return new NodeLocator<T>(this.#pageOrFrame, this.#selector).copyOptions(
      this,
    );
  }
```

#### 5. `packages/puppeteer-core/src/api/locators/locators.ts`

```typescript
  override _clone(): RaceLocator<T> {
    return new RaceLocator<T>(
      this.#locators.map(locator => {
        return locator.clone();
      }),
    ).copyOptions(this);
  }
```

---

## 49. Sample 36 · callee #1

- **Function:** `map`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/locators/locators.ts`
- **Callee:** `MappedLocator(...)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 653, col 16 — pattern `core_fallback`

```typescript
MappedLocator(...)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/api/locators/locators.ts`
- **Range:** line 930, col 13
- **Selection:** `preferred_implementation_over_declaration_kept=2`

```typescript
/**
 * @internal
 */
export class MappedLocator<From, To> extends DelegatedLocator<From, To> {
  #mapper: HandleMapper<From, To>;

  constructor(base: Locator<From>, mapper: HandleMapper<From, To>) {
    super(base);
    this.#mapper = mapper;
  }

  override _clone(): MappedLocator<From, To> {
    return new MappedLocator(this.delegate.clone(), this.#mapper).copyOptions(
      this,
    );
  }

  override _wait(options?: Readonly<ActionOptions>): Observable<HandleFor<To>> {
    return this.delegate._wait(options).pipe(
      mergeMap(handle => {
        return from(Promise.resolve(this.#mapper(handle, options?.signal)));
      }),
    );
  }
}
```

---

## 50. Sample 37 · callee #1

- **Function:** `filter`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/locators/locators.ts`
- **Callee:** `frame.waitForFunction(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 668, col 51 — pattern `core_fallback`

```typescript
frame.waitForFunction(...)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/api/Frame.ts`
- **Range:** line 786, col 8
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  async waitForFunction<
    Params extends unknown[],
    Func extends EvaluateFunc<Params> = EvaluateFunc<Params>,
  >(
    pageFunction: Func | string,
    options: FrameWaitForFunctionOptions = {},
    ...args: Params
  ): Promise<HandleFor<Awaited<ReturnType<Func>>>> {
    return await (this.mainRealm().waitForFunction(
      pageFunction,
      options,
      ...args,
    ) as Promise<HandleFor<Awaited<ReturnType<Func>>>>);
  }
```

---

## 51. Sample 37 · callee #2

- **Function:** `filter`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/locators/locators.ts`
- **Callee:** `FilteredLocator(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 667, col 16 — pattern `core_fallback`

```typescript
FilteredLocator(...)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/api/locators/locators.ts`
- **Range:** line 878, col 13
- **Selection:** `preferred_implementation_over_declaration_kept=2`

```typescript
/**
 * @internal
 */
export class FilteredLocator<From, To extends From> extends DelegatedLocator<
  From,
  To
> {
  #predicate: HandlePredicate<From, To>;

  constructor(base: Locator<From>, predicate: HandlePredicate<From, To>) {
    super(base);
    this.#predicate = predicate;
  }

  override _clone(): FilteredLocator<From, To> {
    return new FilteredLocator(
      this.delegate.clone(),
      this.#predicate,
    ).copyOptions(this);
  }

  override _wait(options?: Readonly<ActionOptions>): Observable<HandleFor<To>> {
    return this.delegate._wait(options).pipe(
      mergeMap(handle => {
        return from(
          Promise.resolve(this.#predicate(handle, options?.signal)),
        ).pipe(
          filter(value => {
            return value;
          }),
          map(() => {
            // SAFETY: It passed the predicate, so this is correct.
            return handle as HandleFor<To>;
          }),
        );
      }),
      throwIfEmpty(),
    );
  }
}
```

---

## 52. Sample 37 · callee #3

- **Function:** `filter`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/locators/locators.ts`
- **Callee:** `await (handle as ElementHandle<Node>)`
- **Status:** OK

### Usage site (matched in test file)

Line 668, col 7 — pattern `anchor_substring`

```typescript
await (handle as ElementHandle<Node>)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/api/locators/locators.ts`
- **Range:** line 666, col 46
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
      await (handle as ElementHandle<Node>).frame.waitForFunction(
        predicate,
        {signal, timeout: this._timeout},
        handle,
      );
```

---

## 53. Sample 37 · callee #4

- **Function:** `filter`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/api/locators/locators.ts`
- **Callee:** `this._timeout`
- **Status:** OK

### Usage site (matched in test file)

Line 670, col 27 — pattern `anchor_substring`

```typescript
this._timeout
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/api/locators/locators.ts`
- **Range:** line 123, col 48

```typescript
/**
   * @internal
   */
protected _timeout = 30000;
```

---

## 54. Sample 39 · callee #0

- **Function:** `unbind`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/bidi/Connection.ts`
- **Callee:** `callbacks.clear()`
- **Status:** OK

### Usage site (matched in test file)

Line 183, col 11 — pattern `anchor_substring`

```typescript
callbacks.clear()
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/common/CallbackRegistry.ts`
- **Range:** line 97, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  clear(): void {
    for (const callback of this.#callbacks.values()) {
      // TODO: probably we can accept error messages as params.
      this._reject(callback, new TargetCloseError('Target closed'));
    }
    this.#callbacks.clear();
  }
```

---

## 55. Sample 39 · callee #1

- **Function:** `unbind`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/bidi/Connection.ts`
- **Callee:** `transport.onmessage`
- **Status:** OK

### Usage site (matched in test file)

Line 180, col 11 — pattern `anchor_substring`

```typescript
transport.onmessage
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/common/ConnectionTransport.ts`
- **Range:** line 12, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  onmessage?: (message: string) => void;
```

---

## 56. Sample 39 · callee #2

- **Function:** `unbind`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/bidi/Connection.ts`
- **Callee:** `transport.onclose`
- **Status:** OK

### Usage site (matched in test file)

Line 181, col 11 — pattern `anchor_substring`

```typescript
transport.onclose
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/common/ConnectionTransport.ts`
- **Range:** line 13, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  onclose?: () => void;
```

---

## 57. Sample 40 · callee #0

- **Function:** `dispose`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/bidi/Connection.ts`
- **Callee:** `this.unbind()`
- **Status:** OK

### Usage site (matched in test file)

Line 190, col 5 — pattern `anchor_substring`

```typescript
this.unbind()
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/bidi/Connection.ts`
- **Range:** line 173, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
   * Unbinds the connection, but keeps the transport open. Useful when the transport will
   * be reused by other connection e.g. with different protocol.
   * @internal
   */
  unbind(): void {
    if (this.#closed) {
      return;
    }
    this.#closed = true;
    // Both may still be invoked and produce errors
    this.#transport.onmessage = () => {};
    this.#transport.onclose = () => {};

    this.#callbacks.clear();
  }
```

---

## 58. Sample 40 · callee #1

- **Function:** `dispose`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/bidi/Connection.ts`
- **Callee:** `transport.close()`
- **Status:** OK

### Usage site (matched in test file)

Line 191, col 11 — pattern `anchor_substring`

```typescript
transport.close()
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/bidi/Connection.test.ts`
- **Range:** line 23, col 4
- **Selection:** `all_implementations`

```typescript
    close(): void {
      this.closed = true;
    }
```

### All implementations (4)

#### 1. `packages/puppeteer-core/src/bidi/Connection.test.ts`

```typescript
    close(): void {
      this.closed = true;
    }
```

#### 2. `packages/puppeteer-core/src/cdp/ExtensionTransport.ts`

```typescript
  close(): void {
    chrome.debugger.onEvent.removeListener(this.#debuggerEventHandler);
    void chrome.debugger.detach({tabId: this.#tabId});
  }
```

#### 3. `packages/puppeteer-core/src/common/BrowserWebSocketTransport.ts`

```typescript
  close(): void {
    this.#ws.close();
  }
```

#### 4. `packages/puppeteer-core/src/node/PipeTransport.ts`

```typescript
  close(): void {
    this.#isClosed = true;
    this.#subscriptions.dispose();
  }
```

---

## 59. Sample 42 · callee #0

- **Function:** `testUrlMatchCookie`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/bidi/Page.ts`
- **Callee:** `URL(url)`
- **Status:** OK

### Usage site (matched in test file)

Line 998, col 29 — pattern `anchor_substring`

```typescript
URL(url)
```

### Resolved definition

- **Path:** `node_modules/@types/node/url.d.ts`
- **Range:** line 941, col 61

```typescript
        interface URL extends _URL {}
```

---

## 60. Sample 42 · callee #2

- **Function:** `testUrlMatchCookie`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/bidi/Page.ts`
- **Callee:** `testUrlMatchCookieHostname(cookie, normalizedUrl)`
- **Status:** OK

### Usage site (matched in test file)

Line 1000, col 8 — pattern `anchor_substring`

```typescript
testUrlMatchCookieHostname(cookie, normalizedUrl)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/bidi/Page.ts`
- **Range:** line 950, col 9
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
 * Check domains match.
 */
function testUrlMatchCookieHostname(
  cookie: Cookie,
  normalizedUrl: URL,
): boolean {
  const cookieDomain = cookie.domain.toLowerCase();
  const urlHostname = normalizedUrl.hostname.toLowerCase();
  if (cookieDomain === urlHostname) {
    return true;
  }
  // TODO: does not consider additional restrictions w.r.t to IP
  // addresses which is fine as it is for representation and does not
  // mean that cookies actually apply that way in the browser.
  // https://datatracker.ietf.org/doc/html/rfc6265#section-5.1.3
  return cookieDomain.startsWith('.') && urlHostname.endsWith(cookieDomain);
}
```

---

## 61. Sample 42 · callee #3

- **Function:** `testUrlMatchCookie`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/bidi/Page.ts`
- **Callee:** `testUrlMatchCookiePath(cookie, normalizedUrl)`
- **Status:** OK

### Usage site (matched in test file)

Line 1003, col 10 — pattern `anchor_substring`

```typescript
testUrlMatchCookiePath(cookie, normalizedUrl)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/bidi/Page.ts`
- **Range:** line 970, col 9
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
 * Check paths match.
 * Spec: https://datatracker.ietf.org/doc/html/rfc6265#section-5.1.4
 */
function testUrlMatchCookiePath(cookie: Cookie, normalizedUrl: URL): boolean {
  const uriPath = normalizedUrl.pathname;
  const cookiePath = cookie.path;

  if (uriPath === cookiePath) {
    // The cookie-path and the request-path are identical.
    return true;
  }
  if (uriPath.startsWith(cookiePath)) {
    // The cookie-path is a prefix of the request-path.
    if (cookiePath.endsWith('/')) {
      // The last character of the cookie-path is %x2F ("/").
      return true;
    }
    if (uriPath[cookiePath.length] === '/') {
      // The first character of the request-path that is not included in the cookie-path
      // is a %x2F ("/") character.
      return true;
    }
  }
  return false;
}
```

---

## 62. Sample 45 · callee #0

- **Function:** `detach`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/CdpSession.ts`
- **Callee:** `connection.send(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 152, col 28 — pattern `core_fallback`

```typescript
connection.send(...)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/cdp/Connection.ts`
- **Range:** line 108, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  send<T extends keyof ProtocolMapping.Commands>(
    method: T,
    params?: ProtocolMapping.Commands[T]['paramsType'][0],
    options?: CommandOptions,
  ): Promise<ProtocolMapping.Commands[T]['returnType']> {
    // There is only ever 1 param arg passed, but the Protocol defines it as an
    // array of 0 or 1 items See this comment:
    // https://github.com/ChromeDevTools/devtools-protocol/pull/113#issuecomment-412603285
    // which explains why the protocol defines the params this way for better
    // type-inference.
    // So now we check if there are any params or not and deal with them accordingly.
    return this._rawSend(this.#callbacks, method, params, undefined, options);
  }
```

---

## 63. Sample 45 · callee #2

- **Function:** `detach`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/CdpSession.ts`
- **Callee:** `this.detached`
- **Status:** OK

### Usage site (matched in test file)

Line 147, col 9 — pattern `anchor_substring`

```typescript
this.detached
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/cdp/CdpSession.ts`
- **Range:** line 76, col 15
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  override get detached(): boolean {
    return this.#connection._closed || this.#detached;
  }
```

---

## 64. Sample 46 · callee #0

- **Function:** `session`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/Connection.ts`
- **Callee:** `this._session(sessionId)`
- **Status:** OK

### Usage site (matched in test file)

Line 102, col 12 — pattern `anchor_substring`

```typescript
this._session(sessionId)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/cdp/Connection.ts`
- **Range:** line 92, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
   * @internal
   */
  _session(sessionId: string): CdpCDPSession | null {
    return this.#sessions.get(sessionId) || null;
  }
```

---

## 65. Sample 47 · callee #0

- **Function:** `startJSCoverage`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/Coverage.ts`
- **Callee:** `jsCoverage.start(options)`
- **Status:** OK

### Usage site (matched in test file)

Line 152, col 24 — pattern `anchor_substring`

```typescript
jsCoverage.start(options)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/cdp/Coverage.ts`
- **Range:** line 215, col 8
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  async start(
    options: {
      resetOnNavigation?: boolean;
      reportAnonymousScripts?: boolean;
      includeRawScriptCoverage?: boolean;
      useBlockCoverage?: boolean;
    } = {},
  ): Promise<void> {
    assert(!this.#enabled, 'JSCoverage is already enabled');
    const {
      resetOnNavigation = true,
      reportAnonymousScripts = false,
      includeRawScriptCoverage = false,
      useBlockCoverage = true,
    } = options;
    this.#resetOnNavigation = resetOnNavigation;
    this.#reportAnonymousScripts = reportAnonymousScripts;
    this.#includeRawScriptCoverage = includeRawScriptCoverage;
    this.#enabled = true;
    this.#scriptURLs.clear();
    this.#scriptSources.clear();
    this.#subscriptions = new DisposableStack();
    const clientEmitter = this.#subscriptions.use(
      new EventEmitter(this.#client),
    );
    clientEmitter.on('Debugger.scriptParsed', this.#onScriptParsed.bind(this));
    clientEmitter.on(
      'Runtime.executionContextsCleared',
      this.#onExecutionContextsCleared.bind(this),
    );
    await Promise.all([
      this.#client.send('Profiler.enable'),
      this.#client.send('Profiler.startPreciseCoverage', {
        callCount: this.#includeRawScriptCoverage,
        detailed: useBlockCoverage,
      }),
      this.#client.send('Debugger.enable'),
      this.#client.send('Debugger.setSkipAllPauses', {skip: true}),
    ]);
  }
```

---

## 66. Sample 48 · callee #0

- **Function:** `startCSSCoverage`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/Coverage.ts`
- **Callee:** `cssCoverage.start(options)`
- **Status:** OK

### Usage site (matched in test file)

Line 173, col 24 — pattern `anchor_substring`

```typescript
cssCoverage.start(options)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/cdp/Coverage.ts`
- **Range:** line 349, col 8
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  async start(options: {resetOnNavigation?: boolean} = {}): Promise<void> {
    assert(!this.#enabled, 'CSSCoverage is already enabled');
    const {resetOnNavigation = true} = options;
    this.#resetOnNavigation = resetOnNavigation;
    this.#enabled = true;
    this.#stylesheetURLs.clear();
    this.#stylesheetSources.clear();
    this.#eventListeners = new DisposableStack();
    const clientEmitter = this.#eventListeners.use(
      new EventEmitter(this.#client),
    );
    clientEmitter.on('CSS.styleSheetAdded', this.#onStyleSheet.bind(this));
    clientEmitter.on(
      'Runtime.executionContextsCleared',
      this.#onExecutionContextsCleared.bind(this),
    );

    await Promise.all([
      this.#client.send('DOM.enable'),
      this.#client.send('CSS.enable'),
      this.#client.send('CSS.startRuleUsageTracking'),
    ]);
  }
```

---

## 67. Sample 49 · callee #0

- **Function:** `stopCSSCoverage`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/Coverage.ts`
- **Callee:** `cssCoverage.stop()`
- **Status:** OK

### Usage site (matched in test file)

Line 185, col 24 — pattern `anchor_substring`

```typescript
cssCoverage.stop()
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/cdp/Coverage.ts`
- **Range:** line 399, col 8
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  async stop(): Promise<CoverageEntry[]> {
    assert(this.#enabled, 'CSSCoverage is not enabled');
    this.#enabled = false;
    const ruleTrackingResponse = await this.#client.send(
      'CSS.stopRuleUsageTracking',
    );
    await Promise.all([
      this.#client.send('CSS.disable'),
      this.#client.send('DOM.disable'),
    ]);
    this.#eventListeners?.dispose();

    // aggregate by styleSheetId
    const styleSheetIdToCoverage = new Map();
    for (const entry of ruleTrackingResponse.ruleUsage) {
      let ranges = styleSheetIdToCoverage.get(entry.styleSheetId);
      if (!ranges) {
        ranges = [];
        styleSheetIdToCoverage.set(entry.styleSheetId, ranges);
      }
      ranges.push({
        startOffset: entry.startOffset,
        endOffset: entry.endOffset,
        count: entry.used ? 1 : 0,
      });
    }

    const coverage: CoverageEntry[] = [];
    for (const styleSheetId of this.#stylesheetURLs.keys()) {
      const url = this.#stylesheetURLs.get(styleSheetId);
      assert(
        typeof url !== 'undefined',
        `Stylesheet URL is undefined (styleSheetId=${styleSheetId})`,
      );
      const text = this.#stylesheetSources.get(styleSheetId);
      assert(
        typeof text !== 'undefined',
        `Stylesheet text is undefined (styleSheetId=${styleSheetId})`,
      );
      const ranges = convertToDisjointRanges(
        styleSheetIdToCoverage.get(styleSheetId) || [],
      );
      coverage.push({url, ranges, text});
    }

    return coverage;
  }
```

---

## 68. Sample 50 · callee #0

- **Function:** `select`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/DeviceRequestPrompt.ts`
- **Callee:** `this.devices.includes(device)`
- **Status:** OK

### Usage site (matched in test file)

Line 175, col 12 — pattern `anchor_substring`

```typescript
this.devices.includes(device)
```

### Resolved definition

- **Path:** `node_modules/typescript/lib/lib.es2016.array.include.d.ts`
- **Range:** line 24, col 4
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
    /**
     * Determines whether an array includes a certain element, returning true or false as appropriate.
     * @param searchElement The element to search for.
     * @param fromIndex The position in this array at which to begin searching for searchElement.
     */
    includes(searchElement: T, fromIndex?: number): boolean;
```

### Nested usages resolved

- `devices` → `packages/puppeteer-core/src/cdp/DeviceRequestPrompt.ts`

---

## 69. Sample 50 · callee #1

- **Function:** `select`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/DeviceRequestPrompt.ts`
- **Callee:** `client.off(...)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 180, col 18 — pattern `core_fallback`

```typescript
client.off(...)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/common/EventEmitter.ts`
- **Range:** line 104, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
   * Remove an event listener from firing.
   * @param type - the event type you'd like to stop listening to.
   * @param handler - the function that should be removed.
   * @returns `this` to enable you to chain method calls.
   */
  off<Key extends keyof EventsWithWildcard<Events>>(
    type: Key,
    handler?: Handler<EventsWithWildcard<Events>[Key]>,
  ): this {
    const handlers = this.#handlers.get(type) ?? [];
    if (handler === undefined) {
      for (const handler of handlers) {
        this.#emitter.off(type, handler);
      }
      this.#handlers.delete(type);
      return this;
    }
    const index = handlers.lastIndexOf(handler);
    if (index > -1) {
      this.#emitter.off(type, ...handlers.splice(index, 1));
    }
    return this;
  }
```

---

## 70. Sample 50 · callee #2

- **Function:** `select`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/DeviceRequestPrompt.ts`
- **Callee:** `client.send(...)`
- **Status:** OK
- **Also seen in:** 2 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 185, col 31 — pattern `core_fallback`

```typescript
client.send(...)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/bidi/CDPSession.ts`
- **Range:** line 66, col 17
- **Selection:** `all_implementations`

```typescript
  override async send<T extends keyof ProtocolMapping.Commands>(
    method: T,
    params?: ProtocolMapping.Commands[T]['paramsType'][0],
    options?: CommandOptions,
  ): Promise<ProtocolMapping.Commands[T]['returnType']> {
    if (this.#connection === undefined) {
      throw new UnsupportedOperation(
        'CDP support is required for this feature. The current browser does not support CDP.',
      );
    }
    if (this.#detached) {
      throw new TargetCloseError(
        `Protocol error (${method}): Session closed. Most likely the page has been closed.`,
      );
    }
    const session = await this.#sessionId.valueOrThrow();
    const {result} = await this.#connection.send(
      'goog:cdp.sendCommand',
      {
        method: method,
        params: params,
        session,
      },
      options?.timeout,
    );
    return result.result;
  }
```

### All implementations (2)

#### 1. `packages/puppeteer-core/src/bidi/CDPSession.ts`

```typescript
  override async send<T extends keyof ProtocolMapping.Commands>(
    method: T,
    params?: ProtocolMapping.Commands[T]['paramsType'][0],
    options?: CommandOptions,
  ): Promise<ProtocolMapping.Commands[T]['returnType']> {
    if (this.#connection === undefined) {
      throw new UnsupportedOperation(
        'CDP support is required for this feature. The current browser does not support CDP.',
      );
    }
    if (this.#detached) {
      throw new TargetCloseError(
        `Protocol error (${method}): Session closed. Most likely the page has been closed.`,
      );
    }
    const session = await this.#sessionId.valueOrThrow();
    const {result} = await this.#connection.send(
      'goog:cdp.sendCommand',
      {
        method: method,
        params: params,
        session,
      },
      options?.timeout,
    );
    return result.result;
  }
```

#### 2. `packages/puppeteer-core/src/cdp/CdpSession.ts`

```typescript
  override send<T extends keyof ProtocolMapping.Commands>(
    method: T,
    params?: ProtocolMapping.Commands[T]['paramsType'][0],
    options?: CommandOptions,
  ): Promise<ProtocolMapping.Commands[T]['returnType']> {
    if (this.detached) {
      return Promise.reject(
        new TargetCloseError(
          `Protocol error (${method}): Session closed. Most likely the ${this.#targetType} has been closed.`,
        ),
      );
    }
    return this.#connection._rawSend(
      this.#callbacks,
      method,
      params,
      this.#sessionId,
      options,
    );
  }
```

---

## 71. Sample 50 · callee #5

- **Function:** `select`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/DeviceRequestPrompt.ts`
- **Callee:** `this.devices`
- **Status:** OK

### Usage site (matched in test file)

Line 175, col 12 — pattern `anchor_substring`

```typescript
this.devices
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/cdp/DeviceRequestPrompt.ts`
- **Range:** line 75, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript

  /**
   * Current list of selectable devices.
   */
  devices: DeviceRequestPromptDevice[] = [];
```

---

## 72. Sample 51 · callee #0

- **Function:** `updateId`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/Frame.ts`
- **Callee:** `this._id`
- **Status:** OK

### Usage site (matched in test file)

Line 129, col 5 — pattern `anchor_substring`

```typescript
this._id
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/cdp/Frame.ts`
- **Range:** line 51, col 11
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript

  override _id: string;
```

---

## 73. Sample 52 · callee #0

- **Function:** `#onClientDisconnect`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/FrameManager.ts`
- **Callee:** `this._frameTree.getMainFrame()`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 102, col 23 — pattern `anchor_substring`

```typescript
this._frameTree.getMainFrame()
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/cdp/FrameTree.ts`
- **Range:** line 26, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  getMainFrame(): FrameType | undefined {
    return this.#mainFrame;
  }
```

---

## 74. Sample 52 · callee #1

- **Function:** `#onClientDisconnect`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/FrameManager.ts`
- **Callee:** `page.browser()`
- **Status:** OK

### Usage site (matched in test file)

Line 107, col 16 — pattern `anchor_substring`

```typescript
page.browser()
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/cdp/Page.ts`
- **Range:** line 454, col 11
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  override browser(): Browser {
    return this.#primaryTarget.browser();
  }
```

---

## 75. Sample 52 · callee #2

- **Function:** `#onClientDisconnect`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/FrameManager.ts`
- **Callee:** `removeFramesRecursively(mainFrame)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 110, col 13 — pattern `anchor_substring`

```typescript
removeFramesRecursively(mainFrame)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/cdp/FrameManager.ts`
- **Range:** line 562, col 3

```typescript
  #removeFramesRecursively(frame: CdpFrame): void {
    for (const child of frame.childFrames()) {
      this.#removeFramesRecursively(child);
    }
    frame[disposeSymbol]();
    this._frameTree.removeFrame(frame);
    this.emit(FrameManagerEvent.FrameDetached, frame);
    frame.emit(FrameEvent.FrameDetached, frame);
  }
```

---

## 76. Sample 52 · callee #4

- **Function:** `#onClientDisconnect`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/FrameManager.ts`
- **Callee:** `this._frameTree`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 102, col 23 — pattern `anchor_substring`

```typescript
this._frameTree
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/cdp/FrameManager.ts`
- **Range:** line 51, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
_frameTree = new FrameTree<CdpFrame>();
```

---

## 77. Sample 52 · callee #5

- **Function:** `#onClientDisconnect`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/FrameManager.ts`
- **Callee:** `Deferred.create`
- **Status:** OK
- **Also seen in:** 2 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 117, col 21 — pattern `anchor_substring`

```typescript
Deferred.create
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/util/Deferred.ts`
- **Range:** line 25, col 9
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  static create<R, X extends Error = Error>(
    opts?: DeferredOptions,
  ): Deferred<R, X> {
    return new Deferred<R, X>(opts);
  }
```

---

## 78. Sample 52 · callee #6

- **Function:** `#onClientDisconnect`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/FrameManager.ts`
- **Callee:** `FrameEvent.FrameSwappedByActivation`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 121, col 20 — pattern `anchor_substring`

```typescript
FrameEvent.FrameSwappedByActivation
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/api/Frame.ts`
- **Range:** line 203, col 15
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  export const FrameSwappedByActivation = Symbol(
```

---

## 79. Sample 53 · callee #1

- **Function:** `swapFrameTree`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/FrameManager.ts`
- **Callee:** `frameNavigatedReceived.add(this.#client.target()._targetId)`
- **Status:** OK

### Usage site (matched in test file)

Line 140, col 13 — pattern `anchor_substring`

```typescript
frameNavigatedReceived.add(this.#client.target()._targetId)
```

### Resolved definition

- **Path:** `node_modules/typescript/lib/lib.es2015.collection.d.ts`
- **Range:** line 92, col 4
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
    /**
     * Appends a new element with a specified value to the end of the Set.
     */
    add(value: T): this;
```

### Nested usages resolved

- `target` → `packages/puppeteer-core/src/cdp/CdpSession.ts`
- `target` → `packages/puppeteer-core/src/cdp/CdpSession.ts`

---

## 80. Sample 53 · callee #2

- **Function:** `swapFrameTree`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/FrameManager.ts`
- **Callee:** `this._frameTree.removeFrame(frame)`
- **Status:** OK

### Usage site (matched in test file)

Line 141, col 7 — pattern `anchor_substring`

```typescript
this._frameTree.removeFrame(frame)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/cdp/FrameTree.ts`
- **Range:** line 71, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  removeFrame(frame: FrameType): void {
    this.#frames.delete(frame._id);
    this.#parentIds.delete(frame._id);
    if (frame._parentId) {
      this.#childIds.get(frame._parentId)?.delete(frame._id);
    } else {
      this.#isMainFrameStale = true;
    }
  }
```

---

## 81. Sample 53 · callee #3

- **Function:** `swapFrameTree`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/FrameManager.ts`
- **Callee:** `this._frameTree.addFrame(frame)`
- **Status:** OK

### Usage site (matched in test file)

Line 143, col 7 — pattern `anchor_substring`

```typescript
this._frameTree.addFrame(frame)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/cdp/FrameTree.ts`
- **Range:** line 54, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  addFrame(frame: FrameType): void {
    this.#frames.set(frame._id, frame);
    if (frame._parentId) {
      this.#parentIds.set(frame._id, frame._parentId);
      if (!this.#childIds.has(frame._parentId)) {
        this.#childIds.set(frame._parentId, new Set());
      }
      this.#childIds.get(frame._parentId)!.add(frame._id);
    } else if (!this.#mainFrame || this.#isMainFrameStale) {
      this.#mainFrame = frame;
      this.#isMainFrameStale = false;
    }
    this.#waitRequests.get(frame._id)?.forEach(request => {
      return request.resolve(frame);
    });
  }
```

---

## 82. Sample 53 · callee #4

- **Function:** `swapFrameTree`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/FrameManager.ts`
- **Callee:** `this.setupEventListeners(client)`
- **Status:** OK

### Usage site (matched in test file)

Line 146, col 5 — pattern `anchor_substring`

```typescript
this.setupEventListeners(client)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/cdp/FrameManager.ts`
- **Range:** line 160, col 10
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  private setupEventListeners(session: CDPSession) {
    session.on('Page.frameAttached', async event => {
      await this.#frameTreeHandled?.valueOrThrow();
      this.#onFrameAttached(session, event.frameId, event.parentFrameId);
    });
    session.on('Page.frameNavigated', async event => {
      this.#frameNavigatedReceived.add(event.frame.id);
      await this.#frameTreeHandled?.valueOrThrow();
      void this.#onFrameNavigated(event.frame, event.type);
    });
    session.on('Page.navigatedWithinDocument', async event => {
      await this.#frameTreeHandled?.valueOrThrow();
      this.#onFrameNavigatedWithinDocument(event.frameId, event.url);
    });
    session.on(
      'Page.frameDetached',
      async (event: Protocol.Page.FrameDetachedEvent) => {
        await this.#frameTreeHandled?.valueOrThrow();
        this.#onFrameDetached(
          event.frameId,
          event.reason as Protocol.Page.FrameDetachedEventReason,
        );
      },
    );
    session.on('Page.frameStartedLoading', async event => {
      await this.#frameTreeHandled?.valueOrThrow();
      this.#onFrameStartedLoading(event.frameId);
    });
    session.on('Page.frameStoppedLoading', async event => {
      await this.#frameTreeHandled?.valueOrThrow();
      this.#onFrameStoppedLoading(event.frameId);
    });
    session.on('Runtime.executionContextCreated', async event => {
      await this.#frameTreeHandled?.valueOrThrow();
      this.#onExecutionContextCreated(event.context, session);
    });
    session.on('Page.lifecycleEvent', async event => {
      await this.#frameTreeHandled?.valueOrThrow();
      this.#onLifecycleEvent(event);
    });
  }
```

---

## 83. Sample 53 · callee #5

- **Function:** `swapFrameTree`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/FrameManager.ts`
- **Callee:** `this.initialize(client, frame)`
- **Status:** OK

### Usage site (matched in test file)

Line 150, col 11 — pattern `anchor_substring`

```typescript
this.initialize(client, frame)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/cdp/FrameManager.ts`
- **Range:** line 202, col 8
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  async initialize(client: CDPSession, frame?: CdpFrame | null): Promise<void> {
    try {
      this.#frameTreeHandled?.resolve();
      this.#frameTreeHandled = Deferred.create();
      // We need to schedule all these commands while the target is paused,
      // therefore, it needs to happen synchronously. At the same time we
      // should not start processing execution context and frame events before
      // we received the initial information about the frame tree.
      await Promise.all([
        this.#networkManager.addClient(client),
        client.send('Page.enable'),
        client.send('Page.getFrameTree').then(({frameTree}) => {
          this.#handleFrameTree(client, frameTree);
          this.#frameTreeHandled?.resolve();
        }),
        client.send('Page.setLifecycleEventsEnabled', {enabled: true}),
        client.send('Runtime.enable').then(() => {
          return this.#createIsolatedWorld(client, UTILITY_WORLD_NAME);
        }),
        ...(frame
          ? Array.from(this.#scriptsToEvaluateOnNewDocument.values())
          : []
        ).map(script => {
          return frame?.addPreloadScript(script);
        }),
        ...(frame ? Array.from(this.#bindings.values()) : []).map(binding => {
          return frame?.addExposedFunctionBinding(binding);
        }),
      ]);
    } catch (error) {
      this.#frameTreeHandled?.resolve();
      // The target might have been closed before the initialization finished.
      if (isErrorLike(error) && isTargetClosedError(error)) {
        return;
      }

      throw error;
    }
  }
```

---

## 84. Sample 53 · callee #6

- **Function:** `swapFrameTree`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/FrameManager.ts`
- **Callee:** `networkManager.addClient(client)`
- **Status:** OK

### Usage site (matched in test file)

Line 151, col 17 — pattern `anchor_substring`

```typescript
networkManager.addClient(client)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/cdp/NetworkManager.ts`
- **Range:** line 94, col 8
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  async addClient(client: CDPSession): Promise<void> {
    if (this.#clients.has(client)) {
      return;
    }
    const subscriptions = new DisposableStack();
    this.#clients.set(client, subscriptions);
    const clientEmitter = subscriptions.use(new EventEmitter(client));

    for (const [event, handler] of this.#handlers) {
      clientEmitter.on(event, (arg: any) => {
        return handler.bind(this)(client, arg);
      });
    }

    await Promise.all([
      client.send('Network.enable'),
      this.#applyExtraHTTPHeaders(client),
      this.#applyNetworkConditions(client),
      this.#applyProtocolCacheDisabled(client),
      this.#applyProtocolRequestInterception(client),
      this.#applyUserAgent(client),
    ]);
  }
```

---

## 85. Sample 53 · callee #7

- **Function:** `swapFrameTree`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/FrameManager.ts`
- **Callee:** `onClientDisconnect()`
- **Status:** OK

### Usage site (matched in test file)

Line 148, col 13 — pattern `anchor_substring`

```typescript
onClientDisconnect()
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/cdp/FrameManager.ts`
- **Range:** line 93, col 3

```typescript
      this.#onClientDisconnect().catch(debugError);
```

---

## 86. Sample 53 · callee #9

- **Function:** `swapFrameTree`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/FrameManager.ts`
- **Callee:** `CDPSessionEvent.Disconnected`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 147, col 17 — pattern `anchor_substring`

```typescript
CDPSessionEvent.Disconnected
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/api/CDPSession.ts`
- **Range:** line 25, col 15
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/** @internal */
  export const Disconnected = Symbol('CDPSession.Disconnected');
```

---

## 87. Sample 54 · callee #0

- **Function:** `waitForFrame`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/FrameTree.ts`
- **Callee:** `this.getById(frameId)`
- **Status:** OK

### Usage site (matched in test file)

Line 40, col 19 — pattern `anchor_substring`

```typescript
this.getById(frameId)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/cdp/FrameTree.ts`
- **Range:** line 30, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  getById(frameId: string): FrameType | undefined {
    return this.#frames.get(frameId);
  }
```

---

## 88. Sample 54 · callee #2

- **Function:** `waitForFrame`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/FrameTree.ts`
- **Callee:** `waitRequests.get(frameId)`
- **Status:** OK
- **Also seen in:** 2 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 46, col 13 — pattern `anchor_substring`

```typescript
waitRequests.get(frameId)
```

### Resolved definition

- **Path:** `node_modules/typescript/lib/lib.es2015.collection.d.ts`
- **Range:** line 32, col 4
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
    /**
     * Returns a specified element from the Map object. If the value that is associated to the provided key is an object, then you will get a reference to that object and any change made to that object will effectively modify it inside the Map.
     * @returns Returns the element associated with the specified key. If no element is associated with the specified key, undefined is returned.
     */
    get(key: K): V | undefined;
```

---

## 89. Sample 55 · callee #0

- **Function:** `#waitForExecutionContext`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/IsolatedWorld.ts`
- **Callee:** `this.timeoutSettings.timeout()`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 150, col 19 — pattern `anchor_substring`

```typescript
this.timeoutSettings.timeout()
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/common/TimeoutSettings.ts`
- **Range:** line 38, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  timeout(): number {
    if (this.#defaultTimeout !== null) {
      return this.#defaultTimeout;
    }
    return DEFAULT_TIMEOUT;
  }
```

---

## 90. Sample 55 · callee #3

- **Function:** `#waitForExecutionContext`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/IsolatedWorld.ts`
- **Callee:** `fromEmitterEvent(this.#emitter, 'context')`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 142, col 7 — pattern `anchor_substring`

```typescript
fromEmitterEvent(this.#emitter, 'context')
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/common/util.ts`
- **Range:** line 428, col 16
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
 * @internal
 */
export function fromEmitterEvent<
  Events extends Record<EventType, unknown>,
  Event extends keyof Events,
>(emitter: EventEmitter<Events>, eventName: Event): Observable<Events[Event]> {
  return new Observable(subscriber => {
    const listener = (event: Events[Event]) => {
      subscriber.next(event);
    };
    emitter.on(eventName, listener);
    return () => {
      emitter.off(eventName, listener);
    };
  });
}
```

---

## 91. Sample 55 · callee #4

- **Function:** `#waitForExecutionContext`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/IsolatedWorld.ts`
- **Callee:** `raceWith(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 143, col 9 — pattern `core_fallback`

```typescript
raceWith(...)
```

### Resolved definition

- **Path:** `node_modules/rxjs/dist/types/internal/operators/raceWith.d.ts`
- **Range:** line 0, col 66
- **Selection:** `external_runtime_resolution_after_ts_nav`

```typescript
/**
 * Creates an Observable that mirrors the first source Observable to emit a next,
 * error or complete notification from the combination of the Observable to which
 * the operator is applied and supplied Observables.
 *
 * ## Example
 *
 * ```ts
 * import { interval, map, raceWith } from 'rxjs';
 *
 * const obs1 = interval(7000).pipe(map(() => 'slow one'));
 * const obs2 = interval(3000).pipe(map(() => 'fast one'));
 * const obs3 = interval(5000).pipe(map(() => 'medium one'));
 *
 * obs1
 *   .pipe(raceWith(obs2, obs3))
 *   .subscribe(winner => console.log(winner));
```

### Runtime implementation

- **Body:** `node_modules/rxjs/src/internal/operators/raceWith.ts`
- **Range:** line 31, col 0

```typescript
/**
 * Creates an Observable that mirrors the first source Observable to emit a next,
 * error or complete notification from the combination of the Observable to which
 * the operator is applied and supplied Observables.
 *
 * ## Example
 *
 * ```ts
 * import { interval, map, raceWith } from 'rxjs';
 *
 * const obs1 = interval(7000).pipe(map(() => 'slow one'));
 * const obs2 = interval(3000).pipe(map(() => 'fast one'));
 * const obs3 = interval(5000).pipe(map(() => 'medium one'));
 *
 * obs1
 *   .pipe(raceWith(obs2, obs3))
 *   .subscribe(winner => console.log(winner));
 *
 * // Outputs
 * // a series of 'fast one'
 * ```
 *
 * @param otherSources Sources used to race for which Observable emits first.
 * @return A function that returns an Observable that mirrors the output of the
 * first Observable to emit an item.
 */
export function raceWith<T, A extends readonly unknown[]>(
  ...otherSources: [...ObservableInputTuple<A>]
): OperatorFunction<T, T | A[number]> {
  return !otherSources.length
    ? identity
    : operate((source, subscriber) => {
        raceInit<T | A[number]>([source, ...otherSources])(subscriber);
      });
}
```

---

## 92. Sample 55 · callee #6

- **Function:** `#waitForExecutionContext`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/IsolatedWorld.ts`
- **Callee:** `map(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 145, col 13 — pattern `core_fallback`

```typescript
map(...)
```

### Resolved definition

- **Path:** `node_modules/rxjs/src/internal/operators/map.ts`
- **Range:** line 4, col 16
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript

export function map<T, R>(project: (value: T, index: number) => R): OperatorFunction<T, R>;
```

---

## 93. Sample 55 · callee #8

- **Function:** `#waitForExecutionContext`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/IsolatedWorld.ts`
- **Callee:** `this.timeoutSettings`
- **Status:** OK

### Usage site (matched in test file)

Line 150, col 19 — pattern `anchor_substring`

```typescript
this.timeoutSettings
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/api/Realm.ts`
- **Range:** line 23, col 21
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  protected readonly timeoutSettings: TimeoutSettings;
```

---

## 94. Sample 57 · callee #0

- **Function:** `#setupPrimaryTargetListeners`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/Page.ts`
- **Callee:** `sessionCloseDeferred.reject(new TargetCloseError('Target closed'))`
- **Status:** OK

### Usage site (matched in test file)

Line 297, col 13 — pattern `anchor_substring`

```typescript
sessionCloseDeferred.reject(new TargetCloseError('Target closed'))
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/util/Deferred.ts`
- **Range:** line 94, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  reject(error: V | TimeoutError): void {
    if (this.#isRejected || this.#isResolved) {
      return;
    }
    this.#isRejected = true;
    this.#finish(error);
  }
```

---

## 95. Sample 57 · callee #1

- **Function:** `#setupPrimaryTargetListeners`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/Page.ts`
- **Callee:** `this.emit(PageEvent.DOMContentLoaded, undefined)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 300, col 7 — pattern `anchor_substring`

```typescript
this.emit(PageEvent.DOMContentLoaded, undefined)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/common/EventEmitter.ts`
- **Range:** line 130, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
   * Emit an event and call any associated listeners.
   *
   * @param type - the event you'd like to emit
   * @param eventData - any data you'd like to emit with the event
   * @returns `true` if there are any listeners, `false` if there are not.
   */
  emit<Key extends keyof EventsWithWildcard<Events>>(
    type: Key,
    event: EventsWithWildcard<Events>[Key],
  ): boolean {
    this.#emitter.emit(type, event);
    return this.listenerCount(type) > 0;
  }
```

---

## 96. Sample 57 · callee #3

- **Function:** `#setupPrimaryTargetListeners`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/Page.ts`
- **Callee:** `onDialog.bind(this)`
- **Status:** OK
- **Also seen in:** 5 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 305, col 60 — pattern `anchor_substring`

```typescript
onDialog.bind(this)
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es5.d.ts`
- **Range:** line 347, col 93

```typescript
/**
     * For a given function, creates a bound function that has the same body as the original function.
     * The this object of the bound function is associated with the specified object, and has the specified initial parameters.
     * @param thisArg The object to be used as the this object.
     */
    bind<T>(this: T, thisArg: ThisParameterType<T>): OmitThisParameter<T>;
```

---

## 97. Sample 57 · callee #9

- **Function:** `#setupPrimaryTargetListeners`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/Page.ts`
- **Callee:** `EventEmitter(this.#primaryTargetClient)`
- **Status:** OK

### Usage site (matched in test file)

Line 294, col 31 — pattern `anchor_substring`

```typescript
EventEmitter(this.#primaryTargetClient)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/common/EventEmitter.ts`
- **Range:** line 44, col 4

```typescript
/**
 * The EventEmitter class that many Puppeteer classes extend.
 *
 * @remarks
 *
 * This allows you to listen to events that Puppeteer classes fire and act
 * accordingly. Therefore you'll mostly use {@link EventEmitter.on | on} and
 * {@link EventEmitter.off | off} to bind
 * and unbind to event listeners.
 *
 * @public
 */
export class EventEmitter<Events extends Record<EventType, unknown>>
  implements CommonEventEmitter<EventsWithWildcard<Events>>
{
  #emitter: Emitter<EventsWithWildcard<Events>> | EventEmitter<Events>;
  #handlers = new Map<keyof Events | '*', Array<Handler<any>>>();

  /**
   * If you pass an emitter, the returned emitter will wrap the passed emitter.
   *
   * @internal
   */
  constructor(
    emitter: Emitter<EventsWithWildcard<Events>> | EventEmitter<Events> = mitt(
      new Map(),
    ),
  ) {
    this.#emitter = emitter;
  }

  /**
   * Bind an event listener to fire when an event occurs.
   * @param type - the event type you'd like to listen to. Can be a string or symbol.
   * @param handler - the function to be called when the event occurs.
   * @returns `this` to enable you to chain method calls.
   */
  on<Key extends keyof EventsWithWildcard<Events>>(
    type: Key,
    handler: Handler<EventsWithWildcard<Events>[Key]>,
  ): this {
    const handlers = this.#handlers.get(type);
    if (handlers === undefined) {
      this.#handlers.set(type, [handler]);
    } else {
      handlers.push(handler);
    }

    this.#emitter.on(type, handler);
    return this;
  }

  /**
   * Remove an event listener from firing.
   * @param type - the event type you'd like to stop listening to.
   * @param handler - the function that should be removed.
   * @returns `this` to enable you to chain method calls.
   */
  off<Key extends keyof EventsWithWildcard<Events>>(
    type: Key,
    handler?: Handler<EventsWithWildcard<Events>[Key]>,
  ): this {
    const handlers = this.#handlers.get(type) ?? [];
    if (handler === undefined) {
      for (const handler of handlers) {
        this.#emitter.off(type, handler);
      }
      this.#handlers.delete(type);
      return this;
    }
    const index = handlers.lastIndexOf(handler);
    if (index > -1) {
      this.#emitter.off(type, ...handlers.splice(index, 1));
    }
    return this;
  }

  /**
   * Emit an event and call any associated listeners.
   *
   * @param type - the event you'd like to emit
   * @param eventData - any data you'd like to emit with the event
   * @returns `true` if there are any listeners, `false` if there are not.
   */
  emit<Key extends keyof EventsWithWildcard<Events>>(
    type: Key,
    event: EventsWithWildcard<Events>[Key],
  ): boolean {
    this.#emitter.emit(type, event);
    return this.listenerCount(type) > 0;
  }

  /**
   * Like `on` but the listener will only be fired once and then it will be removed.
   * @param type - the event you'd like to listen to
   * @param handler - the handler function to run when the event occurs
   * @returns `this` to enable you to chain method calls.
   */
  once<Key extends keyof EventsWithWildcard<Events>>(
    type: Key,
    handler: Handler<EventsWithWildcard<Events>[Key]>,
  ): this {
    const onceHandler: Handler<EventsWithWildcard<Events>[Key]> = eventData => {
      handler(eventData);
      this.off(type, onceHandler);
    };

    return this.on(type, onceHandler);
  }

  /**
   * Gets the number of listeners for a given event.
   *
   * @param type - the event to get the listener count for
   * @returns the number of listeners bound to the given event
   */
  listenerCount(type: keyof EventsWithWildcard<Events>): number {
    return this.#handlers.get(type)?.length || 0;
  }

  /**
   * Removes all listeners. If given an event argument, it will remove only
   * listeners for that event.
   *
   * @param type - the event to remove listeners for.
   * @returns `this` to enable you to chain method calls.
   */
  removeAllListeners(type?: keyof EventsWithWildcard<Events>): this {
    if (type !== undefined) {
      return this.off(type);
    }
    this[disposeSymbol]();
    return this;
  }

  /**
   * @internal
   */
  [disposeSymbol](): void {
    for (const [type, handlers] of this.#handlers) {
      for (const handler of handlers) {
        this.#emitter.off(type, handler);
      }
    }
    this.#handlers.clear();
  }
}
```

---

## 98. Sample 57 · callee #10

- **Function:** `#setupPrimaryTargetListeners`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/Page.ts`
- **Callee:** `TargetCloseError('Target closed')`
- **Status:** OK

### Usage site (matched in test file)

Line 297, col 45 — pattern `anchor_substring`

```typescript
TargetCloseError('Target closed')
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/common/Errors.ts`
- **Range:** line 15, col 2
- **Selection:** `preferred_implementation_over_declaration_kept=2`

```typescript
/**
 * @internal
 */
export class TargetCloseError extends ProtocolError {}
```

---

## 99. Sample 57 · callee #11

- **Function:** `#setupPrimaryTargetListeners`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/Page.ts`
- **Callee:** `CDPSessionEvent.Ready`
- **Status:** OK

### Usage site (matched in test file)

Line 295, col 22 — pattern `anchor_substring`

```typescript
CDPSessionEvent.Ready
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/api/CDPSession.ts`
- **Range:** line 34, col 15
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
   * Emitted when the session is ready to be configured during the auto-attach
   * process. Right after the event is handled, the session will be resumed.
   *
   * @internal
   */
  export const Ready = Symbol('CDPSession.Ready');
```

---

## 100. Sample 57 · callee #13

- **Function:** `#setupPrimaryTargetListeners`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/Page.ts`
- **Callee:** `PageEvent.DOMContentLoaded`
- **Status:** OK

### Usage site (matched in test file)

Line 300, col 17 — pattern `anchor_substring`

```typescript
PageEvent.DOMContentLoaded
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/api/Page.ts`
- **Range:** line 474, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
DOMContentLoaded = 'domcontentloaded',
```

---

## 101. Sample 57 · callee #14

- **Function:** `#setupPrimaryTargetListeners`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/Page.ts`
- **Callee:** `PageEvent.Load`
- **Status:** OK

### Usage site (matched in test file)

Line 303, col 17 — pattern `anchor_substring`

```typescript
PageEvent.Load
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/api/Page.ts`
- **Range:** line 493, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
Load = 'load',
```

---

## 102. Sample 58 · callee #0

- **Function:** `start`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/Tracing.ts`
- **Callee:** `categories.push('disabled-by-default-devtools.screenshot')`
- **Status:** OK
- **Also seen in:** 6 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 88, col 7 — pattern `anchor_substring`

```typescript
categories.push('disabled-by-default-devtools.screenshot')
```

### Resolved definition

- **Path:** `node_modules/typescript/lib/lib.es5.d.ts`
- **Range:** line 1343, col 4
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
    /**
     * Appends new elements to the end of an array, and returns the new length of the array.
     * @param items New elements to add to the array.
     */
    push(...items: T[]): number;
```

---

## 103. Sample 58 · callee #1

- **Function:** `start`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/Tracing.ts`
- **Callee:** `cat.startsWith('-')`
- **Status:** OK

### Usage site (matched in test file)

Line 93, col 16 — pattern `anchor_substring`

```typescript
cat.startsWith('-')
```

### Resolved definition

- **Path:** `node_modules/typescript/lib/lib.es2015.core.d.ts`
- **Range:** line 455, col 4
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript

    /**
     * Returns true if the sequence of elements of searchString converted to a String is the
     * same as the corresponding elements of this object (converted to a String) starting at
     * position. Otherwise returns false.
     */
    startsWith(searchString: string, position?: number): boolean;
```

---

## 104. Sample 58 · callee #2

- **Function:** `start`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/Tracing.ts`
- **Callee:** `cat.slice(1)`
- **Status:** OK

### Usage site (matched in test file)

Line 96, col 16 — pattern `anchor_substring`

```typescript
cat.slice(1)
```

### Resolved definition

- **Path:** `node_modules/typescript/lib/lib.es5.d.ts`
- **Range:** line 483, col 4
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript

    /**
     * Returns a section of a string.
     * @param start The index to the beginning of the specified portion of stringObj.
     * @param end The index to the end of the specified portion of stringObj. The substring includes the characters up to, but not including, the character indicated by end.
     * If this value is not specified, the substring continues to the end of stringObj.
     */
    slice(start?: number, end?: number): string;
```

---

## 105. Sample 58 · callee #3

- **Function:** `start`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/Tracing.ts`
- **Callee:** `categories.filter(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 92, col 8 — pattern `core_fallback`

```typescript
categories.filter(...)
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es5.d.ts`
- **Range:** line 1467, col 87

```typescript
/**
     * Returns the elements of an array that meet the condition specified in a callback function.
     * @param predicate A function that accepts up to three arguments. The filter method calls the predicate function one time for each element in the array.
     * @param thisArg An object to which the this keyword can refer in the predicate function. If thisArg is omitted, undefined is used as the this value.
     */
    filter<S extends T>(predicate: (value: T, index: number, array: T[]) => value is S, thisArg?: any): S[];
```

---

## 106. Sample 59 · callee #0

- **Function:** `stop`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/Tracing.ts`
- **Callee:** `client.once(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 119, col 18 — pattern `core_fallback`

```typescript
client.once(...)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/common/EventEmitter.ts`
- **Range:** line 144, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
   * Like `on` but the listener will only be fired once and then it will be removed.
   * @param type - the event you'd like to listen to
   * @param handler - the handler function to run when the event occurs
   * @returns `this` to enable you to chain method calls.
   */
  once<Key extends keyof EventsWithWildcard<Events>>(
    type: Key,
    handler: Handler<EventsWithWildcard<Events>[Key]>,
  ): this {
    const onceHandler: Handler<EventsWithWildcard<Events>[Key]> = eventData => {
      handler(eventData);
      this.off(type, onceHandler);
    };

    return this.on(type, onceHandler);
  }
```

---

## 107. Sample 59 · callee #3

- **Function:** `stop`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/Tracing.ts`
- **Callee:** `getReadableFromProtocolStream(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 122, col 32 — pattern `core_fallback`

```typescript
getReadableFromProtocolStream(...)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/common/util.ts`
- **Range:** line 244, col 22
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
 * @internal
 */

/**
 * @internal
 */
export async function getReadableFromProtocolStream(
  client: CDPSession,
  handle: string,
): Promise<ReadableStream<Uint8Array>> {
  return new ReadableStream({
    async pull(controller) {
      const {data, base64Encoded, eof} = await client.send('IO.read', {
        handle,
      });

      controller.enqueue(stringToTypedArray(data, base64Encoded ?? false));
      if (eof) {
        await client.send('IO.close', {handle});
        controller.close();
      }
    },
  });
}
```

---

## 108. Sample 59 · callee #4

- **Function:** `stop`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/Tracing.ts`
- **Callee:** `getReadableAsTypedArray(readable, this.#path)`
- **Status:** OK

### Usage site (matched in test file)

Line 126, col 34 — pattern `anchor_substring`

```typescript
getReadableAsTypedArray(readable, this.#path)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/common/util.ts`
- **Range:** line 196, col 22
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
 * @internal
 */
export async function getReadableAsTypedArray(
  readable: ReadableStream<Uint8Array>,
  path?: string,
): Promise<Uint8Array | null> {
  const buffers: Uint8Array[] = [];
  const reader = readable.getReader();
  if (path) {
    const fileHandle = await environment.value.fs.promises.open(path, 'w+');
    try {
      while (true) {
        const {done, value} = await reader.read();
        if (done) {
          break;
        }
        buffers.push(value);
        await fileHandle.writeFile(value);
      }
    } finally {
      await fileHandle.close();
    }
  } else {
    while (true) {
      const {done, value} = await reader.read();
      if (done) {
        break;
      }
      buffers.push(value);
    }
  }
  try {
    const concat = mergeUint8Arrays(buffers);
    if (concat.length === 0) {
      return null;
    }
    return concat;
  } catch (error) {
    debugError(error);
    return null;
  }
}
```

---

## 109. Sample 59 · callee #5

- **Function:** `stop`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/Tracing.ts`
- **Callee:** `isErrorLike(error)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 129, col 13 — pattern `anchor_substring`

```typescript
isErrorLike(error)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/util/ErrorLike.ts`
- **Range:** line 19, col 16
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
 * @internal
 */
export function isErrorLike(obj: unknown): obj is ErrorLike {
  return (
    typeof obj === 'object' && obj !== null && 'name' in obj && 'message' in obj
  );
}
```

---

## 110. Sample 59 · callee #8

- **Function:** `stop`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/cdp/Tracing.ts`
- **Callee:** `event.stream`
- **Status:** OK

### Usage site (matched in test file)

Line 121, col 16 — pattern `anchor_substring`

```typescript
event.stream
```

### Resolved definition

- **Path:** `packages/puppeteer-core/node_modules/devtools-protocol/types/protocol.d.ts`
- **Range:** line 18204, col 12
- **Selection:** `fast_path_refined_via_document_symbols`

```typescript
/**
             * A handle of the stream that holds resulting trace data.
             */
            stream?: IO.StreamHandle;
```

---

## 111. Sample 63 · callee #0

- **Function:** `location`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/common/ConsoleMessage.ts`
- **Callee:** `frame.url()`
- **Status:** OK

### Usage site (matched in test file)

Line 110, col 34 — pattern `anchor_substring`

```typescript
frame.url()
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/bidi/Frame.ts`
- **Range:** line 279, col 11
- **Selection:** `all_implementations`

```typescript
  override url(): string {
    return this.browsingContext.url;
  }
```

### All implementations (2)

#### 1. `packages/puppeteer-core/src/bidi/Frame.ts`

```typescript
  override url(): string {
    return this.browsingContext.url;
  }
```

#### 2. `packages/puppeteer-core/src/cdp/Frame.ts`

```typescript
  override url(): string {
    return this.#url;
  }
```

---

## 112. Sample 64 · callee #0

- **Function:** `register`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/common/CustomQueryHandler.ts`
- **Callee:** `handlers.has(name)`
- **Status:** OK

### Usage site (matched in test file)

Line 76, col 14 — pattern `anchor_substring`

```typescript
handlers.has(name)
```

### Resolved definition

- **Path:** `node_modules/typescript/lib/lib.es2015.collection.d.ts`
- **Range:** line 36, col 4
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
    /**
     * @returns boolean indicating whether an element with the specified key exists or not.
     */
    has(key: K): boolean;
```

---

## 113. Sample 64 · callee #2

- **Function:** `register`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/common/CustomQueryHandler.ts`
- **Callee:** `handlers.set(name, [registerScript, Handler])`
- **Status:** OK

### Usage site (matched in test file)

Line 124, col 11 — pattern `anchor_substring`

```typescript
handlers.set(name, [registerScript, Handler])
```

### Resolved definition

- **Path:** `node_modules/typescript/lib/lib.es2015.collection.d.ts`
- **Range:** line 40, col 4
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
    /**
     * Adds a new element with a specified key and value to the Map. If an element with the same key already exists, the element will be updated.
     */
    set(key: K, value: V): this;
```

---

## 114. Sample 64 · callee #3

- **Function:** `register`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/common/CustomQueryHandler.ts`
- **Callee:** `scriptInjector.append(registerScript)`
- **Status:** OK

### Usage site (matched in test file)

Line 125, col 5 — pattern `anchor_substring`

```typescript
scriptInjector.append(registerScript)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/common/ScriptInjector.ts`
- **Range:** line 12, col 34

```typescript
// Appends a statement of the form `(PuppeteerUtil) => {...}`.
  append(statement: string): void {
    this.#update(() => {
      this.#amendments.add(statement);
    });
  }
```

---

## 115. Sample 64 · callee #5

- **Function:** `register`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/common/CustomQueryHandler.ts`
- **Callee:** `interpolateFunction(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 89, col 60 — pattern `core_fallback`

```typescript
interpolateFunction(...)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/util/Function.ts`
- **Range:** line 75, col 12

```typescript
/**
 * Replaces `PLACEHOLDER`s with the given replacements.
 *
 * All replacements must be valid JS code.
 *
 * @example
 *
 * ```ts
 * interpolateFunction(() => PLACEHOLDER('test'), {test: 'void 0'});
 * // Equivalent to () => void 0
 * ```
 *
 * @internal
 */
export const interpolateFunction = <T extends (...args: never[]) => unknown>(
  fn: T,
  replacements: Record<string, string>,
): T => {
  let value = stringifyFunction(fn);
  for (const [name, jsValue] of Object.entries(replacements)) {
    value = value.replace(
      new RegExp(`PLACEHOLDER\\(\\s*(?:'${name}'|"${name}")\\s*\\)`, 'g'),
      // Wrapping this ensures tersers that accidentally inline PLACEHOLDER calls
      // are still valid. Without, we may get calls like ()=>{...}() which is
      // not valid.
      `(${jsValue})`,
    );
  }
  return createFunction(value) as unknown as T;
};
```

---

## 116. Sample 64 · callee #6

- **Function:** `register`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/common/CustomQueryHandler.ts`
- **Callee:** `PLACEHOLDER('name')`
- **Status:** OK
- **Also seen in:** 2 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 92, col 18 — pattern `anchor_substring`

```typescript
PLACEHOLDER('name')
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/util/Function.ts`
- **Range:** line 92, col 16

```typescript
/**
   * Used for interpolation with {@link interpolateFunction}.
   *
   * @internal
   */
  function PLACEHOLDER<T>(name: string): T;
```

---

## 117. Sample 64 · callee #9

- **Function:** `register`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/common/CustomQueryHandler.ts`
- **Callee:** `stringifyFunction(handler.queryAll)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 116, col 13 — pattern `anchor_substring`

```typescript
stringifyFunction(handler.queryAll)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/util/Function.ts`
- **Range:** line 29, col 16
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
 * @internal
 */
export function stringifyFunction(fn: (...args: never) => unknown): string {
  let value = fn.toString();
  try {
    new Function(`(${value})`);
  } catch (err) {
    if (
      (err as Error).message.includes(
        `Refused to evaluate a string as JavaScript because 'unsafe-eval' is not an allowed source of script in the following Content Security Policy directive`,
      )
    ) {
      // The content security policy does not allow Function eval. Let's
      // assume the value might be valid as is.
      return value;
    }
    // This means we might have a function shorthand (e.g. `test(){}`). Let's
    // try prefixing.
    let prefix = 'function ';
    if (value.startsWith('async ')) {
      prefix = `async ${prefix}`;
      value = value.substring('async '.length);
    }
    value = `${prefix}${value}`;
    try {
      new Function(`(${value})`);
    } catch {
      // We tried hard to serialize, but there's a weird beast here.
      throw new Error('Passed function cannot be serialized!');
    }
  }
  return value;
}
```

---

## 118. Sample 64 · callee #10

- **Function:** `register`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/common/CustomQueryHandler.ts`
- **Callee:** `String(undefined)`
- **Status:** OK

### Usage site (matched in test file)

Line 117, col 13 — pattern `anchor_substring`

```typescript
String(undefined)
```

### Resolved definition

- **Path:** `node_modules/@types/node/compatibility/indexable.d.ts`
- **Range:** line 7, col 1

```typescript
interface String extends RelativeIndexable<string> {}
```

---

## 119. Sample 65 · callee #1

- **Function:** `unregister`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/common/CustomQueryHandler.ts`
- **Callee:** `scriptInjector.pop(handler[0])`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 139, col 5 — pattern `anchor_substring`

```typescript
scriptInjector.pop(handler[0])
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/common/ScriptInjector.ts`
- **Range:** line 21, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  pop(statement: string): void {
    this.#update(() => {
      this.#amendments.delete(statement);
    });
  }
```

---

## 120. Sample 65 · callee #2

- **Function:** `unregister`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/common/CustomQueryHandler.ts`
- **Callee:** `handlers.delete(name)`
- **Status:** OK

### Usage site (matched in test file)

Line 140, col 11 — pattern `anchor_substring`

```typescript
handlers.delete(name)
```

### Resolved definition

- **Path:** `node_modules/typescript/lib/lib.es2015.collection.d.ts`
- **Range:** line 23, col 4
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
    /**
     * @returns true if an element in the Map existed and has been removed, or false if the element does not exist.
     */
    delete(key: K): boolean;
```

---

## 121. Sample 66 · callee #0

- **Function:** `names`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/common/CustomQueryHandler.ts`
- **Callee:** `handlers.keys()`
- **Status:** OK

### Usage site (matched in test file)

Line 147, col 22 — pattern `anchor_substring`

```typescript
handlers.keys()
```

### Resolved definition

- **Path:** `node_modules/typescript/lib/lib.es2015.iterable.d.ts`
- **Range:** line 152, col 4
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript

    /**
     * Returns an iterable of keys in the map
     */
    keys(): MapIterator<K>;
```

---

## 122. Sample 67 · callee #1

- **Function:** `clear`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/common/CustomQueryHandler.ts`
- **Callee:** `handlers.clear()`
- **Status:** OK

### Usage site (matched in test file)

Line 157, col 11 — pattern `anchor_substring`

```typescript
handlers.clear()
```

### Resolved definition

- **Path:** `node_modules/typescript/lib/lib.es2015.collection.d.ts`
- **Range:** line 19, col 4
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
    clear(): void;
```

---

## 123. Sample 71 · callee #0

- **Function:** `accept`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/common/FileChooser.ts`
- **Callee:** `element.uploadFile(...paths)`
- **Status:** OK

### Usage site (matched in test file)

Line 69, col 17 — pattern `anchor_substring`

```typescript
element.uploadFile(...paths)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/bidi/ElementHandle.ts`
- **Range:** line 99, col 3
- **Selection:** `all_implementations`

```typescript
  override async uploadFile(
    this: BidiElementHandle<HTMLInputElement>,
    ...files: string[]
  ): Promise<void> {
    // Locate all files and confirm that they exist.
    const path = environment.value.path;
    if (path) {
      files = files.map(file => {
        if (path.win32.isAbsolute(file) || path.posix.isAbsolute(file)) {
          return file;
        } else {
          return path.resolve(file);
        }
      });
    }
    await this.frame.setFiles(this, files);
  }
```

### All implementations (2)

#### 1. `packages/puppeteer-core/src/bidi/ElementHandle.ts`

```typescript
  override async uploadFile(
    this: BidiElementHandle<HTMLInputElement>,
    ...files: string[]
  ): Promise<void> {
    // Locate all files and confirm that they exist.
    const path = environment.value.path;
    if (path) {
      files = files.map(file => {
        if (path.win32.isAbsolute(file) || path.posix.isAbsolute(file)) {
          return file;
        } else {
          return path.resolve(file);
        }
      });
    }
    await this.frame.setFiles(this, files);
  }
```

#### 2. `packages/puppeteer-core/src/cdp/ElementHandle.ts`

```typescript
  override async uploadFile(
    this: CdpElementHandle<HTMLInputElement>,
    ...files: string[]
  ): Promise<void> {
    const isMultiple = await this.evaluate(element => {
      return element.multiple;
    });
    assert(
      files.length <= 1 || isMultiple,
      'Multiple file uploads only work with <input type=file multiple>',
    );

    // Locate all files and confirm that they exist.
    const path = environment.value.path;
    if (path) {
      files = files.map(filePath => {
        if (
          path.win32.isAbsolute(filePath) ||
          path.posix.isAbsolute(filePath)
        ) {
          return filePath;
        } else {
          return path.resolve(filePath);
        }
      });
    }

    /**
     * The zero-length array is a special case, it seems that
     * DOM.setFileInputFiles does not actually update the files in that case, so
     * the solution is to eval the element value to a new FileList directly.
     */
    if (files.length === 0) {
      // XXX: These events should converted to trusted events. Perhaps do this
      // in `DOM.setFileInputFiles`?
      await this.evaluate(element => {
        element.files = new DataTransfer().files;

        // Dispatch events for this case because it should behave akin to a user action.
        element.dispatchEvent(
          new Event('input', {bubbles: true, composed: true}),
        );
        element.dispatchEvent(new Event('change', {bubbles: true}));
      });
      return;
    }

    const {
      node: {backendNodeId},
    } = await this.client.send('DOM.describeNode', {
      objectId: this.id,
    });
    await this.client.send('DOM.setFileInputFiles', {
      objectId: this.id,
      files,
      backendNodeId,
    });
  }
```

---

## 124. Sample 72 · callee #0

- **Function:** `cancel`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/common/FileChooser.ts`
- **Callee:** `element.evaluate(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 83, col 25 — pattern `core_fallback`

```typescript
element.evaluate(...)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/api/ElementHandle.ts`
- **Range:** line 270, col 17
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
   * @internal
   */
  override async evaluate<
    Params extends unknown[],
    Func extends EvaluateFuncWith<ElementType, Params> = EvaluateFuncWith<
      ElementType,
      Params
    >,
  >(
    pageFunction: Func | string,
    ...args: Params
  ): Promise<Awaited<ReturnType<Func>>> {
    pageFunction = withSourcePuppeteerURLIfNone(
      this.evaluate.name,
      pageFunction,
    );
    return await this.handle.evaluate(pageFunction, ...args);
  }
```

---

## 125. Sample 72 · callee #1

- **Function:** `cancel`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/common/FileChooser.ts`
- **Callee:** `element.dispatchEvent(new Event('cancel', {bubbles: true}))`
- **Status:** OK

### Usage site (matched in test file)

Line 84, col 7 — pattern `anchor_substring`

```typescript
element.dispatchEvent(new Event('cancel', {bubbles: true}))
```

### Resolved definition

- **Path:** `node_modules/typescript/lib/lib.dom.d.ts`
- **Range:** line 8881, col 4
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
    /**
     * Dispatches a synthetic event event to target and returns true if either event's cancelable attribute value is false or its preventDefault() method was not invoked, and false otherwise.
     *
     * [MDN Reference](https://developer.mozilla.org/docs/Web/API/EventTarget/dispatchEvent)
     */
    dispatchEvent(event: Event): boolean;
```

### Nested usages resolved

- `Event` → `node_modules/@types/node/dom-events.d.ts`

---

## 126. Sample 72 · callee #3

- **Function:** `cancel`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/common/FileChooser.ts`
- **Callee:** `Event('cancel', {bubbles: true})`
- **Status:** OK

### Usage site (matched in test file)

Line 84, col 33 — pattern `anchor_substring`

```typescript
Event('cancel', {bubbles: true})
```

### Resolved definition

- **Path:** `node_modules/@types/node/dom-events.d.ts`
- **Range:** line 104, col 16

```typescript
/** An event which takes place in the DOM. */
    interface Event extends __Event {}
```

---

## 127. Sample 73 · callee #0

- **Function:** `unregisterCustomQueryHandler`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/common/Puppeteer.ts`
- **Callee:** `this.customQueryHandlers.unregister(name)`
- **Status:** OK

### Usage site (matched in test file)

Line 79, col 12 — pattern `anchor_substring`

```typescript
this.customQueryHandlers.unregister(name)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/common/CustomQueryHandler.ts`
- **Range:** line 125, col 3

```typescript
/**
   * Unregisters the {@link CustomQueryHandler | custom query handler} for the
   * given name.
   *
   * @throws `Error` if there is no handler under the given name.
   */
  unregister(name: string): void {
    const handler = this.#handlers.get(name);
    if (!handler) {
      throw new Error(`Cannot unregister unknown handler: ${name}`);
    }
    scriptInjector.pop(handler[0]);
    this.#handlers.delete(name);
  }
```

---

## 128. Sample 73 · callee #1

- **Function:** `unregisterCustomQueryHandler`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/common/Puppeteer.ts`
- **Callee:** `this.customQueryHandlers`
- **Status:** OK
- **Also seen in:** 2 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 79, col 12 — pattern `anchor_substring`

```typescript
this.customQueryHandlers
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/common/Puppeteer.ts`
- **Range:** line 34, col 24

```typescript
/**
   * Operations for {@link CustomQueryHandler | custom query handlers}. See
   * {@link CustomQueryHandlerRegistry}.
   *
   * @internal
   */
static customQueryHandlers = customQueryHandlers;
```

---

## 129. Sample 74 · callee #0

- **Function:** `customQueryHandlerNames`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/common/Puppeteer.ts`
- **Callee:** `this.customQueryHandlers.names()`
- **Status:** OK

### Usage site (matched in test file)

Line 86, col 12 — pattern `anchor_substring`

```typescript
this.customQueryHandlers.names()
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/common/CustomQueryHandler.ts`
- **Range:** line 140, col 3

```typescript
/**
   * Gets the names of all {@link CustomQueryHandler | custom query handlers}.
   */
  names(): string[] {
    return [...this.#handlers.keys()];
  }
```

---

## 130. Sample 75 · callee #0

- **Function:** `clearCustomQueryHandlers`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/common/Puppeteer.ts`
- **Callee:** `this.customQueryHandlers.clear()`
- **Status:** OK

### Usage site (matched in test file)

Line 93, col 12 — pattern `anchor_substring`

```typescript
this.customQueryHandlers.clear()
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/common/CustomQueryHandler.ts`
- **Range:** line 152, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
   * Unregisters all custom query handlers.
   */
  clear(): void {
    for (const [registerScript] of this.#handlers) {
      scriptInjector.pop(registerScript);
    }
    this.#handlers.clear();
  }
```

---

## 131. Sample 81 · callee #2

- **Function:** `getBadError`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/common/WaitTask.ts`
- **Callee:** `Error(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 199, col 9 — pattern `core_fallback`

```typescript
Error(...)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/common/WaitTask.ts`
- **Range:** line 193, col 3

```typescript
        return new Error('Waiting failed: Frame detached');
```

---

## 132. Sample 82 · callee #0

- **Function:** `connect`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/node/PuppeteerNode.ts`
- **Callee:** `super.connect(options)`
- **Status:** OK

### Usage site (matched in test file)

Line 113, col 12 — pattern `anchor_substring`

```typescript
super.connect(options)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/common/Puppeteer.ts`
- **Range:** line 121, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
   * This method attaches Puppeteer to an existing browser instance.
   *
   * @remarks
   *
   * @param options - Set of configurable options to set on the browser.
   * @returns Promise which resolves to browser instance.
   */
  connect(options: ConnectOptions): Promise<Browser> {
    return _connectToBrowser(options);
  }
```

---

## 133. Sample 83 · callee #0

- **Function:** `launch`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/node/PuppeteerNode.ts`
- **Callee:** `launcher.launch(options)`
- **Status:** OK

### Usage site (matched in test file)

Line 166, col 18 — pattern `anchor_substring`

```typescript
launcher.launch(options)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/node/BrowserLauncher.ts`
- **Range:** line 73, col 8
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  async launch(options: LaunchOptions = {}): Promise<Browser> {
    const {
      dumpio = false,
      enableExtensions = false,
      env = process.env,
      handleSIGINT = true,
      handleSIGTERM = true,
      handleSIGHUP = true,
      acceptInsecureCerts = false,
      defaultViewport = DEFAULT_VIEWPORT,
      downloadBehavior,
      slowMo = 0,
      timeout = 30000,
      waitForInitialPage = true,
      protocolTimeout,
    } = options;

    let {protocol} = options;

    // Default to 'webDriverBiDi' for Firefox.
    if (this.#browser === 'firefox' && protocol === undefined) {
      protocol = 'webDriverBiDi';
    }

    if (this.#browser === 'firefox' && protocol === 'cdp') {
      throw new Error('Connecting to Firefox using CDP is no longer supported');
    }

    const launchArgs = await this.computeLaunchArguments({
      ...options,
      protocol,
    });

    if (!existsSync(launchArgs.executablePath)) {
      throw new Error(
        `Browser was not found at the configured executablePath (${launchArgs.executablePath})`,
      );
    }

    const usePipe = launchArgs.args.includes('--remote-debugging-pipe');

    const onProcessExit = async () => {
      await this.cleanUserDataDir(launchArgs.userDataDir, {
        isTemp: launchArgs.isTempUserDataDir,
      });
    };

    if (
      this.#browser === 'firefox' &&
      protocol === 'webDriverBiDi' &&
      usePipe
    ) {
      throw new Error(
        'Pipe connections are not supported with Firefox and WebDriver BiDi',
      );
    }

    const browserProcess = launch({
      executablePath: launchArgs.executablePath,
      args: launchArgs.args,
      handleSIGHUP,
      handleSIGTERM,
      handleSIGINT,
      dumpio,
      env,
      pipe: usePipe,
      onExit: onProcessExit,
    });

    let browser: Browser;
    let cdpConnection: Connection;
    let closing = false;

    const browserCloseCallback: BrowserCloseCallback = async () => {
      if (closing) {
        return;
      }
      closing = true;
      await this.closeBrowser(browserProcess, cdpConnection);
    };

    try {
      if (this.#browser === 'firefox' && protocol === 'webDriverBiDi') {
        browser = await this.createBiDiBrowser(
          browserProcess,
          browserCloseCallback,
          {
            timeout,
            protocolTimeout,
            slowMo,
            defaultViewport,
            acceptInsecureCerts,
          },
        );
      } else {
        if (usePipe) {
          cdpConnection = await this.createCdpPipeConnection(browserProcess, {
            timeout,
            protocolTimeout,
            slowMo,
          });
        } else {
          cdpConnection = await this.createCdpSocketConnection(browserProcess, {
            timeout,
            protocolTimeout,
            slowMo,
          });
        }
        if (protocol === 'webDriverBiDi') {
          browser = await this.createBiDiOverCdpBrowser(
            browserProcess,
            cdpConnection,
            browserCloseCallback,
            {
              defaultViewport,
              acceptInsecureCerts,
            },
          );
        } else {
          browser = await CdpBrowser._create(
            cdpConnection,
            [],
            acceptInsecureCerts,
            defaultViewport,
            downloadBehavior,
            browserProcess.nodeProcess,
            browserCloseCallback,
            options.targetFilter,
          );
        }
      }
    } catch (error) {
      void browserCloseCallback();
      if (error instanceof BrowsersTimeoutError) {
        throw new TimeoutError(error.message);
      }
      throw error;
    }

    if (Array.isArray(enableExtensions)) {
      if (this.#browser === 'chrome' && !usePipe) {
        throw new Error(
          'To use `enableExtensions` with a list of paths in Chrome, you must be connected with `--remote-debugging-pipe` (`pipe: true`).',
        );
      }

      await Promise.all([
        enableExtensions.map(path => {
          return browser.installExtension(path);
        }),
      ]);
    }

    if (waitForInitialPage) {
      await this.waitForPageTarget(browser, timeout);
    }

    return browser;
  }
```

---

## 134. Sample 83 · callee #2

- **Function:** `launch`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/node/PuppeteerNode.ts`
- **Callee:** `getLauncher(browser)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 165, col 28 — pattern `anchor_substring`

```typescript
getLauncher(browser)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/node/PuppeteerNode.ts`
- **Range:** line 166, col 3

```typescript
    this.#launcher = this.#getLauncher(browser);
```

---

## 135. Sample 83 · callee #3

- **Function:** `launch`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/node/PuppeteerNode.ts`
- **Callee:** `this.defaultBrowser`
- **Status:** OK

### Usage site (matched in test file)

Line 153, col 22 — pattern `anchor_substring`

```typescript
this.defaultBrowser
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/node/PuppeteerNode.ts`
- **Range:** line 247, col 6
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
   * The name of the browser that will be launched by default. For
   * `puppeteer`, this is influenced by your configuration. Otherwise, it's
   * `chrome`.
   */
  get defaultBrowser(): SupportedBrowser {
    return this.configuration.defaultBrowser ?? 'chrome';
  }
```

---

## 136. Sample 83 · callee #4

- **Function:** `launch`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/node/PuppeteerNode.ts`
- **Callee:** `this.defaultBrowserRevision`
- **Status:** OK

### Usage site (matched in test file)

Line 157, col 9 — pattern `anchor_substring`

```typescript
this.defaultBrowserRevision
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/node/PuppeteerNode.ts`
- **Range:** line 68, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript

  /**
   * @internal
   */
  defaultBrowserRevision: string;
```

---

## 137. Sample 83 · callee #5

- **Function:** `launch`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/node/PuppeteerNode.ts`
- **Callee:** `PUPPETEER_REVISIONS.chrome`
- **Status:** OK

### Usage site (matched in test file)

Line 157, col 39 — pattern `anchor_substring`

```typescript
PUPPETEER_REVISIONS.chrome
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/revisions.ts`
- **Range:** line 10, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
chrome: '137.0.7151.55',
```

---

## 138. Sample 83 · callee #6

- **Function:** `launch`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/node/PuppeteerNode.ts`
- **Callee:** `PUPPETEER_REVISIONS.firefox`
- **Status:** OK

### Usage site (matched in test file)

Line 160, col 39 — pattern `anchor_substring`

```typescript
PUPPETEER_REVISIONS.firefox
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/revisions.ts`
- **Range:** line 12, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
firefox: 'stable_139.0',
```

---

## 139. Sample 84 · callee #0

- **Function:** `defaultDownloadPath`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/node/PuppeteerNode.ts`
- **Callee:** `this.configuration`
- **Status:** OK
- **Also seen in:** 2 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 233, col 12 — pattern `anchor_substring`

```typescript
this.configuration
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/node/PuppeteerNode.ts`
- **Range:** line 73, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript

  /**
   * @internal
   */
  configuration: Configuration = {};
```

---

## 140. Sample 86 · callee #0

- **Function:** `product`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/node/PuppeteerNode.ts`
- **Callee:** `this.lastLaunchedBrowser`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 261, col 12 — pattern `anchor_substring`

```typescript
this.lastLaunchedBrowser
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/node/PuppeteerNode.ts`
- **Range:** line 238, col 6
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
   * The name of the browser that was last launched.
   */
  get lastLaunchedBrowser(): SupportedBrowser {
    return this.#lastLaunchedBrowser ?? this.defaultBrowser;
  }
```

---

## 141. Sample 88 · callee #0

- **Function:** `trimCache`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/node/PuppeteerNode.ts`
- **Callee:** `detectBrowserPlatform()`
- **Status:** OK

### Usage site (matched in test file)

Line 290, col 22 — pattern `anchor_substring`

```typescript
detectBrowserPlatform()
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/node/PuppeteerNode.ts`
- **Range:** line 8, col 17

```typescript
    const platform = detectBrowserPlatform();
```

---

## 142. Sample 88 · callee #2

- **Function:** `trimCache`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/node/PuppeteerNode.ts`
- **Callee:** `getInstalledBrowsers(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 296, col 37 — pattern `core_fallback`

```typescript
getInstalledBrowsers(...)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/node/PuppeteerNode.ts`
- **Range:** line 9, col 24

```typescript
    const installedBrowsers = await getInstalledBrowsers({
      cacheDir,
    });
```

---

## 143. Sample 88 · callee #3

- **Function:** `trimCache`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/node/PuppeteerNode.ts`
- **Callee:** `resolveBuildId(item.browser, platform, tag)`
- **Status:** OK

### Usage site (matched in test file)

Line 323, col 35 — pattern `anchor_substring`

```typescript
resolveBuildId(item.browser, platform, tag)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/node/PuppeteerNode.ts`
- **Range:** line 7, col 39

```typescript
      item.currentBuildId = await resolveBuildId(item.browser, platform, tag);
```

---

## 144. Sample 88 · callee #4

- **Function:** `trimCache`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/node/PuppeteerNode.ts`
- **Callee:** `Set(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 326, col 38 — pattern `core_fallback`

```typescript
Set(...)
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es2015.collection.d.ts`
- **Range:** line 87, col 40

```typescript
declare var Set: SetConstructor;
```

---

## 145. Sample 88 · callee #6

- **Function:** `trimCache`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/node/PuppeteerNode.ts`
- **Callee:** `browsers_SupportedBrowser.CHROME`
- **Status:** OK

### Usage site (matched in test file)

Line 307, col 18 — pattern `anchor_substring`

```typescript
browsers_SupportedBrowser.CHROME
```

### Resolved definition

- **Path:** `packages/browsers/src/browser-data/types.ts`
- **Range:** line 12, col 0
- **Selection:** `import_alias_enum_member`

```typescript
CHROME = 'chrome',
```

---

## 146. Sample 88 · callee #7

- **Function:** `trimCache`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/node/PuppeteerNode.ts`
- **Callee:** `browsers_SupportedBrowser.FIREFOX`
- **Status:** OK

### Usage site (matched in test file)

Line 312, col 18 — pattern `anchor_substring`

```typescript
browsers_SupportedBrowser.FIREFOX
```

### Resolved definition

- **Path:** `packages/browsers/src/browser-data/types.ts`
- **Range:** line 15, col 0
- **Selection:** `import_alias_enum_member`

```typescript
FIREFOX = 'firefox',
```

---

## 147. Sample 88 · callee #8

- **Function:** `trimCache`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/node/PuppeteerNode.ts`
- **Callee:** `browser.browser`
- **Status:** OK

### Usage site (matched in test file)

Line 328, col 19 — pattern `anchor_substring`

```typescript
browser.browser
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/node/PuppeteerNode.ts`
- **Range:** line 301, col 6
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
      browser: browsers_SupportedBrowser;
```

---

## 148. Sample 88 · callee #9

- **Function:** `trimCache`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/node/PuppeteerNode.ts`
- **Callee:** `browser.currentBuildId`
- **Status:** OK

### Usage site (matched in test file)

Line 328, col 38 — pattern `anchor_substring`

```typescript
browser.currentBuildId
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/node/PuppeteerNode.ts`
- **Range:** line 302, col 6
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
      currentBuildId: string;
```

---

## 149. Sample 92 · callee #0

- **Function:** `move`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/util/disposable.ts`
- **Callee:** `ReferenceError('A disposed stack can not use anything new')`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 145, col 17 — pattern `anchor_substring`

```typescript
ReferenceError('A disposed stack can not use anything new')
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es5.d.ts`
- **Range:** line 1106, col 46

```typescript
interface ReferenceError extends Error {
}
```

---

## 150. Sample 92 · callee #1

- **Function:** `move`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/util/disposable.ts`
- **Callee:** `DisposableStack()`
- **Status:** OK

### Usage site (matched in test file)

Line 147, col 23 — pattern `anchor_substring`

```typescript
DisposableStack()
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/util/disposable.ts`
- **Range:** line 47, col 13
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
 * @internal
 */
export class DisposableStack {
  #disposed = false;
  #stack: Disposable[] = [];

  /**
   * Returns a value indicating whether the stack has been disposed.
   */
  get disposed(): boolean {
    return this.#disposed;
  }

  /**
   * Alias for `[Symbol.dispose]()`.
   */
  dispose(): void {
    this[disposeSymbol]();
  }

  /**
   * Adds a disposable resource to the top of stack, returning the resource.
   * Has no effect if provided `null` or `undefined`.
   *
   * @param value - A `Disposable` object, `null`, or `undefined`.
   * `null` and `undefined` will not be added, but will be returned.
   * @returns The provided `value`.
   */
  use<T extends Disposable | null | undefined>(value: T): T {
    if (value && typeof value[disposeSymbol] === 'function') {
      this.#stack.push(value);
    }
    return value;
  }

  /**
   * Adds a non-disposable resource and a disposal callback to the top of the stack.
   *
   * @param value - A resource to be disposed.
   * @param onDispose - A callback invoked to dispose the provided value.
   * Will be invoked with `value` as the first parameter.
   * @returns The provided `value`.
   */
  adopt<T>(value: T, onDispose: (value: T) => void): T {
    this.#stack.push({
      [disposeSymbol]() {
        onDispose(value);
      },
    });
    return value;
  }

  /**
   * Add a disposal callback to the top of the stack to be invoked when stack is disposed.
   * @param onDispose - A callback to invoke when this object is disposed.
   */
  defer(onDispose: () => void): void {
    this.#stack.push({
      [disposeSymbol]() {
        onDispose();
      },
    });
  }

  /**
   * Move all resources out of this stack and into a new `DisposableStack`, and
   * marks this stack as disposed.
   * @returns The new `DisposableStack`.
   *
   * @example
   *
   * ```ts
   * class C {
   *   #res1: Disposable;
   *   #res2: Disposable;
   *   #disposables: DisposableStack;
   *   constructor() {
   *     // stack will be disposed when exiting constructor for any reason
   *     using stack = new DisposableStack();
   *
   *     // get first resource
   *     this.#res1 = stack.use(getResource1());
   *
   *     // get second resource. If this fails, both `stack` and `#res1` will be disposed.
   *     this.#res2 = stack.use(getResource2());
   *
   *     // all operations succeeded, move resources out of `stack` so that
   *     // they aren't disposed when constructor exits
   *     this.#disposables = stack.move();
   *   }
   *
   *   [disposeSymbol]() {
   *     this.#disposables.dispose();
   *   }
   * }
   * ```
   */
  move(): DisposableStack {
    if (this.#disposed) {
      throw new ReferenceError('A disposed stack can not use anything new');
    }
    const stack = new DisposableStack();
    stack.#stack = this.#stack;
    this.#stack = [];
    this.#disposed = true;
    return stack;
  }

  /**
   * Disposes each resource in the stack in last-in-first-out (LIFO) manner.
   */
  [disposeSymbol](): void {
    if (this.#disposed) {
      return;
    }
    this.#disposed = true;
    const errors: unknown[] = [];
    for (const resource of this.#stack.reverse()) {
      try {
        resource[disposeSymbol]();
      } catch (e) {
        errors.push(e);
      }
    }
    if (errors.length === 1) {
      throw errors[0];
    } else if (errors.length > 1) {
      let suppressed = null;
      for (const error of errors.reverse()) {
        if (suppressed === null) {
          suppressed = error;
        } else {
          suppressed = new SuppressedError(error, suppressed);
        }
      }
      throw suppressed;
    }
  }

  readonly [Symbol.toStringTag] = 'DisposableStack';
}
```

---

## 151. Sample 93 · callee #0

- **Function:** `[disposeSymbol]`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/util/disposable.ts`
- **Callee:** `stack.reverse()`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 163, col 34 — pattern `anchor_substring`

```typescript
stack.reverse()
```

### Resolved definition

- **Path:** `node_modules/typescript/lib/lib.es5.d.ts`
- **Range:** line 1365, col 4
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
    /**
     * Reverses the elements in an array in place.
     * This method mutates the array and returns a reference to the same array.
     */
    reverse(): T[];
```

---

## 152. Sample 93 · callee #1

- **Function:** `[disposeSymbol]`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/util/disposable.ts`
- **Callee:** `SuppressedError(error, suppressed)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 178, col 28 — pattern `anchor_substring`

```typescript
SuppressedError(error, suppressed)
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/util/disposable.ts`
- **Range:** line 348, col 13
- **Selection:** `preferred_implementation_over_declaration_kept=2`

```typescript
/**
 * @internal
 * Represents an error that occurs when multiple errors are thrown during
 * the disposal of resources. This class encapsulates the primary error and
 * any suppressed errors that occurred subsequently.
 */
export class SuppressedError extends Error {
  #error: unknown;
  #suppressed: unknown;

  constructor(
    error: unknown,
    suppressed: unknown,
    message = 'An error was suppressed during disposal',
  ) {
    super(message);
    this.name = 'SuppressedError';
    this.#error = error;
    this.#suppressed = suppressed;
  }

  /**
   * The primary error that occurred during disposal.
   */
  get error(): unknown {
    return this.#error;
  }

  /**
   * The suppressed error i.e. the error that was suppressed
   * because it occurred later in the flow after the original error.
   */
  get suppressed(): unknown {
    return this.#suppressed;
  }
}
```

---

## 153. Sample 97 · callee #1

- **Function:** `move`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/packages/puppeteer-core/src/util/disposable.ts`
- **Callee:** `AsyncDisposableStack()`
- **Status:** OK

### Usage site (matched in test file)

Line 302, col 23 — pattern `anchor_substring`

```typescript
AsyncDisposableStack()
```

### Resolved definition

- **Path:** `packages/puppeteer-core/src/util/disposable.ts`
- **Range:** line 190, col 13
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
 * @internal
 */
export class AsyncDisposableStack {
  #disposed = false;
  #stack: AsyncDisposable[] = [];

  /**
   * Returns a value indicating whether the stack has been disposed.
   */
  get disposed(): boolean {
    return this.#disposed;
  }

  /**
   * Alias for `[Symbol.asyncDispose]()`.
   */
  async dispose(): Promise<void> {
    await this[asyncDisposeSymbol]();
  }

  /**
   * Adds a AsyncDisposable resource to the top of stack, returning the resource.
   * Has no effect if provided `null` or `undefined`.
   *
   * @param value - A `AsyncDisposable` object, `null`, or `undefined`.
   * `null` and `undefined` will not be added, but will be returned.
   * @returns The provided `value`.
   */
  use<T extends AsyncDisposable | Disposable | null | undefined>(value: T): T {
    if (value) {
      const asyncDispose = (value as AsyncDisposable)[asyncDisposeSymbol];
      const dispose = (value as Disposable)[disposeSymbol];

      if (typeof asyncDispose === 'function') {
        this.#stack.push(value as AsyncDisposable);
      } else if (typeof dispose === 'function') {
        this.#stack.push({
          [asyncDisposeSymbol]: async () => {
            (value as Disposable)[disposeSymbol]();
          },
        });
      }
    }

    return value;
  }

  /**
   * Adds a non-disposable resource and a disposal callback to the top of the stack.
   *
   * @param value - A resource to be disposed.
   * @param onDispose - A callback invoked to dispose the provided value.
   * Will be invoked with `value` as the first parameter.
   * @returns The provided `value`.
   */
  adopt<T>(value: T, onDispose: (value: T) => Promise<void>): T {
    this.#stack.push({
      [asyncDisposeSymbol]() {
        return onDispose(value);
      },
    });
    return value;
  }

  /**
   * Add a disposal callback to the top of the stack to be invoked when stack is disposed.
   * @param onDispose - A callback to invoke when this object is disposed.
   */
  defer(onDispose: () => Promise<void>): void {
    this.#stack.push({
      [asyncDisposeSymbol]() {
        return onDispose();
      },
    });
  }

  /**
   * Move all resources out of this stack and into a new `DisposableStack`, and
   * marks this stack as disposed.
   * @returns The new `AsyncDisposableStack`.
   *
   * @example
   *
   * ```ts
   * class C {
   *   #res1: Disposable;
   *   #res2: Disposable;
   *   #disposables: DisposableStack;
   *   constructor() {
   *     // stack will be disposed when exiting constructor for any reason
   *     using stack = new DisposableStack();
   *
   *     // get first resource
   *     this.#res1 = stack.use(getResource1());
   *
   *     // get second resource. If this fails, both `stack` and `#res1` will be disposed.
   *     this.#res2 = stack.use(getResource2());
   *
   *     // all operations succeeded, move resources out of `stack` so that
   *     // they aren't disposed when constructor exits
   *     this.#disposables = stack.move();
   *   }
   *
   *   [disposeSymbol]() {
   *     this.#disposables.dispose();
   *   }
   * }
   * ```
   */
  move(): AsyncDisposableStack {
    if (this.#disposed) {
      throw new ReferenceError('A disposed stack can not use anything new');
    }
    const stack = new AsyncDisposableStack();
    stack.#stack = this.#stack;
    this.#stack = [];
    this.#disposed = true;
    return stack;
  }

  /**
   * Disposes each resource in the stack in last-in-first-out (LIFO) manner.
   */
  async [asyncDisposeSymbol](): Promise<void> {
    if (this.#disposed) {
      return;
    }
    this.#disposed = true;
    const errors: unknown[] = [];
    for (const resource of this.#stack.reverse()) {
      try {
        await resource[asyncDisposeSymbol]();
      } catch (e) {
        errors.push(e);
      }
    }
    if (errors.length === 1) {
      throw errors[0];
    } else if (errors.length > 1) {
      let suppressed = null;
      for (const error of errors.reverse()) {
        if (suppressed === null) {
          suppressed = error;
        } else {
          suppressed = new SuppressedError(error, suppressed);
        }
      }
      throw suppressed;
    }
  }

  readonly [Symbol.toStringTag] = 'AsyncDisposableStack';
}
```

---

## 154. Sample 100 · callee #0

- **Function:** `_createDescriptionCell`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/tools/docgen/src/custom_markdown_documenter.ts`
- **Callee:** `ApiReleaseTagMixin.isBaseClassOf(apiItem)`
- **Status:** OK

### Usage site (matched in test file)

Line 1334, col 9 — pattern `anchor_substring`

```typescript
ApiReleaseTagMixin.isBaseClassOf(apiItem)
```

### Resolved definition

- **Path:** `node_modules/@microsoft/api-extractor-model/dist/rollup.d.ts`
- **Range:** line 1783, col 45

```typescript
/**
     * A type guard that tests whether the specified `ApiItem` subclass extends the `ApiReleaseTagMixin` mixin.
     *
     * @remarks
     *
     * The JavaScript `instanceof` operator cannot be used to test for mixin inheritance, because each invocation of
     * the mixin function produces a different subclass.  (This could be mitigated by `Symbol.hasInstance`, however
     * the TypeScript type system cannot invoke a runtime test.)
     */
    export function isBaseClassOf(apiItem: ApiItem): apiItem is ApiReleaseTagMixin;
```

---

## 155. Sample 100 · callee #1

- **Function:** `_createDescriptionCell`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/tools/docgen/src/custom_markdown_documenter.ts`
- **Callee:** `modifierTagSet.isExperimental()`
- **Status:** OK

### Usage site (matched in test file)

Line 1347, col 31 — pattern `anchor_substring`

```typescript
modifierTagSet.isExperimental()
```

### Resolved definition

- **Path:** `node_modules/@microsoft/tsdoc/lib/details/StandardModifierTagSet.d.ts`
- **Range:** line 21, col 4
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
    /**
     * Returns true if the `@experimental` modifier tag was specified.
     */
    isExperimental(): boolean;
```

---

## 156. Sample 100 · callee #2

- **Function:** `_createDescriptionCell`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/tools/docgen/src/custom_markdown_documenter.ts`
- **Callee:** `this._appendAndMergeSection(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 1360, col 14 — pattern `core_fallback`

```typescript
this._appendAndMergeSection(...)
```

### Resolved definition

- **Path:** `tools/docgen/src/custom_markdown_documenter.ts`
- **Range:** line 1516, col 10
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  private _appendAndMergeSection(
    output: DocSection,
    docSection: DocSection,
  ): void {
    let firstNode = true;
    for (const node of docSection.nodes) {
      if (firstNode) {
        if (node.kind === DocNodeKind.Paragraph) {
          output.appendNodesInParagraph(node.getChildNodes());
          firstNode = false;
          continue;
        }
      }
      firstNode = false;

      output.appendNode(node);
    }
  }
```

---

## 157. Sample 100 · callee #3

- **Function:** `_createDescriptionCell`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/tools/docgen/src/custom_markdown_documenter.ts`
- **Callee:** `DocSection(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 1332, col 25 — pattern `core_fallback`

```typescript
DocSection(...)
```

### Resolved definition

- **Path:** `node_modules/@microsoft/tsdoc/lib/nodes/DocSection.d.ts`
- **Range:** line 11, col 1
- **Selection:** `external_runtime_resolution_after_ts_nav`

```typescript
/**
 * Represents a general block of rich text.
 */
export declare class DocSection extends DocNodeContainer {
    /**
     * Don't call this directly.  Instead use {@link TSDocParser}
     * @internal
     */
    constructor(parameters: IDocSectionParameters | IDocSectionParsedParameters, childNodes?: ReadonlyArray<DocNode>);
    /** @override */
    get kind(): DocNodeKind | string;
    /**
     * If the last item in DocSection.nodes is not a DocParagraph, a new paragraph
     * is started.  Either way, the provided docNode will be appended to the paragraph.
     */
    appendNodeInParagraph(docNode: DocNode): void;
    appendNodesInParagraph(docNodes: ReadonlyArray<DocNode>): void;
}
```

### Runtime implementation

- **Body:** `node_modules/@microsoft/tsdoc/lib/nodes/DocSection.js`
- **Range:** line 23, col 0

```typescript
/**
 * Represents a general block of rich text.
 */
var DocSection = /** @class */ (function (_super) {
    __extends(DocSection, _super);
    /**
     * Don't call this directly.  Instead use {@link TSDocParser}
     * @internal
     */
    function DocSection(parameters, childNodes) {
        return _super.call(this, parameters, childNodes) || this;
    }
    Object.defineProperty(DocSection.prototype, "kind", {
        /** @override */
        get: function () {
            return DocNodeKind.Section;
        },
        enumerable: false,
        configurable: true
    });
    /**
     * If the last item in DocSection.nodes is not a DocParagraph, a new paragraph
     * is started.  Either way, the provided docNode will be appended to the paragraph.
     */
    DocSection.prototype.appendNodeInParagraph = function (docNode) {
        var paragraphNode = undefined;
        if (this.nodes.length > 0) {
            var lastNode = this.nodes[this.nodes.length - 1];
            if (lastNode.kind === DocNodeKind.Paragraph) {
                paragraphNode = lastNode;
            }
        }
        if (!paragraphNode) {
            paragraphNode = new DocParagraph({ configuration: this.configuration });
            this.appendNode(paragraphNode);
        }
        paragraphNode.appendNode(docNode);
    };
    DocSection.prototype.appendNodesInParagraph = function (docNodes) {
        for (var _i = 0, docNodes_1 = docNodes; _i < docNodes_1.length; _i++) {
            var docNode = docNodes_1[_i];
            this.appendNodeInParagraph(docNode);
        }
    };
    return DocSection;
}(DocNodeContainer));
```

---

## 158. Sample 100 · callee #4

- **Function:** `_createDescriptionCell`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/tools/docgen/src/custom_markdown_documenter.ts`
- **Callee:** `DocEmphasisSpan(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 1337, col 15 — pattern `core_fallback`

```typescript
DocEmphasisSpan(...)
```

### Resolved definition

- **Path:** `node_modules/@microsoft/api-documenter/lib/nodes/DocEmphasisSpan.js`
- **Range:** line 11, col 6
- **Selection:** `preferred_implementation_over_declaration_kept=2`

```typescript
/**
 * Represents a span of text that is styled with CommonMark emphasis (italics), strong emphasis (boldface),
 * or both.
 */
class DocEmphasisSpan extends tsdoc_1.DocNodeContainer {
    constructor(parameters, children) {
        super(parameters, children);
        this.bold = !!parameters.bold;
        this.italic = !!parameters.italic;
    }
    /** @override */
    get kind() {
        return CustomDocNodeKind_1.CustomDocNodeKind.EmphasisSpan;
    }
}
```

---

## 159. Sample 100 · callee #5

- **Function:** `_createDescriptionCell`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/tools/docgen/src/custom_markdown_documenter.ts`
- **Callee:** `DocPlainText(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 1338, col 17 — pattern `core_fallback`

```typescript
DocPlainText(...)
```

### Resolved definition

- **Path:** `node_modules/@microsoft/tsdoc/lib/nodes/DocPlainText.d.ts`
- **Range:** line 13, col 1
- **Selection:** `external_runtime_resolution_after_ts_nav`

```typescript
/**
 * Represents a span of comment text that is considered by the parser
 * to contain no special symbols or meaning.
 *
 * @remarks
 * The text content must not contain newline characters.
 * Use DocSoftBreak to represent manual line splitting.
 */
export declare class DocPlainText extends DocNode {
    private static readonly _newlineCharacterRegExp;
    private _text;
    private readonly _textExcerpt;
    /**
     * Don't call this directly.  Instead use {@link TSDocParser}
     * @internal
     */
    constructor(parameters: IDocPlainTextParameters | IDocPlainTextParsedParameters);
    /** @override */
    get kind(): DocNodeKind | string;
    /**
     * The text content.
     */
    get text(): string;
    get textExcerpt(): TokenSequence | undefined;
    /** @override */
    protected onGetChildNodes(): ReadonlyArray<DocNode | undefined>;
}
```

### Runtime implementation

- **Body:** `node_modules/@microsoft/tsdoc/lib/nodes/DocPlainText.js`
- **Range:** line 27, col 0

```typescript
/**
 * Represents a span of comment text that is considered by the parser
 * to contain no special symbols or meaning.
 *
 * @remarks
 * The text content must not contain newline characters.
 * Use DocSoftBreak to represent manual line splitting.
 */
var DocPlainText = /** @class */ (function (_super) {
    __extends(DocPlainText, _super);
    /**
     * Don't call this directly.  Instead use {@link TSDocParser}
     * @internal
     */
    function DocPlainText(parameters) {
        var _this = _super.call(this, parameters) || this;
        if (DocNode.isParsedParameters(parameters)) {
            _this._textExcerpt = new DocExcerpt({
                configuration: _this.configuration,
                excerptKind: ExcerptKind.PlainText,
                content: parameters.textExcerpt
            });
        }
        else {
            if (DocPlainText._newlineCharacterRegExp.test(parameters.text)) {
                // Use DocSoftBreak to represent manual line splitting
                throw new Error('The DocPlainText content must not contain newline characters');
            }
            _this._text = parameters.text;
        }
        return _this;
    }
    Object.defineProperty(DocPlainText.prototype, "kind", {
        /** @override */
        get: function () {
            return DocNodeKind.PlainText;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(DocPlainText.prototype, "text", {
        /**
         * The text content.
         */
        get: function () {
            if (this._text === undefined) {
                this._text = this._textExcerpt.content.toString();
            }
            return this._text;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(DocPlainText.prototype, "textExcerpt", {
        get: function () {
            if (this._textExcerpt) {
                return this._textExcerpt.content;
            }
            else {
                return undefined;
            }
        },
        enumerable: false,
        configurable: true
    });
    /** @override */
    DocPlainText.prototype.onGetChildNodes = function () {
        return [this._textExcerpt];
    };
    // TODO: We should also prohibit "\r", but this requires updating LineExtractor
    // to interpret a lone "\r" as a newline
    DocPlainText._newlineCharacterRegExp = /[\n]/;
    return DocPlainText;
}(DocNode));
```

---

## 160. Sample 100 · callee #6

- **Function:** `_createDescriptionCell`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/tools/docgen/src/custom_markdown_documenter.ts`
- **Callee:** `DocParagraph(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 1367, col 17 — pattern `core_fallback`

```typescript
DocParagraph(...)
```

### Resolved definition

- **Path:** `node_modules/@microsoft/tsdoc/lib/nodes/DocParagraph.d.ts`
- **Range:** line 6, col 1
- **Selection:** `external_runtime_resolution_after_ts_nav`

```typescript
/**
 * Represents a paragraph of text, similar to a `<p>` element in HTML.
 * Like CommonMark, the TSDoc syntax uses blank lines to delineate paragraphs
 * instead of explicitly notating them.
 */
export declare class DocParagraph extends DocNodeContainer {
    /**
     * Don't call this directly.  Instead use {@link TSDocParser}
     * @internal
     */
    constructor(parameters: IDocParagraphParameters, childNodes?: ReadonlyArray<DocNode>);
    /** @override */
    get kind(): DocNodeKind | string;
}
```

### Runtime implementation

- **Body:** `node_modules/@microsoft/tsdoc/lib/nodes/DocParagraph.js`
- **Range:** line 24, col 0

```typescript
/**
 * Represents a paragraph of text, similar to a `<p>` element in HTML.
 * Like CommonMark, the TSDoc syntax uses blank lines to delineate paragraphs
 * instead of explicitly notating them.
 */
var DocParagraph = /** @class */ (function (_super) {
    __extends(DocParagraph, _super);
    /**
     * Don't call this directly.  Instead use {@link TSDocParser}
     * @internal
     */
    function DocParagraph(parameters, childNodes) {
        return _super.call(this, parameters, childNodes) || this;
    }
    Object.defineProperty(DocParagraph.prototype, "kind", {
        /** @override */
        get: function () {
            return DocNodeKind.Paragraph;
        },
        enumerable: false,
        configurable: true
    });
    return DocParagraph;
}(DocNodeContainer));
```

---

## 161. Sample 100 · callee #7

- **Function:** `_createDescriptionCell`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/tools/docgen/src/custom_markdown_documenter.ts`
- **Callee:** `DocTableCell(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 1396, col 16 — pattern `core_fallback`

```typescript
DocTableCell(...)
```

### Resolved definition

- **Path:** `node_modules/@microsoft/api-documenter/lib/nodes/DocTableCell.js`
- **Range:** line 10, col 6
- **Selection:** `preferred_implementation_over_declaration_kept=2`

```typescript
/**
 * Represents table cell, similar to an HTML `<td>` element.
 */
class DocTableCell extends tsdoc_1.DocNode {
    constructor(parameters, sectionChildNodes) {
        super(parameters);
        this.content = new tsdoc_1.DocSection({ configuration: this.configuration }, sectionChildNodes);
    }
    /** @override */
    get kind() {
        return CustomDocNodeKind_1.CustomDocNodeKind.TableCell;
    }
}
```

---

## 162. Sample 100 · callee #8

- **Function:** `_createDescriptionCell`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/tools/docgen/src/custom_markdown_documenter.ts`
- **Callee:** `this._tsdocConfiguration`
- **Status:** OK

### Usage site (matched in test file)

Line 1330, col 27 — pattern `anchor_substring`

```typescript
this._tsdocConfiguration
```

### Resolved definition

- **Path:** `tools/docgen/src/custom_markdown_documenter.ts`
- **Range:** line 112, col 19
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  private readonly _tsdocConfiguration: TSDocConfiguration;
```

---

## 163. Sample 100 · callee #9

- **Function:** `_createDescriptionCell`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/tools/docgen/src/custom_markdown_documenter.ts`
- **Callee:** `ReleaseTag.Beta`
- **Status:** OK

### Usage site (matched in test file)

Line 1335, col 34 — pattern `anchor_substring`

```typescript
ReleaseTag.Beta
```

### Resolved definition

- **Path:** `node_modules/@microsoft/api-extractor-model/dist/rollup.d.ts`
- **Range:** line 2894, col 14

```typescript
/**
     * Indicates that an API item has been released in an experimental state. Third parties are
     * encouraged to try it and provide feedback. However, a "beta" API should NOT be used
     * in production.
     */
Beta = 3,
```

---

## 164. Sample 100 · callee #10

- **Function:** `_createDescriptionCell`
- **File:** `/Users/trieyang/Desktop/DocPrism/puppeteer/tools/docgen/src/custom_markdown_documenter.ts`
- **Callee:** `deprecatedBlock.content`
- **Status:** OK

### Usage site (matched in test file)

Line 1375, col 34 — pattern `anchor_substring`

```typescript
deprecatedBlock.content
```

### Resolved definition

- **Path:** `node_modules/@microsoft/tsdoc/lib/nodes/DocBlock.d.ts`
- **Range:** line 14, col 1

```typescript
/**
     * The TSDoc tag that introduces this section.
     */
    get content(): DocSection;
```

---
