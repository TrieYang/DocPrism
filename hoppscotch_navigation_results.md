# Hoppscotch code navigation results

Generated from `code_navigation_TypeScript.resolve_from_snippet` on samples in `hoppscotch.json`.

## Summary

- Runtime: 317.77s
- Samples with at least one callee: 94
- Callee rows evaluated: 547 (547 ok, 0 failed)
- Samples skipped (no extractable callees): 6
- Unique resolved definitions shown below: 235 (deduped from 547 callee rows)

---

## 1. Sample 2 · callee #0

- **Function:** `createPAT`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/access-token/access-token.service.ts`
- **Callee:** `E.left(...)`
- **Status:** OK
- **Also seen in:** 70 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 75, col 16 — pattern `core_fallback`

```typescript
E.left(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/fp-ts@2.16.10/node_modules/fp-ts/lib/Either.d.ts`
- **Range:** line 117, col 20
- **Selection:** `external_runtime_resolution_after_ts_nav`

```typescript
/**
 * Constructs a new `Either` holding a `Left` value. This usually represents a failure, due to the right-bias of this
 * structure.
 *
 * @category constructors
 * @since 2.0.0
 */
export declare const left: <E = never, A = never>(e: E) => Either<E, A>
```

### Runtime implementation

- **Export surface:** `node_modules/.pnpm/fp-ts@2.16.10/node_modules/fp-ts/lib/Either.js`

```typescript
// -------------------------------------------------------------------------------------
// constructors
// -------------------------------------------------------------------------------------
/**
 * Constructs a new `Either` holding a `Left` value. This usually represents a failure, due to the right-bias of this
 * structure.
 *
 * @category constructors
 * @since 2.0.0
 */
exports.left = _.left;
```

- **Body:** `node_modules/.pnpm/fp-ts@2.16.10/node_modules/fp-ts/lib/internal.js`
- **Range:** line 37, col 0

```typescript
/** @internal */
var left = function (e) { return ({ _tag: 'Left', left: e }); };
```

---

## 2. Sample 2 · callee #1

- **Function:** `createPAT`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/access-token/access-token.service.ts`
- **Callee:** `this.validateExpirationDate(createAccessTokenDto.expiryInDays)`
- **Status:** OK

### Usage site (matched in test file)

Line 80, col 10 — pattern `anchor_substring`

```typescript
this.validateExpirationDate(createAccessTokenDto.expiryInDays)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/access-token/access-token.service.ts`
- **Range:** line 29, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Validate the expiration date of the token
   *
   * @param expiresOn Number of days the token is valid for
   * @returns Boolean indicating if the expiration date is valid
   */
  private validateExpirationDate(expiresOn: null | number) {
    if (expiresOn === null || this.VALID_TOKEN_DURATIONS.includes(expiresOn))
      return true;
    return false;
  }
```

---

## 3. Sample 2 · callee #2

- **Function:** `createPAT`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/access-token/access-token.service.ts`
- **Callee:** `this.prisma.personalAccessToken.create(...)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 86, col 62 — pattern `core_fallback`

```typescript
this.prisma.personalAccessToken.create(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 21969, col 241

```typescript
/**
     * Create a PersonalAccessToken.
     * @param {PersonalAccessTokenCreateArgs} args - Arguments to create a PersonalAccessToken.
     * @example
     * // Create one PersonalAccessToken
     * const PersonalAccessToken = await prisma.personalAccessToken.create({
     *   data: {
     *     // ... data to create a PersonalAccessToken
     *   }
     * })
     * 
     */
    create<T extends PersonalAccessTokenCreateArgs>(args: SelectSubset<T, PersonalAccessTokenCreateArgs<ExtArgs>>): Prisma__PersonalAccessTokenClient<$Result.GetResult<Prisma.$PersonalAccessTokenPayload<ExtArgs>, T, "create", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>
```

---

## 4. Sample 2 · callee #3

- **Function:** `createPAT`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/access-token/access-token.service.ts`
- **Callee:** `this.cast(createdPAT)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 96, col 13 — pattern `anchor_substring`

```typescript
this.cast(createdPAT)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/access-token/access-token.service.ts`
- **Range:** line 40, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Typecast a database PersonalAccessToken to a AccessToken model
   * @param token database PersonalAccessToken
   * @returns AccessToken model
   */
  private cast(token: PersonalAccessToken): AccessToken {
    return <AccessToken>{
      id: token.id,
      label: token.label,
      createdOn: token.createdOn,
      expiresOn: token.expiresOn,
      lastUsedOn: token.updatedOn,
    };
  }
```

---

## 5. Sample 2 · callee #4

- **Function:** `createPAT`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/access-token/access-token.service.ts`
- **Callee:** `E.right(res)`
- **Status:** OK
- **Also seen in:** 47 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 99, col 12 — pattern `anchor_substring`

```typescript
E.right(res)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/fp-ts@2.16.10/node_modules/fp-ts/lib/Either.d.ts`
- **Range:** line 125, col 20
- **Selection:** `external_runtime_resolution_after_ts_nav`

```typescript
/**
 * Constructs a new `Either` holding a `Right` value. This usually represents a successful value due to the right bias
 * of this structure.
 *
 * @category constructors
 * @since 2.0.0
 */
export declare const right: <E = never, A = never>(a: A) => Either<E, A>
```

### Runtime implementation

- **Export surface:** `node_modules/.pnpm/fp-ts@2.16.10/node_modules/fp-ts/lib/Either.js`

```typescript
/**
 * Constructs a new `Either` holding a `Right` value. This usually represents a successful value due to the right bias
 * of this structure.
 *
 * @category constructors
 * @since 2.0.0
 */
exports.right = _.right;
```

- **Body:** `node_modules/.pnpm/fp-ts@2.16.10/node_modules/fp-ts/lib/internal.js`
- **Range:** line 40, col 0

```typescript
/** @internal */
var right = function (a) { return ({ _tag: 'Right', right: a }); };
```

---

## 6. Sample 2 · callee #5

- **Function:** `createPAT`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/access-token/access-token.service.ts`
- **Callee:** `isValidLength(...)`
- **Status:** OK
- **Also seen in:** 2 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 70, col 26 — pattern `core_fallback`

```typescript
isValidLength(...)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/utils.ts`
- **Range:** line 228, col 16
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
 *
 * @param title string whose length we need to check
 * @param length minimum length the title needs to be
 * @returns boolean if title is of valid length or not
 */
export function isValidLength(title: string, length: number) {
  if (title.length < length) {
    return false;
  }

  return true;
}
```

---

## 7. Sample 2 · callee #6

- **Function:** `createPAT`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/access-token/access-token.service.ts`
- **Callee:** `calculateExpirationDate(createAccessTokenDto.expiryInDays)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 90, col 20 — pattern `anchor_substring`

```typescript
calculateExpirationDate(createAccessTokenDto.expiryInDays)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/utils.ts`
- **Range:** line 308, col 16
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
 * Calculate the expiration date of the token
 *
 * @param expiresOn Number of days the token is valid for
 * @returns Date object of the expiration date
 */
export function calculateExpirationDate(expiresOn: null | number) {
  if (expiresOn === null) return null;
  return new Date(Date.now() + expiresOn * 24 * 60 * 60 * 1000);
}
```

---

## 8. Sample 2 · callee #7

- **Function:** `createPAT`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/access-token/access-token.service.ts`
- **Callee:** `this.TITLE_LENGTH`
- **Status:** OK

### Usage site (matched in test file)

Line 72, col 7 — pattern `anchor_substring`

```typescript
this.TITLE_LENGTH
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/access-token/access-token.service.ts`
- **Range:** line 19, col 2
- **Selection:** `go_to_source_definition_primary`

```typescript
TITLE_LENGTH = 3;
```

---

## 9. Sample 2 · callee #8

- **Function:** `createPAT`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/access-token/access-token.service.ts`
- **Callee:** `HttpStatus.BAD_REQUEST`
- **Status:** OK

### Usage site (matched in test file)

Line 77, col 21 — pattern `anchor_substring`

```typescript
HttpStatus.BAD_REQUEST
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@nestjs+common@11.1.1_class-transformer@0.5.1_class-validator@0.14.2_reflect-metadata@0.2.2_rxjs@7.8.2/node_modules/@nestjs/common/enums/http-status.enum.d.ts`
- **Range:** line 24, col 29

```typescript
BAD_REQUEST = 400,
```

---

## 10. Sample 2 · callee #9

- **Function:** `createPAT`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/access-token/access-token.service.ts`
- **Callee:** `this.prisma`
- **Status:** OK
- **Also seen in:** 3 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 86, col 30 — pattern `anchor_substring`

```typescript
this.prisma
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/access-token/access-token.service.ts`
- **Range:** line 17, col 31
- **Selection:** `go_to_source_definition_primary`

```typescript
  constructor(private readonly prisma: PrismaService) {}
```

---

## 11. Sample 2 · callee #11

- **Function:** `createPAT`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/access-token/access-token.service.ts`
- **Callee:** `this.TOKEN_PREFIX`
- **Status:** OK

### Usage site (matched in test file)

Line 95, col 17 — pattern `anchor_substring`

```typescript
this.TOKEN_PREFIX
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/access-token/access-token.service.ts`
- **Range:** line 21, col 2
- **Selection:** `go_to_source_definition_primary`

```typescript
TOKEN_PREFIX = 'pat-';
```

---

## 12. Sample 3 · callee #0

- **Function:** `deletePAT`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/access-token/access-token.service.ts`
- **Callee:** `this.prisma.personalAccessToken.delete(...)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 110, col 45 — pattern `core_fallback`

```typescript
this.prisma.personalAccessToken.delete(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 22021, col 285

```typescript
/**
     * Delete a PersonalAccessToken.
     * @param {PersonalAccessTokenDeleteArgs} args - Arguments to delete one PersonalAccessToken.
     * @example
     * // Delete one PersonalAccessToken
     * const PersonalAccessToken = await prisma.personalAccessToken.delete({
     *   where: {
     *     // ... filter to delete one PersonalAccessToken
     *   }
     * })
     * 
     */
    delete<T extends PersonalAccessTokenDeleteArgs>(args: SelectSubset<T, PersonalAccessTokenDeleteArgs<ExtArgs>>): Prisma__PersonalAccessTokenClient<$Result.GetResult<Prisma.$PersonalAccessTokenPayload<ExtArgs>, T, "delete", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>
```

---

## 13. Sample 3 · callee #5

- **Function:** `deletePAT`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/access-token/access-token.service.ts`
- **Callee:** `HttpStatus.NOT_FOUND`
- **Status:** OK
- **Also seen in:** 3 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 117, col 21 — pattern `anchor_substring`

```typescript
HttpStatus.NOT_FOUND
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@nestjs+common@11.1.1_class-transformer@0.5.1_class-validator@0.14.2_reflect-metadata@0.2.2_rxjs@7.8.2/node_modules/@nestjs/common/enums/http-status.enum.d.ts`
- **Range:** line 28, col 20

```typescript
NOT_FOUND = 404,
```

---

## 14. Sample 4 · callee #0

- **Function:** `getUserPAT`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/access-token/access-token.service.ts`
- **Callee:** `this.extractUUID(accessToken)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 154, col 28 — pattern `anchor_substring`

```typescript
this.extractUUID(accessToken)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/access-token/access-token.service.ts`
- **Range:** line 56, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Extract UUID from the token
   *
   * @param token Personal Access Token
   * @returns UUID of the token
   */
  private extractUUID(token): string | null {
    if (!token.startsWith(this.TOKEN_PREFIX)) return null;
    return token.slice(this.TOKEN_PREFIX.length);
  }
```

---

## 15. Sample 4 · callee #2

- **Function:** `getUserPAT`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/access-token/access-token.service.ts`
- **Callee:** `this.prisma.personalAccessToken.findUniqueOrThrow(...)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 158, col 61 — pattern `core_fallback`

```typescript
this.prisma.personalAccessToken.findUniqueOrThrow(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 21906, col 302

```typescript
/**
     * Find one PersonalAccessToken that matches the filter or throw an error with `error.code='P2025'`
     * if no matches were found.
     * @param {PersonalAccessTokenFindUniqueOrThrowArgs} args - Arguments to find a PersonalAccessToken
     * @example
     * // Get one PersonalAccessToken
     * const personalAccessToken = await prisma.personalAccessToken.findUniqueOrThrow({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     */
    findUniqueOrThrow<T extends PersonalAccessTokenFindUniqueOrThrowArgs>(args: SelectSubset<T, PersonalAccessTokenFindUniqueOrThrowArgs<ExtArgs>>): Prisma__PersonalAccessTokenClient<$Result.GetResult<Prisma.$PersonalAccessTokenPayload<ExtArgs>, T, "findUniqueOrThrow", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>
```

---

## 16. Sample 5 · callee #2

- **Function:** `updateLastUsedForPAT`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/access-token/access-token.service.ts`
- **Callee:** `this.prisma.personalAccessToken.update(...)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 179, col 72 — pattern `core_fallback`

```typescript
this.prisma.personalAccessToken.update(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 22035, col 280

```typescript
/**
     * Update one PersonalAccessToken.
     * @param {PersonalAccessTokenUpdateArgs} args - Arguments to update one PersonalAccessToken.
     * @example
     * // Update one PersonalAccessToken
     * const personalAccessToken = await prisma.personalAccessToken.update({
     *   where: {
     *     // ... provide filter here
     *   },
     *   data: {
     *     // ... provide data here
     *   }
     * })
     * 
     */
    update<T extends PersonalAccessTokenUpdateArgs>(args: SelectSubset<T, PersonalAccessTokenUpdateArgs<ExtArgs>>): Prisma__PersonalAccessTokenClient<$Result.GetResult<Prisma.$PersonalAccessTokenPayload<ExtArgs>, T, "update", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>
```

---

## 17. Sample 5 · callee #5

- **Function:** `updateLastUsedForPAT`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/access-token/access-token.service.ts`
- **Callee:** `Date()`
- **Status:** OK

### Usage site (matched in test file)

Line 182, col 26 — pattern `anchor_substring`

```typescript
Date()
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es5.d.ts`
- **Range:** line 766, col 23

```typescript
declare var Date: DateConstructor;
```

---

## 18. Sample 6 · callee #0

- **Function:** `fetchUsers`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Callee:** `this.userService.fetchAllUsers(cursorID, take)`
- **Status:** OK

### Usage site (matched in test file)

Line 60, col 28 — pattern `anchor_substring`

```typescript
this.userService.fetchAllUsers(cursorID, take)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/user/user.service.ts`
- **Range:** line 373, col 8
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Fetch all the users in the `User` table based on cursor
   * @param cursorID string of userUID or null
   * @param take number of users to query
   * @returns an array of `User` object
   * @deprecated use fetchAllUsersV2 instead
   */
  async fetchAllUsers(cursorID: string, take: number) {
    const fetchedUsers = await this.prisma.user.findMany({
      skip: cursorID ? 1 : 0,
      take: take,
      cursor: cursorID ? { uid: cursorID } : undefined,
    });
    return fetchedUsers;
  }
```

---

## 19. Sample 6 · callee #1

- **Function:** `fetchUsers`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Callee:** `this.userService`
- **Status:** OK
- **Also seen in:** 5 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 60, col 28 — pattern `anchor_substring`

```typescript
this.userService
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Range:** line 37, col 21
- **Selection:** `go_to_source_definition_primary`

```typescript
private readonly userService: UserService,
```

---

## 20. Sample 7 · callee #1

- **Function:** `revokeUserInvitations`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Callee:** `this.prisma.invitedUsers.deleteMany(...)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 173, col 38 — pattern `core_fallback`

```typescript
this.prisma.invitedUsers.deleteMany(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 17577, col 252

```typescript
/**
     * Delete zero or more InvitedUsers.
     * @param {InvitedUsersDeleteManyArgs} args - Arguments to filter InvitedUsers to delete.
     * @example
     * // Delete a few InvitedUsers
     * const { count } = await prisma.invitedUsers.deleteMany({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     * 
     */
    deleteMany<T extends InvitedUsersDeleteManyArgs>(args?: SelectSubset<T, InvitedUsersDeleteManyArgs<ExtArgs>>): Prisma.PrismaPromise<BatchPayload>
```

---

## 21. Sample 7 · callee #4

- **Function:** `revokeUserInvitations`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Callee:** `validateEmail(email)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 166, col 7 — pattern `anchor_substring`

```typescript
validateEmail(email)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/utils.ts`
- **Range:** line 150, col 13
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
 * Checks to see if the email is valid or not
 * @param email The email
 * @see https://emailregex.com/ for information on email regex
 * @returns A Boolean depending on the format of the email
 */
export const validateEmail = (email: string) => {
  return new RegExp(
    /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/,
  ).test(email);
};
```

---

## 22. Sample 7 · callee #5

- **Function:** `revokeUserInvitations`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Callee:** `this.prisma`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 173, col 13 — pattern `anchor_substring`

```typescript
this.prisma
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Range:** line 44, col 21
- **Selection:** `go_to_source_definition_primary`

```typescript
private readonly prisma: PrismaService,
```

---

## 23. Sample 8 · callee #0

- **Function:** `fetchInvitedUsers`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Callee:** `this.prisma.user.findMany(...)`
- **Status:** OK
- **Also seen in:** 3 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 189, col 50 — pattern `core_fallback`

```typescript
this.prisma.user.findMany(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 10875, col 261

```typescript
/**
     * Find zero or more Users that matches the filter.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {UserFindManyArgs} args - Arguments to filter and select certain fields only.
     * @example
     * // Get all Users
     * const users = await prisma.user.findMany()
     * 
     * // Get first 10 Users
     * const users = await prisma.user.findMany({ take: 10 })
     * 
     * // Only select the `uid`
     * const userWithUidOnly = await prisma.user.findMany({ select: { uid: true } })
     * 
     */
    findMany<T extends UserFindManyArgs>(args?: SelectSubset<T, UserFindManyArgs<ExtArgs>>): Prisma.PrismaPromise<$Result.GetResult<Prisma.$UserPayload<ExtArgs>, T, "findMany", GlobalOmitOptions>>
```

---

## 24. Sample 8 · callee #3

- **Function:** `fetchInvitedUsers`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Callee:** `invitedUsers.findMany`
- **Status:** OK

### Usage site (matched in test file)

Line 195, col 51 — pattern `anchor_substring`

```typescript
invitedUsers.findMany
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 17476, col 293

```typescript
/**
     * Find zero or more InvitedUsers that matches the filter.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {InvitedUsersFindManyArgs} args - Arguments to filter and select certain fields only.
     * @example
     * // Get all InvitedUsers
     * const invitedUsers = await prisma.invitedUsers.findMany()
     * 
     * // Get first 10 InvitedUsers
     * const invitedUsers = await prisma.invitedUsers.findMany({ take: 10 })
     * 
     * // Only select the `adminUid`
     * const invitedUsersWithAdminUidOnly = await prisma.invitedUsers.findMany({ select: { adminUid: true } })
     * 
     */
    findMany<T extends InvitedUsersFindManyArgs>(args?: SelectSubset<T, InvitedUsersFindManyArgs<ExtArgs>>): Prisma.PrismaPromise<$Result.GetResult<Prisma.$InvitedUsersPayload<ExtArgs>, T, "findMany", GlobalOmitOptions>>
```

---

## 25. Sample 9 · callee #0

- **Function:** `membersCountInTeam`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Callee:** `this.teamService.getCountOfMembersInTeam(teamID)`
- **Status:** OK

### Usage site (matched in test file)

Line 236, col 13 — pattern `anchor_substring`

```typescript
this.teamService.getCountOfMembersInTeam(teamID)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/team/team.service.ts`
- **Range:** line 474, col 8
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Get a count of members in a team
   * @param teamID Team ID
   * @returns a count of members in a team
   */
  async getCountOfMembersInTeam(teamID: string) {
    const memberCount = await this.prisma.teamMember.count({
      where: {
        teamID: teamID,
      },
    });

    return memberCount;
  }
```

---

## 26. Sample 9 · callee #1

- **Function:** `membersCountInTeam`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Callee:** `this.teamService`
- **Status:** OK
- **Also seen in:** 4 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 236, col 13 — pattern `anchor_substring`

```typescript
this.teamService
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Range:** line 38, col 21
- **Selection:** `go_to_source_definition_primary`

```typescript
private readonly teamService: TeamService,
```

---

## 27. Sample 10 · callee #0

- **Function:** `environmentCountInTeam`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Callee:** `this.teamEnvironmentsService.totalEnvsInTeam(teamID)`
- **Status:** OK

### Usage site (matched in test file)

Line 269, col 28 — pattern `anchor_substring`

```typescript
this.teamEnvironmentsService.totalEnvsInTeam(teamID)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/team-environments/team-environments.service.ts`
- **Range:** line 240, col 8
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Fetch the count of environments for a given team.
   * @param teamID team id
   * @returns a count of team envs
   */
  async totalEnvsInTeam(teamID: string) {
    const envCount = await this.prisma.teamEnvironment.count({
      where: {
        teamID: teamID,
      },
    });
    return envCount;
  }
```

---

## 28. Sample 10 · callee #1

- **Function:** `environmentCountInTeam`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Callee:** `this.teamEnvironmentsService`
- **Status:** OK

### Usage site (matched in test file)

Line 269, col 28 — pattern `anchor_substring`

```typescript
this.teamEnvironmentsService
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Range:** line 41, col 21
- **Selection:** `go_to_source_definition_primary`

```typescript
private readonly teamEnvironmentsService: TeamEnvironmentsService,
```

---

## 29. Sample 11 · callee #0

- **Function:** `pendingInvitationCountInTeam`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Callee:** `this.teamInvitationService.getTeamInvitations(teamID)`
- **Status:** OK

### Usage site (matched in test file)

Line 280, col 13 — pattern `anchor_substring`

```typescript
this.teamInvitationService.getTeamInvitations(teamID)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/team-invitation/team-invitation.service.ts`
- **Range:** line 240, col 8
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Fetch all team invitations for a given team.
   * @param teamID team id
   * @returns array of team invitations for a team
   */
  async getTeamInvitations(teamID: string) {
    const dbInvitations = await this.prisma.teamInvitation.findMany({
      where: {
        teamID: teamID,
      },
    });

    const invitations: TeamInvitation[] = dbInvitations.map((dbInvitation) =>
      this.cast(dbInvitation),
    );

    return invitations;
  }
```

---

## 30. Sample 11 · callee #1

- **Function:** `pendingInvitationCountInTeam`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Callee:** `this.teamInvitationService`
- **Status:** OK
- **Also seen in:** 2 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 280, col 13 — pattern `anchor_substring`

```typescript
this.teamInvitationService
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Range:** line 42, col 21
- **Selection:** `go_to_source_definition_primary`

```typescript
private readonly teamInvitationService: TeamInvitationService,
```

---

## 31. Sample 12 · callee #0

- **Function:** `removeUserFromTeam`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Callee:** `this.teamService.leaveTeam(teamID, userUid)`
- **Status:** OK

### Usage site (matched in test file)

Line 314, col 31 — pattern `anchor_substring`

```typescript
this.teamService.leaveTeam(teamID, userUid)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/team/team.service.ts`
- **Range:** line 206, col 8
- **Selection:** `go_to_source_definition_primary`

```typescript
  async leaveTeam(
    teamID: string,
    userUid: string,
  ): Promise<E.Left<string> | E.Right<boolean>> {
    const ownerCount = await this.prisma.teamMember.count({
      where: {
        teamID,
        role: TeamAccessRole.OWNER,
      },
    });

    const member = await this.getTeamMember(teamID, userUid);
    if (!member) return E.left(TEAM_INVALID_ID_OR_USER);

    if (ownerCount === 1 && member.role === TeamAccessRole.OWNER) {
      return E.left(TEAM_ONLY_ONE_OWNER);
    }

    try {
      await this.prisma.teamMember.delete({
        where: {
          teamID_userUid: {
            userUid,
            teamID,
          },
        },
      });
    } catch (e) {
      // Record not found
      return E.left(TEAM_INVALID_ID_OR_USER);
    }

    this.pubsub.publish(`team/${teamID}/member_removed`, userUid);

    return E.right(true);
  }
```

---

## 32. Sample 12 · callee #1

- **Function:** `removeUserFromTeam`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Callee:** `E.isLeft(removedUser)`
- **Status:** OK
- **Also seen in:** 27 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 315, col 9 — pattern `anchor_substring`

```typescript
E.isLeft(removedUser)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/fp-ts@2.16.10/node_modules/fp-ts/lib/Either.d.ts`
- **Range:** line 659, col 20
- **Selection:** `external_runtime_resolution_after_ts_nav`

```typescript
/**
 * Returns `true` if the either is an instance of `Left`, `false` otherwise.
 *
 * @category refinements
 * @since 2.0.0
 */
export declare const isLeft: <E>(ma: Either<E, unknown>) => ma is Left<E>
```

### Runtime implementation

- **Export surface:** `node_modules/.pnpm/fp-ts@2.16.10/node_modules/fp-ts/lib/Either.js`

```typescript
/*#__PURE__*/ (0, FromEither_1.fromOption)(exports.FromEither);
// -------------------------------------------------------------------------------------
// refinements
// -------------------------------------------------------------------------------------
/**
 * Returns `true` if the either is an instance of `Left`, `false` otherwise.
 *
 * @category refinements
 * @since 2.0.0
 */
exports.isLeft = _.isLeft;
```

- **Body:** `node_modules/.pnpm/fp-ts@2.16.10/node_modules/fp-ts/lib/internal.js`
- **Range:** line 31, col 0

```typescript
// -------------------------------------------------------------------------------------
// Either
// -------------------------------------------------------------------------------------
/** @internal */
var isLeft = function (ma) { return ma._tag === 'Left'; };
```

---

## 33. Sample 13 · callee #1

- **Function:** `addUserToTeam`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Callee:** `this.userService.findUserByEmail(userEmail)`
- **Status:** OK

### Usage site (matched in test file)

Line 330, col 24 — pattern `anchor_substring`

```typescript
this.userService.findUserByEmail(userEmail)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/user/user.service.ts`
- **Range:** line 65, col 8
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Find User with given email id
   *
   * @param email User's email
   * @returns Option of found User
   */
  async findUserByEmail(email: string): Promise<O.None | O.Some<AuthUser>> {
    const user = await this.prisma.user.findFirst({
      where: {
        email: {
          equals: email,
          mode: 'insensitive',
        },
      },
    });
    if (!user) return O.none;
    return O.some(user);
  }
```

---

## 34. Sample 13 · callee #2

- **Function:** `addUserToTeam`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Callee:** `O.isNone(user)`
- **Status:** OK
- **Also seen in:** 5 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 331, col 9 — pattern `anchor_substring`

```typescript
O.isNone(user)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/fp-ts@2.16.10/node_modules/fp-ts/lib/Option.js`
- **Range:** line 634, col 4
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
 * Returns `true` if the option is `None`, `false` otherwise.
 *
 * @example
 * import { some, none, isNone } from 'fp-ts/Option'
 *
 * assert.strictEqual(isNone(some(1)), false)
 * assert.strictEqual(isNone(none), true)
 *
 * @category refinements
 * @since 2.0.0
 */
var isNone = function (fa) { return fa._tag === 'None'; };
```

---

## 35. Sample 13 · callee #4

- **Function:** `addUserToTeam`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Callee:** `this.teamService.getTeamMemberTE(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 333, col 47 — pattern `core_fallback`

```typescript
this.teamService.getTeamMemberTE(...)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/team/team.service.ts`
- **Range:** line 377, col 2
- **Selection:** `go_to_source_definition_primary`

```typescript
  getTeamMemberTE(teamID: string, userUid: string) {
    return pipe(
      () => this.getTeamMember(teamID, userUid),
      TE.fromTask,
      TE.chain(
        TE.fromPredicate(
          (x): x is TeamMember => !!x,
          () => TEAM_MEMBER_NOT_FOUND,
        ),
      ),
    );
  }
```

---

## 36. Sample 13 · callee #6

- **Function:** `addUserToTeam`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Callee:** `this.teamService.addMemberToTeamWithEmail(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 338, col 48 — pattern `core_fallback`

```typescript
this.teamService.addMemberToTeamWithEmail(...)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/team/team.service.ts`
- **Range:** line 62, col 8
- **Selection:** `go_to_source_definition_primary`

```typescript
  async addMemberToTeamWithEmail(
    teamID: string,
    email: string,
    role: TeamAccessRole,
  ): Promise<E.Left<string> | E.Right<TeamMember>> {
    const user = await this.userService.findUserByEmail(email);
    if (O.isNone(user)) return E.left(USER_NOT_FOUND);

    const teamMember = await this.addMemberToTeam(teamID, user.value.uid, role);
    return E.right(teamMember);
  }
```

---

## 37. Sample 13 · callee #9

- **Function:** `addUserToTeam`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Callee:** `this.teamInvitationService.getTeamInviteByEmailAndTeamID(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 346, col 42 — pattern `core_fallback`

```typescript
this.teamInvitationService.getTeamInviteByEmailAndTeamID(...)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/team-invitation/team-invitation.service.ts`
- **Range:** line 72, col 8
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Get the team invite for an invitee with email and teamID.
   * @param inviteeEmail invitee email
   * @param teamID team id
   * @returns an Either of team invitation for the invitee or error
   */
  async getTeamInviteByEmailAndTeamID(inviteeEmail: string, teamID: string) {
    const isEmailValid = validateEmail(inviteeEmail);
    if (!isEmailValid) return E.left(INVALID_EMAIL);

    try {
      const teamInvite = await this.prisma.teamInvitation.findFirstOrThrow({
        where: {
          inviteeEmail: {
            equals: inviteeEmail,
            mode: 'insensitive',
          },
          teamID,
        },
      });

      return E.right(teamInvite);
    } catch (e) {
      return E.left(TEAM_INVITE_NO_INVITE_FOUND);
    }
  }
```

---

## 38. Sample 13 · callee #10

- **Function:** `addUserToTeam`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Callee:** `E.isRight(userInvitation)`
- **Status:** OK

### Usage site (matched in test file)

Line 351, col 11 — pattern `anchor_substring`

```typescript
E.isRight(userInvitation)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/fp-ts@2.16.10/node_modules/fp-ts/lib/Either.d.ts`
- **Range:** line 666, col 20
- **Selection:** `external_runtime_resolution_after_ts_nav`

```typescript
/**
 * Returns `true` if the either is an instance of `Right`, `false` otherwise.
 *
 * @category refinements
 * @since 2.0.0
 */
export declare const isRight: <A>(ma: Either<unknown, A>) => ma is Right<A>
```

### Runtime implementation

- **Export surface:** `node_modules/.pnpm/fp-ts@2.16.10/node_modules/fp-ts/lib/Either.js`

```typescript
/**
 * Returns `true` if the either is an instance of `Right`, `false` otherwise.
 *
 * @category refinements
 * @since 2.0.0
 */
exports.isRight = _.isRight;
```

- **Body:** `node_modules/.pnpm/fp-ts@2.16.10/node_modules/fp-ts/lib/internal.js`
- **Range:** line 34, col 0

```typescript
/** @internal */
var isRight = function (ma) { return ma._tag === 'Right'; };
```

---

## 39. Sample 13 · callee #11

- **Function:** `addUserToTeam`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Callee:** `this.teamInvitationService.revokeInvitation(...)`
- **Status:** OK
- **Also seen in:** 2 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 352, col 42 — pattern `core_fallback`

```typescript
this.teamInvitationService.revokeInvitation(...)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/team-invitation/team-invitation.service.ts`
- **Range:** line 172, col 8
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Revoke a team invitation
   * @param inviteID invite id
   * @returns an Either of true or error message
   */
  async revokeInvitation(inviteID: string) {
    // check if the invite exists
    const invitation = await this.getInvitation(inviteID);
    if (O.isNone(invitation)) return E.left(TEAM_INVITE_NO_INVITE_FOUND);

    // delete the invite
    await this.prisma.teamInvitation.delete({
      where: {
        id: inviteID,
      },
    });

    this.pubsub.publish(
      `team/${invitation.value.teamID}/invite_removed`,
      invitation.value.id,
    );

    return E.right(true);
  }
```

---

## 40. Sample 14 · callee #0

- **Function:** `renameATeam`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Callee:** `this.teamService.renameTeam(teamID, newName)`
- **Status:** OK

### Usage site (matched in test file)

Line 386, col 31 — pattern `anchor_substring`

```typescript
this.teamService.renameTeam(teamID, newName)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/team/team.service.ts`
- **Range:** line 130, col 8
- **Selection:** `go_to_source_definition_primary`

```typescript
  async renameTeam(
    teamID: string,
    newName: string,
  ): Promise<E.Left<string> | E.Right<Team>> {
    const isValidTitle = this.validateTeamName(newName);
    if (E.isLeft(isValidTitle)) return isValidTitle;

    try {
      const updatedTeam = await this.prisma.team.update({
        where: {
          id: teamID,
        },
        data: {
          name: newName,
        },
      });
      return E.right(updatedTeam);
    } catch (e) {
      // Prisma update errors out if it can't find the record
      return E.left(TEAM_INVALID_ID);
    }
  }
```

---

## 41. Sample 15 · callee #0

- **Function:** `deleteATeam`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Callee:** `this.teamService.deleteTeam(teamID)`
- **Status:** OK

### Usage site (matched in test file)

Line 398, col 30 — pattern `anchor_substring`

```typescript
this.teamService.deleteTeam(teamID)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/team/team.service.ts`
- **Range:** line 102, col 8
- **Selection:** `go_to_source_definition_primary`

```typescript
  async deleteTeam(teamID: string): Promise<E.Left<string> | E.Right<boolean>> {
    const team = await this.prisma.team.findUnique({
      where: {
        id: teamID,
      },
    });
    if (!team) return E.left(TEAM_INVALID_ID);

    await this.prisma.teamMember.deleteMany({
      where: {
        teamID: teamID,
      },
    });

    await this.prisma.team.delete({
      where: {
        id: teamID,
      },
    });

    return E.right(true);
  }
```

---

## 42. Sample 16 · callee #0

- **Function:** `fetchAdmins`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Callee:** `this.userService.fetchAdminUsers()`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 409, col 20 — pattern `anchor_substring`

```typescript
this.userService.fetchAdminUsers()
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/user/user.service.ts`
- **Range:** line 470, col 8
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Fetch all the admin users
   * @returns an array of admin users
   */
  async fetchAdminUsers() {
    const admins = this.prisma.user.findMany({
      where: {
        isAdmin: true,
      },
    });

    return admins;
  }
```

---

## 43. Sample 17 · callee #0

- **Function:** `removeUserAccount`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Callee:** `this.userService.findUserById(userUid)`
- **Status:** OK

### Usage site (matched in test file)

Line 432, col 24 — pattern `anchor_substring`

```typescript
this.userService.findUserById(userUid)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/user/user.service.ts`
- **Range:** line 84, col 8
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Find User with given ID
   *
   * @param userUid User ID
   * @returns Option of found User
   */
  async findUserById(userUid: string): Promise<O.None | O.Some<AuthUser>> {
    try {
      const user = await this.prisma.user.findUniqueOrThrow({
        where: {
          uid: userUid,
        },
      });
      return O.some(user);
    } catch (error) {
      return O.none;
    }
  }
```

---

## 44. Sample 17 · callee #4

- **Function:** `removeUserAccount`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Callee:** `this.userService.deleteUserByUID(user.value)`
- **Status:** OK

### Usage site (matched in test file)

Line 437, col 27 — pattern `anchor_substring`

```typescript
this.userService.deleteUserByUID(user.value)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/user/user.service.ts`
- **Range:** line 528, col 2
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Deletes a user by UID
   * @param user User Object
   * @returns an TaskEither of string  or boolean
   */
  deleteUserByUID(user: AuthUser) {
    return pipe(
      this.getUserDeletionErrors(user),
      TO.matchEW(
        () =>
          pipe(
            this.userDataHandlers,
            A.map((handler) => handler.onUserDelete(user)),
            T.sequenceArray,
            T.map(constVoid),
            TE.fromTask,
          ) as TE.TaskEither<never, void>,
        (errors): TE.TaskEither<string[], void> => TE.left(errors),
      ),

      TE.chainW(() => () => this.deleteUserAccount(user.uid)),

      TE.chainFirst(() =>
        TE.fromTask(() =>
          this.pubsub.publish(`user/${user.uid}/deleted`, <User>{
            uid: user.uid,
            displayName: user.displayName,
            email: user.email,
            photoURL: user.photoURL,
            isAdmin: user.isAdmin,
            createdOn: user.createdOn,
            currentGQLSession: user.currentGQLSession,
            currentRESTSession: user.currentRESTSession,
          }),
        ),
      ),

      TE.mapLeft((errors) => errors.toString()),
    );
  }
```

---

## 45. Sample 18 · callee #0

- **Function:** `makeUsersAdmin`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Callee:** `this.userService.makeAdmins(userUIDs)`
- **Status:** OK

### Usage site (matched in test file)

Line 522, col 29 — pattern `anchor_substring`

```typescript
this.userService.makeAdmins(userUIDs)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/user/user.service.ts`
- **Range:** line 454, col 8
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Change users to admins by toggling isAdmin param to true
   * @param userUID user UIDs
   * @returns a Either of true or error
   */
  async makeAdmins(userUIDs: string[]) {
    try {
      await this.prisma.user.updateMany({
        where: { uid: { in: userUIDs } },
        data: { isAdmin: true },
      });
      return E.right(true);
    } catch (error) {
      return E.left(USER_UPDATE_FAILED);
    }
  }
```

---

## 46. Sample 19 · callee #2

- **Function:** `removeUserAsAdmin`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Callee:** `this.userService.removeUserAsAdmin(userUID)`
- **Status:** OK

### Usage site (matched in test file)

Line 537, col 25 — pattern `anchor_substring`

```typescript
this.userService.removeUserAsAdmin(userUID)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/user/user.service.ts`
- **Range:** line 569, col 8
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Change the user from an admin by toggling isAdmin param to false
   * @param userUID user UID
   * @returns a Either of `User` object or error
   */
  async removeUserAsAdmin(userUID: string) {
    try {
      const user = await this.prisma.user.update({
        where: {
          uid: userUID,
        },
        data: {
          isAdmin: false,
        },
      });
      return E.right(user);
    } catch (error) {
      return E.left(USER_NOT_FOUND);
    }
  }
```

---

## 47. Sample 21 · callee #0

- **Function:** `deleteAllUserHistory`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Callee:** `this.userHistoryService.deleteAllHistories()`
- **Status:** OK

### Usage site (matched in test file)

Line 660, col 26 — pattern `anchor_substring`

```typescript
this.userHistoryService.deleteAllHistories()
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/user-history/user-history.service.ts`
- **Range:** line 195, col 8
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Delete all user history from DB
   * @returns a boolean
   */
  async deleteAllHistories() {
    try {
      await this.prisma.userHistory.deleteMany();
    } catch (error) {
      return E.left(USER_HISTORY_DELETION_FAILED);
    }

    this.pubsub.publish('user_history/all/deleted', true);
    return E.right(true);
  }
```

---

## 48. Sample 21 · callee #4

- **Function:** `deleteAllUserHistory`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Callee:** `this.userHistoryService`
- **Status:** OK

### Usage site (matched in test file)

Line 660, col 26 — pattern `anchor_substring`

```typescript
this.userHistoryService
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/admin/admin.service.ts`
- **Range:** line 48, col 21
- **Selection:** `go_to_source_definition_primary`

```typescript
private readonly userHistoryService: UserHistoryService,
```

---

## 49. Sample 22 · callee #0

- **Function:** `generateMagicLinkTokens`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/auth/auth.service.ts`
- **Callee:** `bcrypt.genSalt(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 52, col 31 — pattern `core_fallback`

```typescript
bcrypt.genSalt(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/bcrypt@6.0.0/node_modules/bcrypt/bcrypt.js`
- **Range:** line 30, col 9
- **Selection:** `go_to_source_definition_primary`

```typescript
/// generate a salt
/// @param {Number} [rounds] number of rounds (default 10)
/// @param {Function} cb callback(err, salt)
function genSalt(rounds, minor, cb) {
    let error;

    // if callback is first argument, then use defaults for others
    if (typeof arguments[0] === 'function') {
        // have to set callback first otherwise arguments are overridden
        cb = arguments[0];
        rounds = 10;
        minor = 'b';
        // callback is second argument
    } else if (typeof arguments[1] === 'function') {
        // have to set callback first otherwise arguments are overridden
        cb = arguments[1];
        minor = 'b';
    }

    if (!cb) {
        return promises.promise(genSalt, this, [rounds, minor]);
    }

    // default 10 rounds
    if (!rounds) {
        rounds = 10;
    } else if (typeof rounds !== 'number') {
        // callback error asynchronously
        error = new Error('rounds must be a number');
        return process.nextTick(function () {
            cb(error);
        });
    }

    if (!minor) {
        minor = 'b'
    } else if (minor !== 'b' && minor !== 'a') {
        error = new Error('minor must be either "a" or "b"');
        return process.nextTick(function () {
            cb(error);
        });
    }

    crypto.randomBytes(16, function (error, randomBytes) {
        if (error) {
            cb(error);
            return;
        }

        bindings.gen_salt(minor, rounds, randomBytes, cb);
    });
}
```

---

## 50. Sample 22 · callee #1

- **Function:** `generateMagicLinkTokens`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/auth/auth.service.ts`
- **Callee:** `this.configService.get('TOKEN_SALT_COMPLEXITY')`
- **Status:** OK
- **Also seen in:** 5 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 53, col 16 — pattern `anchor_substring`

```typescript
this.configService.get('TOKEN_SALT_COMPLEXITY')
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@nestjs+config@4.0.2_@nestjs+common@11.1.1_class-transformer@0.5.1_class-validator@0.14_51d8e439a37a012ddbcfadb29c8865f1/node_modules/@nestjs/config/dist/config.service.d.ts`
- **Range:** line 40, col 75
- **Selection:** `external_runtime_resolution_after_ts_nav`

```typescript
/**
     * Get a configuration value (either custom configuration or process environment variable)
     * based on property path (you can use dot notation to traverse nested object, e.g. "database.host").
     * @param propertyPath
     */
    get<T = any>(propertyPath: KeyOf<K>): ValidatedResult<WasValidated, T>;
```

### Runtime implementation

- **Body:** `node_modules/.pnpm/@nestjs+config@4.0.2_@nestjs+common@11.1.1_class-transformer@0.5.1_class-validator@0.14_51d8e439a37a012ddbcfadb29c8865f1/node_modules/@nestjs/config/dist/config.service.js`
- **Range:** line 98, col 0

```typescript
/**
     * Get a configuration value (either custom configuration or process environment variable)
     * based on property path (you can use dot notation to traverse nested object, e.g. "database.host").
     * It returns a default value if the key does not exist.
     * @param propertyPath
     * @param defaultValueOrOptions
     */
    get(propertyPath, defaultValueOrOptions, options) {
        const internalValue = this.getFromInternalConfig(propertyPath);
        if (!(0, shared_utils_1.isUndefined)(internalValue)) {
            return internalValue;
        }
        const validatedEnvValue = this.getFromValidatedEnv(propertyPath);
        if (!(0, shared_utils_1.isUndefined)(validatedEnvValue)) {
            return validatedEnvValue;
        }
        const defaultValue = this.isGetOptionsObject(defaultValueOrOptions) &&
            !options
            ? undefined
            : defaultValueOrOptions;
        if (!this._skipProcessEnv) {
            const processEnvValue = this.getFromProcessEnv(propertyPath, defaultValue);
            if (!(0, shared_utils_1.isUndefined)(processEnvValue)) {
                return processEnvValue;
            }
        }
        return defaultValue;
    }
```

---

## 51. Sample 22 · callee #2

- **Function:** `generateMagicLinkTokens`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/auth/auth.service.ts`
- **Callee:** `DateTime.now()`
- **Status:** OK

### Usage site (matched in test file)

Line 55, col 23 — pattern `anchor_substring`

```typescript
DateTime.now()
```

### Resolved definition

- **Path:** `node_modules/.pnpm/luxon@3.6.1/node_modules/luxon/build/node/luxon.js`
- **Range:** line 5727, col 9
- **Selection:** `go_to_source_definition_primary`

```typescript
// CONSTRUCT

  /**
   * Create a DateTime for the current instant, in the system's time zone.
   *
   * Use Settings to override these default values if needed.
   * @example DateTime.now().toISO() //~> now in the ISO format
   * @return {DateTime}
   */
  static now() {
    return new DateTime({});
  }
```

---

## 52. Sample 22 · callee #4

- **Function:** `generateMagicLinkTokens`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/auth/auth.service.ts`
- **Callee:** `this.prisma.verificationToken.create(...)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 62, col 57 — pattern `core_fallback`

```typescript
this.prisma.verificationToken.create(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 13278, col 235

```typescript
/**
     * Create a VerificationToken.
     * @param {VerificationTokenCreateArgs} args - Arguments to create a VerificationToken.
     * @example
     * // Create one VerificationToken
     * const VerificationToken = await prisma.verificationToken.create({
     *   data: {
     *     // ... data to create a VerificationToken
     *   }
     * })
     * 
     */
    create<T extends VerificationTokenCreateArgs>(args: SelectSubset<T, VerificationTokenCreateArgs<ExtArgs>>): Prisma__VerificationTokenClient<$Result.GetResult<Prisma.$VerificationTokenPayload<ExtArgs>, T, "create", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>
```

---

## 53. Sample 22 · callee #5

- **Function:** `generateMagicLinkTokens`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/auth/auth.service.ts`
- **Callee:** `parseInt(this.configService.get('TOKEN_SALT_COMPLEXITY'))`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 53, col 7 — pattern `anchor_substring`

```typescript
parseInt(this.configService.get('TOKEN_SALT_COMPLEXITY'))
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es5.d.ts`
- **Range:** line 30, col 38

```typescript
/**
 * Converts a string to an integer.
 * @param string A string to convert into a number.
 * @param radix A value between 2 and 36 that specifies the base of the number in `string`.
 * If this argument is not supplied, strings with a prefix of '0x' are considered hexadecimal.
 * All other strings are considered decimal.
 */
declare function parseInt(string: string, radix?: number): number;
```

---

## 54. Sample 22 · callee #7

- **Function:** `generateMagicLinkTokens`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/auth/auth.service.ts`
- **Callee:** `this.configService`
- **Status:** OK
- **Also seen in:** 2 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 53, col 16 — pattern `anchor_substring`

```typescript
this.configService
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/auth/auth.service.ts`
- **Range:** line 40, col 21
- **Selection:** `go_to_source_definition_primary`

```typescript
private readonly configService: ConfigService,
```

---

## 55. Sample 22 · callee #8

- **Function:** `generateMagicLinkTokens`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/auth/auth.service.ts`
- **Callee:** `this.prisma`
- **Status:** OK

### Usage site (matched in test file)

Line 62, col 27 — pattern `anchor_substring`

```typescript
this.prisma
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/auth/auth.service.ts`
- **Range:** line 37, col 21
- **Selection:** `go_to_source_definition_primary`

```typescript
private readonly prisma: PrismaService,
```

---

## 56. Sample 23 · callee #1

- **Function:** `generateRefreshToken`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/auth/auth.service.ts`
- **Callee:** `this.jwtService.sign(...)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 108, col 48 — pattern `core_fallback`

```typescript
this.jwtService.sign(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@nestjs+jwt@11.0.0_@nestjs+common@11.1.1_class-transformer@0.5.1_class-validator@0.14.2_61ebb541c64dd4afa81c37c3cd2a2e7f/node_modules/@nestjs/jwt/dist/jwt.service.d.ts`
- **Range:** line 5, col 44
- **Selection:** `external_runtime_resolution_after_ts_nav`

```typescript
    sign(payload: string, options?: Omit<JwtSignOptions, keyof jwt.SignOptions>): string;
    sign(payload: Buffer | object, options?: JwtSignOptions): string;
```

### Runtime implementation

- **Body:** `node_modules/.pnpm/@nestjs+jwt@11.0.0_@nestjs+common@11.1.1_class-transformer@0.5.1_class-validator@0.14.2_61ebb541c64dd4afa81c37c3cd2a2e7f/node_modules/@nestjs/jwt/dist/jwt.service.js`
- **Range:** line 25, col 0

```typescript
    sign(payload, options) {
        const signOptions = this.mergeJwtOptions({ ...options }, 'signOptions');
        const secret = this.getSecretKey(payload, options, 'privateKey', interfaces_1.JwtSecretRequestType.SIGN);
        if (secret instanceof Promise) {
            secret.catch(() => { });
            this.logger.warn('For async version of "secretOrKeyProvider", please use "signAsync".');
            throw new jwt_errors_1.WrongSecretProviderError();
        }
        const allowedSignOptKeys = ['secret', 'privateKey'];
        const signOptKeys = Object.keys(signOptions);
        if (typeof payload === 'string' &&
            signOptKeys.some((k) => !allowedSignOptKeys.includes(k))) {
            throw new Error('Payload as string is not allowed with the following sign options: ' +
                signOptKeys.join(', '));
        }
        return jwt.sign(payload, secret, signOptions);
    }
```

---

## 57. Sample 23 · callee #3

- **Function:** `generateRefreshToken`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/auth/auth.service.ts`
- **Callee:** `argon2.hash(refreshToken)`
- **Status:** OK

### Usage site (matched in test file)

Line 112, col 36 — pattern `anchor_substring`

```typescript
argon2.hash(refreshToken)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/argon2@0.43.0/node_modules/argon2/argon2.cjs`
- **Range:** line 63, col 11
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
 * @typedef {Object} Options
 * @property {number} [hashLength=32]
 * @property {number} [timeCost=3]
 * @property {number} [memoryCost=65536]
 * @property {number} [parallelism=4]
 * @property {keyof typeof names} [type=argon2id]
 * @property {number} [version=19]
 * @property {Buffer} [salt]
 * @property {Buffer} [associatedData]
 * @property {Buffer} [secret]
 */

/**
 * Hashes a password with Argon2, producing a raw hash
 *
 * @overload
 * @param {Buffer | string} password The plaintext password to be hashed
 * @param {Options & { raw: true }} options The parameters for Argon2
 * @returns {Promise<Buffer>} The raw hash generated from `password`
 */
/**
 * Hashes a password with Argon2, producing an encoded hash
 *
 * @overload
 * @param {Buffer | string} password The plaintext password to be hashed
 * @param {Options & { raw?: boolean }} [options] The parameters for Argon2
 * @returns {Promise<string>} The encoded hash generated from `password`
 */
/**
 * @param {Buffer | string} password The plaintext password to be hashed
 * @param {Options & { raw?: boolean }} [options] The parameters for Argon2
 */
async function hash(password, options) {
  let { raw, salt, ...rest } = { ...defaults, ...options };

  if (rest.hashLength > 2 ** 32 - 1) {
    throw new RangeError("Hash length is too large");
  }

  if (rest.memoryCost > 2 ** 32 - 1) {
    throw new RangeError("Memory cost is too large");
  }

  if (rest.timeCost > 2 ** 32 - 1) {
    throw new RangeError("Time cost is too large");
  }

  if (rest.parallelism > 2 ** 24 - 1) {
    throw new RangeError("Parallelism is too large");
  }

  salt = salt ?? (await generateSalt(16));

  const {
    hashLength,
    secret = Buffer.alloc(0),
    type,
    version,
    memoryCost: m,
    timeCost: t,
    parallelism: p,
    associatedData: data = Buffer.alloc(0),
  } = rest;

  const hash = await bindingsHash({
    password: Buffer.from(password),
    salt,
    secret,
    data,
    hashLength,
    m,
    t,
    p,
    version,
    type,
  });
  if (raw) {
    return hash;
  }

  return serialize({
    id: names[type],
    version,
    params: { m, t, p, ...(data.byteLength > 0 ? { data } : {}) },
    salt,
    hash,
  });
}
```

---

## 58. Sample 23 · callee #4

- **Function:** `generateRefreshToken`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/auth/auth.service.ts`
- **Callee:** `this.usersService.updateUserRefreshToken(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 114, col 49 — pattern `core_fallback`

```typescript
this.usersService.updateUserRefreshToken(...)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/user/user.service.ts`
- **Range:** line 118, col 8
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Update User with new generated hashed refresh token
   *
   * @param refreshTokenHash Hash of newly generated refresh token
   * @param userUid User uid
   * @returns Either of User with updated refreshToken
   */
  async updateUserRefreshToken(refreshTokenHash: string, userUid: string) {
    try {
      const user = await this.prisma.user.update({
        where: {
          uid: userUid,
        },
        data: {
          refreshToken: refreshTokenHash,
        },
      });

      return E.right(user);
    } catch (error) {
      return E.left(USER_NOT_FOUND);
    }
  }
```

---

## 59. Sample 23 · callee #9

- **Function:** `generateRefreshToken`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/auth/auth.service.ts`
- **Callee:** `this.jwtService`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 108, col 32 — pattern `anchor_substring`

```typescript
this.jwtService
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/auth/auth.service.ts`
- **Range:** line 38, col 21
- **Selection:** `go_to_source_definition_primary`

```typescript
private readonly jwtService: JwtService,
```

---

## 60. Sample 23 · callee #10

- **Function:** `generateRefreshToken`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/auth/auth.service.ts`
- **Callee:** `this.usersService`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 114, col 31 — pattern `anchor_substring`

```typescript
this.usersService
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/auth/auth.service.ts`
- **Range:** line 36, col 21
- **Selection:** `go_to_source_definition_primary`

```typescript
private readonly usersService: UserService,
```

---

## 61. Sample 24 · callee #1

- **Function:** `generateAuthTokens`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/auth/auth.service.ts`
- **Callee:** `this.generateRefreshToken(userUid)`
- **Status:** OK

### Usage site (matched in test file)

Line 140, col 32 — pattern `anchor_substring`

```typescript
this.generateRefreshToken(userUid)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/auth/auth.service.ts`
- **Range:** line 92, col 3

```typescript
/**
   * Generate new refresh token for user
   *
   * @param userUid User Id
   * @returns Generated refreshToken
   */
  private async generateRefreshToken(userUid: string) {
    const refreshTokenPayload: RefreshTokenPayload = {
      iss: this.configService.get('VITE_BASE_URL'),
      sub: userUid,
      aud: [this.configService.get('VITE_BASE_URL')],
    };

    const refreshToken = await this.jwtService.sign(refreshTokenPayload, {
      expiresIn: this.configService.get('REFRESH_TOKEN_VALIDITY'), //7 Days
    });

    const refreshTokenHash = await argon2.hash(refreshToken);

    const updatedUser = await this.usersService.updateUserRefreshToken(
      refreshTokenHash,
      userUid,
    );
    if (E.isLeft(updatedUser))
      return E.left(<RESTError>{
        message: updatedUser.left,
        statusCode: HttpStatus.NOT_FOUND,
      });

    return E.right(refreshToken);
  }
```

---

## 62. Sample 25 · callee #1

- **Function:** `refreshAuthTokens`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/auth/auth.service.ts`
- **Callee:** `argon2.verify(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 342, col 41 — pattern `core_fallback`

```typescript
argon2.verify(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/argon2@0.43.0/node_modules/argon2/argon2.cjs`
- **Range:** line 159, col 11
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
 * @param {string} digest The digest to be checked
 * @param {Buffer | string} password The plaintext password to be verified
 * @param {Object} [options] The current parameters for Argon2
 * @param {Buffer} [options.secret]
 * @returns {Promise<boolean>} `true` if the digest parameters matches the hash generated from `password`, otherwise `false`
 */
async function verify(digest, password, options = {}) {
  const { id, ...rest } = deserialize(digest);
  if (!(id in types)) {
    return false;
  }

  const {
    version = 0x10,
    params: { m, t, p, data = "" },
    salt,
    hash,
  } = rest;

  const { secret = Buffer.alloc(0) } = options;

  return timingSafeEqual(
    await bindingsHash({
      password: Buffer.from(password),
      salt,
      secret,
      data: Buffer.from(data, "base64"),
      hashLength: hash.byteLength,
      m: +m,
      t: +t,
      p: +p,
      version: +version,
      type: types[id],
    }),
    hash,
  );
}
```

---

## 63. Sample 25 · callee #2

- **Function:** `refreshAuthTokens`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/auth/auth.service.ts`
- **Callee:** `this.generateAuthTokens(user.uid)`
- **Status:** OK

### Usage site (matched in test file)

Line 353, col 39 — pattern `anchor_substring`

```typescript
this.generateAuthTokens(user.uid)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/auth/auth.service.ts`
- **Range:** line 132, col 8
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Generate access and refresh token pair
   *
   * @param userUid User ID
   * @returns Either of generated AuthTokens
   */
  async generateAuthTokens(userUid: string) {
    const accessTokenPayload: AccessTokenPayload = {
      iss: this.configService.get('VITE_BASE_URL'),
      sub: userUid,
      aud: [this.configService.get('VITE_BASE_URL')],
    };

    const refreshToken = await this.generateRefreshToken(userUid);
    if (E.isLeft(refreshToken)) return E.left(refreshToken.left);

    return E.right(<AuthTokens>{
      access_token: await this.jwtService.sign(accessTokenPayload, {
        expiresIn: this.configService.get('ACCESS_TOKEN_VALIDITY'), //1 Day
      }),
      refresh_token: refreshToken.right,
    });
  }
```

---

## 64. Sample 26 · callee #1

- **Function:** `verifyAdmin`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/auth/auth.service.ts`
- **Callee:** `this.usersService.getUsersCount()`
- **Status:** OK

### Usage site (matched in test file)

Line 372, col 30 — pattern `anchor_substring`

```typescript
this.usersService.getUsersCount()
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/user/user.service.ts`
- **Range:** line 423, col 8
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Fetch the number of users in db
   * @returns a count (Int) of user records in DB
   */
  async getUsersCount() {
    const usersCount = await this.prisma.user.count();
    return usersCount;
  }
```

---

## 65. Sample 26 · callee #2

- **Function:** `verifyAdmin`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/auth/auth.service.ts`
- **Callee:** `this.usersService.makeAdmin(user.uid)`
- **Status:** OK

### Usage site (matched in test file)

Line 374, col 34 — pattern `anchor_substring`

```typescript
this.usersService.makeAdmin(user.uid)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/user/user.service.ts`
- **Range:** line 433, col 8
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Change a user to an admin by toggling isAdmin param to true
   * @param userUID user UID
   * @returns a Either of `User` object or error
   */
  async makeAdmin(userUID: string) {
    try {
      const elevatedUser = await this.prisma.user.update({
        where: {
          uid: userUID,
        },
        data: {
          isAdmin: true,
        },
      });
      return E.right(elevatedUser);
    } catch (error) {
      return E.left(USER_NOT_FOUND);
    }
  }
```

---

## 66. Sample 27 · callee #0

- **Function:** `updateMany`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/infra-config/infra-config.service.ts`
- **Callee:** `this.EXCLUDE_FROM_UPDATE_CONFIGS.includes(infraConfigs[i].name)`
- **Status:** OK

### Usage site (matched in test file)

Line 215, col 11 — pattern `anchor_substring`

```typescript
this.EXCLUDE_FROM_UPDATE_CONFIGS.includes(infraConfigs[i].name)
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es2016.array.include.d.ts`
- **Range:** line 16, col 20

```typescript
/**
     * Determines whether an array includes a certain element, returning true or false as appropriate.
     * @param searchElement The element to search for.
     * @param fromIndex The position in this array at which to begin searching for searchElement.
     */
    includes(searchElement: T, fromIndex?: number): boolean;
```

---

## 67. Sample 27 · callee #2

- **Function:** `updateMany`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/infra-config/infra-config.service.ts`
- **Callee:** `this.validateEnvValues(infraConfigs)`
- **Status:** OK

### Usage site (matched in test file)

Line 219, col 24 — pattern `anchor_substring`

```typescript
this.validateEnvValues(infraConfigs)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/infra-config/infra-config.service.ts`
- **Range:** line 526, col 2
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Validate the values of the InfraConfigs
   */
  validateEnvValues(
    infraConfigs: {
      name: InfraConfigEnum;
      value: string;
    }[],
  ) {
    for (let i = 0; i < infraConfigs.length; i++) {
      switch (infraConfigs[i].name) {
        case InfraConfigEnum.MAILER_SMTP_ENABLE:
          if (
            infraConfigs[i].value !== 'true' &&
            infraConfigs[i].value !== 'false'
          )
            return E.left(INFRA_CONFIG_INVALID_INPUT);
          break;
        case InfraConfigEnum.MAILER_USE_CUSTOM_CONFIGS:
          if (
            infraConfigs[i].value !== 'true' &&
            infraConfigs[i].value !== 'false'
          )
            return E.left(INFRA_CONFIG_INVALID_INPUT);
          break;
        case InfraConfigEnum.MAILER_SMTP_URL:
          const isValidUrl = validateSMTPUrl(infraConfigs[i].value);
          if (!isValidUrl) return E.left(INFRA_CONFIG_INVALID_INPUT);
          break;
        case InfraConfigEnum.MAILER_ADDRESS_FROM:
          const isValidEmail = validateSMTPEmail(infraConfigs[i].value);
          if (!isValidEmail) return E.left(INFRA_CONFIG_INVALID_INPUT);
          break;
        case InfraConfigEnum.MAILER_SMTP_HOST:
          if (!infraConfigs[i].value) return E.left(INFRA_CONFIG_INVALID_INPUT);
          break;
        case InfraConfigEnum.MAILER_SMTP_PORT:
          if (!infraConfigs[i].value) return E.left(INFRA_CONFIG_INVALID_INPUT);
          break;
        case InfraConfigEnum.MAILER_SMTP_SECURE:
          if (
            infraConfigs[i].value !== 'true' &&
            infraConfigs[i].value !== 'false'
          )
            return E.left(INFRA_CONFIG_INVALID_INPUT);
          break;
        case InfraConfigEnum.MAILER_SMTP_USER:
          if (!infraConfigs[i].value) return E.left(INFRA_CONFIG_INVALID_INPUT);
          break;
        case InfraConfigEnum.MAILER_SMTP_PASSWORD:
          if (!infraConfigs[i].value) return E.left(INFRA_CONFIG_INVALID_INPUT);
          break;
        case InfraConfigEnum.MAILER_TLS_REJECT_UNAUTHORIZED:
          if (
            infraConfigs[i].value !== 'true' &&
            infraConfigs[i].value !== 'false'
          )
            return E.left(INFRA_CONFIG_INVALID_INPUT);
          break;
        case InfraConfigEnum.GOOGLE_CLIENT_ID:
          if (!infraConfigs[i].value) return E.left(INFRA_CONFIG_INVALID_INPUT);
          break;
        case InfraConfigEnum.GOOGLE_CLIENT_SECRET:
          if (!infraConfigs[i].value) return E.left(INFRA_CONFIG_INVALID_INPUT);
          break;
        case InfraConfigEnum.GOOGLE_CALLBACK_URL:
          if (!validateUrl(infraConfigs[i].value))
            return E.left(INFRA_CONFIG_INVALID_INPUT);
          break;
        case InfraConfigEnum.GOOGLE_SCOPE:
          if (!infraConfigs[i].value) return E.left(INFRA_CONFIG_INVALID_INPUT);
          break;
        case InfraConfigEnum.GITHUB_CLIENT_ID:
          if (!infraConfigs[i].value) return E.left(INFRA_CONFIG_INVALID_INPUT);
          break;
        case InfraConfigEnum.GITHUB_CLIENT_SECRET:
          if (!infraConfigs[i].value) return E.left(INFRA_CONFIG_INVALID_INPUT);
          break;
        case InfraConfigEnum.GITHUB_CALLBACK_URL:
          if (!validateUrl(infraConfigs[i].value))
            return E.left(INFRA_CONFIG_INVALID_INPUT);
          break;
        case InfraConfigEnum.GITHUB_SCOPE:
          if (!infraConfigs[i].value) return E.left(INFRA_CONFIG_INVALID_INPUT);
          break;
        case InfraConfigEnum.MICROSOFT_CLIENT_ID:
          if (!infraConfigs[i].value) return E.left(INFRA_CONFIG_INVALID_INPUT);
          break;
        case InfraConfigEnum.MICROSOFT_CLIENT_SECRET:
          if (!infraConfigs[i].value) return E.left(INFRA_CONFIG_INVALID_INPUT);
          break;
        case InfraConfigEnum.MICROSOFT_CALLBACK_URL:
          if (!validateUrl(infraConfigs[i].value))
            return E.left(INFRA_CONFIG_INVALID_INPUT);
          break;
        case InfraConfigEnum.MICROSOFT_SCOPE:
          if (!infraConfigs[i].value) return E.left(INFRA_CONFIG_INVALID_INPUT);
          break;
        case InfraConfigEnum.MICROSOFT_TENANT:
          if (!infraConfigs[i].value) return E.left(INFRA_CONFIG_INVALID_INPUT);
          break;
        default:
          break;
      }
    }

    return E.right(true);
  }
```

---

## 68. Sample 27 · callee #5

- **Function:** `updateMany`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/infra-config/infra-config.service.ts`
- **Callee:** `this.prisma.infraConfig.findMany(...)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 223, col 59 — pattern `core_fallback`

```typescript
this.prisma.infraConfig.findMany(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 20916, col 289

```typescript
/**
     * Find zero or more InfraConfigs that matches the filter.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {InfraConfigFindManyArgs} args - Arguments to filter and select certain fields only.
     * @example
     * // Get all InfraConfigs
     * const infraConfigs = await prisma.infraConfig.findMany()
     * 
     * // Get first 10 InfraConfigs
     * const infraConfigs = await prisma.infraConfig.findMany({ take: 10 })
     * 
     * // Only select the `id`
     * const infraConfigWithIdOnly = await prisma.infraConfig.findMany({ select: { id: true } })
     * 
     */
    findMany<T extends InfraConfigFindManyArgs>(args?: SelectSubset<T, InfraConfigFindManyArgs<ExtArgs>>): Prisma.PrismaPromise<$Result.GetResult<Prisma.$InfraConfigPayload<ExtArgs>, T, "findMany", GlobalOmitOptions>>
```

---

## 69. Sample 27 · callee #6

- **Function:** `updateMany`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/infra-config/infra-config.service.ts`
- **Callee:** `this.prisma.$transaction(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 227, col 25 — pattern `core_fallback`

```typescript
this.prisma.$transaction(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 241, col 89

```typescript


  /**
   * Allows the running of a sequence of read/write operations that are guaranteed to either succeed or fail as a whole.
   * @example
   * ```
   * const [george, bob, alice] = await prisma.$transaction([
   *   prisma.user.create({ data: { name: 'George' } }),
   *   prisma.user.create({ data: { name: 'Bob' } }),
   *   prisma.user.create({ data: { name: 'Alice' } }),
   * ])
   * ```
   * 
   * Read more in our [docs](https://www.prisma.io/docs/concepts/components/prisma-client/transactions).
   */
  $transaction<P extends Prisma.PrismaPromise<any>[]>(arg: [...P], options?: { isolationLevel?: Prisma.TransactionIsolationLevel }): $Utils.JsPromise<runtime.Types.Utils.UnwrapTuple<P>>

  $transaction<R>(fn: (prisma: Omit<PrismaClient, runtime.ITXClientDenyList>) => $Utils.JsPromise<R>, options?: { maxWait?: number, timeout?: number, isolationLevel?: Prisma.TransactionIsolationLevel }): $Utils.JsPromise<R>
```

---

## 70. Sample 27 · callee #9

- **Function:** `updateMany`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/infra-config/infra-config.service.ts`
- **Callee:** `encrypt(infraConfigs[i].value)`
- **Status:** OK

### Usage site (matched in test file)

Line 237, col 19 — pattern `anchor_substring`

```typescript
encrypt(infraConfigs[i].value)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/utils.ts`
- **Range:** line 341, col 16
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
 * Encrypts a text using a key
 * @param text The text to encrypt
 * @param key The key to use for encryption
 * @returns The encrypted text
 */
export function encrypt(text: string, key = process.env.DATA_ENCRYPTION_KEY) {
  if (!key) throw new Error(ENV_NOT_FOUND_KEY_DATA_ENCRYPTION_KEY);

  if (text === null || text === undefined) return text;

  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv(
    ENCRYPTION_ALGORITHM,
    Buffer.from(key),
    iv,
  );
  let encrypted = cipher.update(text);
  encrypted = Buffer.concat([encrypted, cipher.final()]);
  return iv.toString('hex') + ':' + encrypted.toString('hex');
}
```

---

## 71. Sample 27 · callee #10

- **Function:** `updateMany`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/infra-config/infra-config.service.ts`
- **Callee:** `stopApp()`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 244, col 7 — pattern `anchor_substring`

```typescript
stopApp()
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/infra-config/helper.ts`
- **Range:** line 382, col 16
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
 * Stop the app after 5 seconds
 * (Docker will re-start the app)
 */
export function stopApp() {
  console.log('Stopping app in 5 seconds...');

  setTimeout(() => {
    console.log('Stopping app now...');
    process.kill(process.pid, 'SIGTERM');
  }, 5000);
}
```

---

## 72. Sample 27 · callee #11

- **Function:** `updateMany`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/infra-config/infra-config.service.ts`
- **Callee:** `this.EXCLUDE_FROM_UPDATE_CONFIGS`
- **Status:** OK

### Usage site (matched in test file)

Line 215, col 11 — pattern `anchor_substring`

```typescript
this.EXCLUDE_FROM_UPDATE_CONFIGS
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/infra-config/infra-config.service.ts`
- **Range:** line 46, col 2
- **Selection:** `go_to_source_definition_primary`

```typescript
EXCLUDE_FROM_UPDATE_CONFIGS = [
```

---

## 73. Sample 27 · callee #12

- **Function:** `updateMany`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/infra-config/infra-config.service.ts`
- **Callee:** `this.prisma`
- **Status:** OK
- **Also seen in:** 2 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 223, col 35 — pattern `anchor_substring`

```typescript
this.prisma
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/infra-config/infra-config.service.ts`
- **Range:** line 40, col 21
- **Selection:** `go_to_source_definition_primary`

```typescript
private readonly prisma: PrismaService,
```

---

## 74. Sample 28 · callee #0

- **Function:** `get`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/infra-config/infra-config.service.ts`
- **Callee:** `this.prisma.infraConfig.findUniqueOrThrow(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 419, col 57 — pattern `core_fallback`

```typescript
this.prisma.infraConfig.findUniqueOrThrow(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 20871, col 270

```typescript
/**
     * Find one InfraConfig that matches the filter or throw an error with `error.code='P2025'`
     * if no matches were found.
     * @param {InfraConfigFindUniqueOrThrowArgs} args - Arguments to find a InfraConfig
     * @example
     * // Get one InfraConfig
     * const infraConfig = await prisma.infraConfig.findUniqueOrThrow({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     */
    findUniqueOrThrow<T extends InfraConfigFindUniqueOrThrowArgs>(args: SelectSubset<T, InfraConfigFindUniqueOrThrowArgs<ExtArgs>>): Prisma__InfraConfigClient<$Result.GetResult<Prisma.$InfraConfigPayload<ExtArgs>, T, "findUniqueOrThrow", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>
```

---

## 75. Sample 28 · callee #2

- **Function:** `get`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/infra-config/infra-config.service.ts`
- **Callee:** `this.cast(infraConfig)`
- **Status:** OK

### Usage site (matched in test file)

Line 423, col 22 — pattern `anchor_substring`

```typescript
this.cast(infraConfig)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/infra-config/infra-config.service.ts`
- **Range:** line 136, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Typecast a database InfraConfig to a InfraConfig model
   * @param dbInfraConfig database InfraConfig
   * @returns InfraConfig model
   */
  private cast(dbInfraConfig: DBInfraConfig) {
    switch (dbInfraConfig.name) {
      case InfraConfigEnum.USER_HISTORY_STORE_ENABLED:
        dbInfraConfig.value =
          dbInfraConfig.value === 'true'
            ? ServiceStatus.ENABLE
            : ServiceStatus.DISABLE;
        break;
      default:
        break;
    }

    const plainValue = dbInfraConfig.isEncrypted
      ? decrypt(dbInfraConfig.value)
      : dbInfraConfig.value;

    return <InfraConfig>{
      name: dbInfraConfig.name,
      value: plainValue ?? '',
    };
  }
```

---

## 76. Sample 29 · callee #0

- **Function:** `reset`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/infra-config/infra-config.service.ts`
- **Callee:** `this.prisma.infraConfig.deleteMany(...)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 504, col 37 — pattern `core_fallback`

```typescript
this.prisma.infraConfig.deleteMany(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 21017, col 248

```typescript
/**
     * Delete zero or more InfraConfigs.
     * @param {InfraConfigDeleteManyArgs} args - Arguments to filter InfraConfigs to delete.
     * @example
     * // Delete a few InfraConfigs
     * const { count } = await prisma.infraConfig.deleteMany({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     * 
     */
    deleteMany<T extends InfraConfigDeleteManyArgs>(args?: SelectSubset<T, InfraConfigDeleteManyArgs<ExtArgs>>): Prisma.PrismaPromise<BatchPayload>
```

---

## 77. Sample 29 · callee #1

- **Function:** `reset`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/infra-config/infra-config.service.ts`
- **Callee:** `this.prisma.infraConfig.createMany(...)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 512, col 37 — pattern `core_fallback`

```typescript
this.prisma.infraConfig.createMany(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 20948, col 248

```typescript
/**
     * Create many InfraConfigs.
     * @param {InfraConfigCreateManyArgs} args - Arguments to create many InfraConfigs.
     * @example
     * // Create many InfraConfigs
     * const infraConfig = await prisma.infraConfig.createMany({
     *   data: [
     *     // ... provide data here
     *   ]
     * })
     *     
     */
    createMany<T extends InfraConfigCreateManyArgs>(args?: SelectSubset<T, InfraConfigCreateManyArgs<ExtArgs>>): Prisma.PrismaPromise<BatchPayload>
```

---

## 78. Sample 29 · callee #4

- **Function:** `reset`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/infra-config/infra-config.service.ts`
- **Callee:** `getDefaultInfraConfigs()`
- **Status:** OK

### Usage site (matched in test file)

Line 499, col 44 — pattern `anchor_substring`

```typescript
getDefaultInfraConfigs()
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/infra-config/helper.ts`
- **Range:** line 93, col 22
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
 * Read the default values from .env file and return them as an array
 * @returns Array of default infra configs
 */
export async function getDefaultInfraConfigs(): Promise<DefaultInfraConfig[]> {
  const prisma = new PrismaService();

  // Prepare rows for 'infra_config' table with default values (from .env) for each 'name'
  const configuredSSOProviders = getConfiguredSSOProvidersFromEnvFile();
  const generatedAnalyticsUserId = generateAnalyticsUserId();

  const infraConfigDefaultObjs: DefaultInfraConfig[] = [
    {
      name: InfraConfigEnum.MAILER_SMTP_ENABLE,
      value: process.env.MAILER_SMTP_ENABLE ?? 'true',
      lastSyncedEnvFileValue: process.env.MAILER_SMTP_ENABLE ?? 'true',
      isEncrypted: false,
    },
    {
      name: InfraConfigEnum.MAILER_USE_CUSTOM_CONFIGS,
      value: process.env.MAILER_USE_CUSTOM_CONFIGS ?? 'false',
      lastSyncedEnvFileValue: process.env.MAILER_USE_CUSTOM_CONFIGS ?? 'false',
      isEncrypted: false,
    },
    {
      name: InfraConfigEnum.MAILER_SMTP_URL,
      value: encrypt(process.env.MAILER_SMTP_URL),
      lastSyncedEnvFileValue: encrypt(process.env.MAILER_SMTP_URL),
      isEncrypted: true,
    },
    {
      name: InfraConfigEnum.MAILER_ADDRESS_FROM,
      value: process.env.MAILER_ADDRESS_FROM,
      lastSyncedEnvFileValue: process.env.MAILER_ADDRESS_FROM,
      isEncrypted: false,
    },
    {
      name: InfraConfigEnum.MAILER_SMTP_HOST,
      value: process.env.MAILER_SMTP_HOST,
      lastSyncedEnvFileValue: process.env.MAILER_SMTP_HOST,
      isEncrypted: false,
    },
    {
      name: InfraConfigEnum.MAILER_SMTP_PORT,
      value: process.env.MAILER_SMTP_PORT,
      lastSyncedEnvFileValue: process.env.MAILER_SMTP_PORT,
      isEncrypted: false,
    },
    {
      name: InfraConfigEnum.MAILER_SMTP_SECURE,
      value: process.env.MAILER_SMTP_SECURE,
      lastSyncedEnvFileValue: process.env.MAILER_SMTP_SECURE,
      isEncrypted: false,
    },
    {
      name: InfraConfigEnum.MAILER_SMTP_USER,
      value: process.env.MAILER_SMTP_USER,
      lastSyncedEnvFileValue: process.env.MAILER_SMTP_USER,
      isEncrypted: false,
    },
    {
      name: InfraConfigEnum.MAILER_SMTP_PASSWORD,
      value: encrypt(process.env.MAILER_SMTP_PASSWORD),
      lastSyncedEnvFileValue: encrypt(process.env.MAILER_SMTP_PASSWORD),
      isEncrypted: true,
    },
    {
      name: InfraConfigEnum.MAILER_TLS_REJECT_UNAUTHORIZED,
      value: process.env.MAILER_TLS_REJECT_UNAUTHORIZED,
      lastSyncedEnvFileValue: process.env.MAILER_TLS_REJECT_UNAUTHORIZED,
      isEncrypted: false,
    },
    {
      name: InfraConfigEnum.GOOGLE_CLIENT_ID,
      value: encrypt(process.env.GOOGLE_CLIENT_ID),
      lastSyncedEnvFileValue: encrypt(process.env.GOOGLE_CLIENT_ID),
      isEncrypted: true,
    },
    {
      name: InfraConfigEnum.GOOGLE_CLIENT_SECRET,
      value: encrypt(process.env.GOOGLE_CLIENT_SECRET),
      lastSyncedEnvFileValue: encrypt(process.env.GOOGLE_CLIENT_SECRET),
      isEncrypted: true,
    },
    {
      name: InfraConfigEnum.GOOGLE_CALLBACK_URL,
      value: process.env.GOOGLE_CALLBACK_URL,
      lastSyncedEnvFileValue: process.env.GOOGLE_CALLBACK_URL,
      isEncrypted: false,
    },
    {
      name: InfraConfigEnum.GOOGLE_SCOPE,
      value: process.env.GOOGLE_SCOPE,
      lastSyncedEnvFileValue: process.env.GOOGLE_SCOPE,
      isEncrypted: false,
    },
    {
      name: InfraConfigEnum.GITHUB_CLIENT_ID,
      value: encrypt(process.env.GITHUB_CLIENT_ID),
      lastSyncedEnvFileValue: encrypt(process.env.GITHUB_CLIENT_ID),
      isEncrypted: true,
    },
    {
      name: InfraConfigEnum.GITHUB_CLIENT_SECRET,
      value: encrypt(process.env.GITHUB_CLIENT_SECRET),
      lastSyncedEnvFileValue: encrypt(process.env.GITHUB_CLIENT_SECRET),
      isEncrypted: true,
    },
    {
      name: InfraConfigEnum.GITHUB_CALLBACK_URL,
      value: process.env.GITHUB_CALLBACK_URL,
      lastSyncedEnvFileValue: process.env.GITHUB_CALLBACK_URL,
      isEncrypted: false,
    },
    {
      name: InfraConfigEnum.GITHUB_SCOPE,
      value: process.env.GITHUB_SCOPE,
      lastSyncedEnvFileValue: process.env.GITHUB_SCOPE,
      isEncrypted: false,
    },
    {
      name: InfraConfigEnum.MICROSOFT_CLIENT_ID,
      value: encrypt(process.env.MICROSOFT_CLIENT_ID),
      lastSyncedEnvFileValue: encrypt(process.env.MICROSOFT_CLIENT_ID),
      isEncrypted: true,
    },
    {
      name: InfraConfigEnum.MICROSOFT_CLIENT_SECRET,
      value: encrypt(process.env.MICROSOFT_CLIENT_SECRET),
      lastSyncedEnvFileValue: encrypt(process.env.MICROSOFT_CLIENT_SECRET),
      isEncrypted: true,
    },
    {
      name: InfraConfigEnum.MICROSOFT_CALLBACK_URL,
      value: process.env.MICROSOFT_CALLBACK_URL,
      lastSyncedEnvFileValue: process.env.MICROSOFT_CALLBACK_URL,
      isEncrypted: false,
    },
    {
      name: InfraConfigEnum.MICROSOFT_SCOPE,
      value: process.env.MICROSOFT_SCOPE,
      lastSyncedEnvFileValue: process.env.MICROSOFT_SCOPE,
      isEncrypted: false,
    },
    {
      name: InfraConfigEnum.MICROSOFT_TENANT,
      value: process.env.MICROSOFT_TENANT,
      lastSyncedEnvFileValue: process.env.MICROSOFT_TENANT,
      isEncrypted: false,
    },
    {
      name: InfraConfigEnum.VITE_ALLOWED_AUTH_PROVIDERS,
      value: configuredSSOProviders,
      lastSyncedEnvFileValue: configuredSSOProviders,
      isEncrypted: false,
    },
    {
      name: InfraConfigEnum.ALLOW_ANALYTICS_COLLECTION,
      value: false.toString(),
      lastSyncedEnvFileValue: null,
      isEncrypted: false,
    },
    {
      name: InfraConfigEnum.ANALYTICS_USER_ID,
      value: generatedAnalyticsUserId,
      lastSyncedEnvFileValue: null,
      isEncrypted: false,
    },
    {
      name: InfraConfigEnum.IS_FIRST_TIME_INFRA_SETUP,
      value: (await prisma.infraConfig.count()) === 0 ? 'true' : 'false',
      lastSyncedEnvFileValue: null,
      isEncrypted: false,
    },
    {
      name: InfraConfigEnum.USER_HISTORY_STORE_ENABLED,
      value: 'true',
      lastSyncedEnvFileValue: null,
      isEncrypted: false,
    },
  ];

  return infraConfigDefaultObjs;
}
```

---

## 79. Sample 29 · callee #6

- **Function:** `reset`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/infra-config/infra-config.service.ts`
- **Callee:** `InfraConfigEnum.IS_FIRST_TIME_INFRA_SETUP`
- **Status:** OK

### Usage site (matched in test file)

Line 494, col 7 — pattern `anchor_substring`

```typescript
InfraConfigEnum.IS_FIRST_TIME_INFRA_SETUP
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/types/InfraConfig.ts`
- **Range:** line 33, col 2
- **Selection:** `go_to_source_definition_primary`

```typescript
IS_FIRST_TIME_INFRA_SETUP = 'IS_FIRST_TIME_INFRA_SETUP',
```

---

## 80. Sample 29 · callee #7

- **Function:** `reset`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/infra-config/infra-config.service.ts`
- **Callee:** `InfraConfigEnum.ANALYTICS_USER_ID`
- **Status:** OK

### Usage site (matched in test file)

Line 495, col 7 — pattern `anchor_substring`

```typescript
InfraConfigEnum.ANALYTICS_USER_ID
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/types/InfraConfig.ts`
- **Range:** line 32, col 2
- **Selection:** `go_to_source_definition_primary`

```typescript
ANALYTICS_USER_ID = 'ANALYTICS_USER_ID',
```

---

## 81. Sample 29 · callee #8

- **Function:** `reset`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/infra-config/infra-config.service.ts`
- **Callee:** `InfraConfigEnum.ALLOW_ANALYTICS_COLLECTION`
- **Status:** OK

### Usage site (matched in test file)

Line 496, col 7 — pattern `anchor_substring`

```typescript
InfraConfigEnum.ALLOW_ANALYTICS_COLLECTION
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/types/InfraConfig.ts`
- **Range:** line 31, col 2
- **Selection:** `go_to_source_definition_primary`

```typescript
ALLOW_ANALYTICS_COLLECTION = 'ALLOW_ANALYTICS_COLLECTION',
```

---

## 82. Sample 30 · callee #1

- **Function:** `create`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/infra-token/infra-token.service.ts`
- **Callee:** `this.validateExpirationDate(expiryInDays ?? null)`
- **Status:** OK

### Usage site (matched in test file)

Line 82, col 10 — pattern `anchor_substring`

```typescript
this.validateExpirationDate(expiryInDays ?? null)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/infra-token/infra-token.service.ts`
- **Range:** line 32, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Validate the expiration date of the token
   *
   * @param expiresOn Number of days the token is valid for
   * @returns Boolean indicating if the expiration date is valid
   */
  private validateExpirationDate(expiresOn: null | number) {
    if (expiresOn === null || this.VALID_TOKEN_DURATIONS.includes(expiresOn))
      return true;
    return false;
  }
```

---

## 83. Sample 30 · callee #3

- **Function:** `create`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/infra-token/infra-token.service.ts`
- **Callee:** `this.prisma.infraToken.create(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 77, col 9 — pattern `core_fallback`

```typescript
this.prisma.infraToken.create(...)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/infra-token/infra-token.service.ts`
- **Range:** line 76, col 8
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Create a new infra token
   * @param label label of the token
   * @param expiryInDays expiry duration of the token
   * @param admin admin who created the token
   * @returns Either of error message or CreateInfraTokenResponse
   */
  async create(label: string, expiryInDays: number, admin: Admin) {
    if (!isValidLength(label, this.TITLE_LENGTH)) {
      return E.left(INFRA_TOKEN_LABEL_SHORT);
    }

    if (!this.validateExpirationDate(expiryInDays ?? null)) {
      return E.left(INFRA_TOKEN_EXPIRY_INVALID);
    }

    const createdInfraToken = await this.prisma.infraToken.create({
      data: {
        creatorUid: admin.uid,
        label,
        expiresOn: calculateExpirationDate(expiryInDays ?? null) ?? undefined,
      },
    });

    const res: CreateInfraTokenResponse = {
      token: createdInfraToken.token,
      info: this.cast(createdInfraToken),
    };

    return E.right(res);
  }
```

---

## 84. Sample 30 · callee #4

- **Function:** `create`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/infra-token/infra-token.service.ts`
- **Callee:** `this.cast(createdInfraToken)`
- **Status:** OK

### Usage site (matched in test file)

Line 96, col 13 — pattern `anchor_substring`

```typescript
this.cast(createdInfraToken)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/infra-token/infra-token.service.ts`
- **Range:** line 43, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Typecast a database InfraToken to a InfraToken model
   * @param dbInfraToken database InfraToken
   * @returns InfraToken model
   */
  private cast(dbInfraToken: dbInfraToken): InfraToken {
    return {
      id: dbInfraToken.id,
      label: dbInfraToken.label,
      createdOn: dbInfraToken.createdOn,
      expiresOn: dbInfraToken.expiresOn,
      lastUsedOn: dbInfraToken.updatedOn,
    };
  }
```

---

## 85. Sample 30 · callee #8

- **Function:** `create`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/infra-token/infra-token.service.ts`
- **Callee:** `this.TITLE_LENGTH`
- **Status:** OK

### Usage site (matched in test file)

Line 78, col 31 — pattern `anchor_substring`

```typescript
this.TITLE_LENGTH
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/infra-token/infra-token.service.ts`
- **Range:** line 23, col 2
- **Selection:** `go_to_source_definition_primary`

```typescript
TITLE_LENGTH = 3;
```

---

## 86. Sample 30 · callee #9

- **Function:** `create`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/infra-token/infra-token.service.ts`
- **Callee:** `this.prisma`
- **Status:** OK

### Usage site (matched in test file)

Line 86, col 37 — pattern `anchor_substring`

```typescript
this.prisma
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/infra-token/infra-token.service.ts`
- **Range:** line 19, col 21
- **Selection:** `go_to_source_definition_primary`

```typescript
private readonly prisma: PrismaService,
```

---

## 87. Sample 30 · callee #10

- **Function:** `create`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/infra-token/infra-token.service.ts`
- **Callee:** `infraToken.create`
- **Status:** OK

### Usage site (matched in test file)

Line 86, col 49 — pattern `anchor_substring`

```typescript
infraToken.create
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 23039, col 214

```typescript
/**
     * Create a InfraToken.
     * @param {InfraTokenCreateArgs} args - Arguments to create a InfraToken.
     * @example
     * // Create one InfraToken
     * const InfraToken = await prisma.infraToken.create({
     *   data: {
     *     // ... data to create a InfraToken
     *   }
     * })
     * 
     */
    create<T extends InfraTokenCreateArgs>(args: SelectSubset<T, InfraTokenCreateArgs<ExtArgs>>): Prisma__InfraTokenClient<$Result.GetResult<Prisma.$InfraTokenPayload<ExtArgs>, T, "create", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>
```

---

## 88. Sample 31 · callee #0

- **Function:** `generateShortCodeID`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/shortcode/shortcode.service.ts`
- **Callee:** `Math.floor(Math.random() * SHORT_CODE_CHARS.length)`
- **Status:** OK

### Usage site (matched in test file)

Line 74, col 26 — pattern `anchor_substring`

```typescript
Math.floor(Math.random() * SHORT_CODE_CHARS.length)
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es5.d.ts`
- **Range:** line 715, col 27

```typescript
/**
     * Returns the greatest integer less than or equal to its numeric argument.
     * @param x A numeric expression.
     */
    floor(x: number): number;
```

---

## 89. Sample 31 · callee #1

- **Function:** `generateShortCodeID`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/shortcode/shortcode.service.ts`
- **Callee:** `Math.random()`
- **Status:** OK

### Usage site (matched in test file)

Line 74, col 37 — pattern `anchor_substring`

```typescript
Math.random()
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es5.d.ts`
- **Range:** line 741, col 38

```typescript
/** Returns a pseudorandom number between 0 and 1. */
    random(): number;
```

---

## 90. Sample 31 · callee #2

- **Function:** `generateShortCodeID`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/shortcode/shortcode.service.ts`
- **Callee:** `SHORT_CODE_CHARS.length`
- **Status:** OK

### Usage site (matched in test file)

Line 74, col 53 — pattern `anchor_substring`

```typescript
SHORT_CODE_CHARS.length
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es5.d.ts`
- **Range:** line 511, col 19

```typescript
/** Removes the leading and trailing white space and line terminator characters from a string. */
/** Returns the length of a String object. */
    readonly length: number;
```

---

## 91. Sample 32 · callee #0

- **Function:** `generateUniqueShortCodeID`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/shortcode/shortcode.service.ts`
- **Callee:** `this.generateShortCodeID()`
- **Status:** OK

### Usage site (matched in test file)

Line 86, col 20 — pattern `anchor_substring`

```typescript
this.generateShortCodeID()
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/shortcode/shortcode.service.ts`
- **Range:** line 69, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Generate a shortcode
   *
   * @returns generated shortcode
   */
  private generateShortCodeID(): string {
    let result = '';
    for (let i = 0; i < SHORT_CODE_LENGTH; i++) {
      result +=
        SHORT_CODE_CHARS[Math.floor(Math.random() * SHORT_CODE_CHARS.length)];
    }
    return result;
  }
```

---

## 92. Sample 32 · callee #1

- **Function:** `generateUniqueShortCodeID`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/shortcode/shortcode.service.ts`
- **Callee:** `this.getShortCode(code)`
- **Status:** OK

### Usage site (matched in test file)

Line 88, col 26 — pattern `anchor_substring`

```typescript
this.getShortCode(code)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/shortcode/shortcode.service.ts`
- **Range:** line 99, col 8
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Fetch details regarding a ShortCode
   *
   * @param shortcode ShortCode
   * @returns Either of ShortCode details or error
   */
  async getShortCode(shortcode: string) {
    try {
      const shortcodeInfo = await this.prisma.shortcode.findFirstOrThrow({
        where: { id: shortcode },
      });
      return E.right(this.cast(shortcodeInfo));
    } catch (error) {
      return E.left(SHORTCODE_NOT_FOUND);
    }
  }
```

---

## 93. Sample 33 · callee #0

- **Function:** `getShortCode`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/shortcode/shortcode.service.ts`
- **Callee:** `this.prisma.shortcode.findFirstOrThrow(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 102, col 57 — pattern `core_fallback`

```typescript
this.prisma.shortcode.findFirstOrThrow(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 8653, col 259

```typescript
/**
     * Find the first Shortcode that matches the filter or
     * throw `PrismaKnownClientError` with `P2025` code if no matches were found.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {ShortcodeFindFirstOrThrowArgs} args - Arguments to find a Shortcode
     * @example
     * // Get one Shortcode
     * const shortcode = await prisma.shortcode.findFirstOrThrow({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     */
    findFirstOrThrow<T extends ShortcodeFindFirstOrThrowArgs>(args?: SelectSubset<T, ShortcodeFindFirstOrThrowArgs<ExtArgs>>): Prisma__ShortcodeClient<$Result.GetResult<Prisma.$ShortcodePayload<ExtArgs>, T, "findFirstOrThrow", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>
```

---

## 94. Sample 33 · callee #2

- **Function:** `getShortCode`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/shortcode/shortcode.service.ts`
- **Callee:** `this.cast(shortcodeInfo)`
- **Status:** OK

### Usage site (matched in test file)

Line 105, col 22 — pattern `anchor_substring`

```typescript
this.cast(shortcodeInfo)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/shortcode/shortcode.service.ts`
- **Range:** line 52, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Converts a Prisma Shortcode type into the Shortcode model
   *
   * @param shortcodeInfo Prisma Shortcode type
   * @returns GQL Shortcode
   */
  private cast(shortcodeInfo: DBShortCode): Shortcode {
    return <Shortcode>{
      id: shortcodeInfo.id,
      request: JSON.stringify(shortcodeInfo.request),
      properties:
        shortcodeInfo.embedProperties != null
          ? JSON.stringify(shortcodeInfo.embedProperties)
          : null,
      createdOn: shortcodeInfo.createdOn,
    };
  }
```

---

## 95. Sample 33 · callee #4

- **Function:** `getShortCode`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/shortcode/shortcode.service.ts`
- **Callee:** `this.prisma`
- **Status:** OK

### Usage site (matched in test file)

Line 102, col 35 — pattern `anchor_substring`

```typescript
this.prisma
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/shortcode/shortcode.service.ts`
- **Range:** line 27, col 21
- **Selection:** `go_to_source_definition_primary`

```typescript
private readonly prisma: PrismaService,
```

---

## 96. Sample 34 · callee #0

- **Function:** `fetchAllTeams`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team/team.service.ts`
- **Callee:** `this.prisma.team.findMany(options)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 536, col 32 — pattern `anchor_substring`

```typescript
this.prisma.team.findMany(options)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 3044, col 261

```typescript
/**
     * Find zero or more Teams that matches the filter.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {TeamFindManyArgs} args - Arguments to filter and select certain fields only.
     * @example
     * // Get all Teams
     * const teams = await prisma.team.findMany()
     * 
     * // Get first 10 Teams
     * const teams = await prisma.team.findMany({ take: 10 })
     * 
     * // Only select the `id`
     * const teamWithIdOnly = await prisma.team.findMany({ select: { id: true } })
     * 
     */
    findMany<T extends TeamFindManyArgs>(args?: SelectSubset<T, TeamFindManyArgs<ExtArgs>>): Prisma.PrismaPromise<$Result.GetResult<Prisma.$TeamPayload<ExtArgs>, T, "findMany", GlobalOmitOptions>>
```

---

## 97. Sample 34 · callee #1

- **Function:** `fetchAllTeams`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team/team.service.ts`
- **Callee:** `this.prisma`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 536, col 32 — pattern `anchor_substring`

```typescript
this.prisma
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/team/team.service.ts`
- **Range:** line 29, col 21
- **Selection:** `go_to_source_definition_primary`

```typescript
private readonly prisma: PrismaService,
```

---

## 98. Sample 35 · callee #0

- **Function:** `getTeamsCount`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team/team.service.ts`
- **Callee:** `this.prisma.team.count()`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 546, col 30 — pattern `anchor_substring`

```typescript
this.prisma.team.count()
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 3227, col 220

```typescript
/**
     * Count the number of Teams.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {TeamCountArgs} args - Arguments to filter Teams to count.
     * @example
     * // Count the number of Teams
     * const count = await prisma.team.count({
     *   where: {
     *     // ... the filter for the Teams we want to count
     *   }
     * })
    **/
    count<T extends TeamCountArgs>(
      args?: Subset<T, TeamCountArgs>,
    ): Prisma.PrismaPromise<
      T extends $Utils.Record<'select', any>
        ? T['select'] extends true
          ? number
          : GetScalarType<T['select'], TeamCountAggregateOutputType>
        : number
    >
```

---

## 99. Sample 36 · callee #0

- **Function:** `exportCollectionsToJSON`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-collection/team-collection.service.ts`
- **Callee:** `this.prisma.teamCollection.findMany(...)`
- **Status:** OK
- **Also seen in:** 5 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 160, col 62 — pattern `core_fallback`

```typescript
this.prisma.teamCollection.findMany(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 6399, col 301

```typescript
/**
     * Find zero or more TeamCollections that matches the filter.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {TeamCollectionFindManyArgs} args - Arguments to filter and select certain fields only.
     * @example
     * // Get all TeamCollections
     * const teamCollections = await prisma.teamCollection.findMany()
     * 
     * // Get first 10 TeamCollections
     * const teamCollections = await prisma.teamCollection.findMany({ take: 10 })
     * 
     * // Only select the `id`
     * const teamCollectionWithIdOnly = await prisma.teamCollection.findMany({ select: { id: true } })
     * 
     */
    findMany<T extends TeamCollectionFindManyArgs>(args?: SelectSubset<T, TeamCollectionFindManyArgs<ExtArgs>>): Prisma.PrismaPromise<$Result.GetResult<Prisma.$TeamCollectionPayload<ExtArgs>, T, "findMany", GlobalOmitOptions>>
```

---

## 100. Sample 36 · callee #1

- **Function:** `exportCollectionsToJSON`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-collection/team-collection.service.ts`
- **Callee:** `this.exportCollectionToJSONObject(teamID, coll.id)`
- **Status:** OK

### Usage site (matched in test file)

Line 169, col 28 — pattern `anchor_substring`

```typescript
this.exportCollectionToJSONObject(teamID, coll.id)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/team-collection/team-collection.service.ts`
- **Range:** line 105, col 8
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Generate a JSON containing all the contents of a collection
   *
   * @param teamID The Team ID
   * @param collectionID The Collection ID
   * @returns A JSON string containing all the contents of a collection
   */
  async exportCollectionToJSONObject(
    teamID: string,
    collectionID: string,
  ): Promise<E.Right<CollectionFolder> | E.Left<string>> {
    const collection = await this.getCollection(collectionID);
    if (E.isLeft(collection)) return E.left(TEAM_INVALID_COLL_ID);

    const childrenCollection = await this.prisma.teamCollection.findMany({
      where: {
        teamID,
        parentID: collectionID,
      },
      orderBy: {
        orderIndex: 'asc',
      },
    });

    const childrenCollectionObjects = [];
    for (const coll of childrenCollection) {
      const result = await this.exportCollectionToJSONObject(teamID, coll.id);
      if (E.isLeft(result)) return E.left(result.left);

      childrenCollectionObjects.push(result.right);
    }

    const requests = await this.prisma.teamRequest.findMany({
      where: {
        teamID,
        collectionID,
      },
      orderBy: {
        orderIndex: 'asc',
      },
    });

    const data = transformCollectionData(collection.right.data);

    const result: CollectionFolder = {
      name: collection.right.title,
      folders: childrenCollectionObjects,
      requests: requests.map((x) => x.request),
      data,
    };

    return E.right(result);
  }
```

---

## 101. Sample 36 · callee #5

- **Function:** `exportCollectionsToJSON`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-collection/team-collection.service.ts`
- **Callee:** `JSON.stringify(rootCollectionObjects)`
- **Status:** OK
- **Also seen in:** 7 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 175, col 20 — pattern `anchor_substring`

```typescript
JSON.stringify(rootCollectionObjects)
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

## 102. Sample 36 · callee #6

- **Function:** `exportCollectionsToJSON`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-collection/team-collection.service.ts`
- **Callee:** `this.prisma`
- **Status:** OK
- **Also seen in:** 4 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 160, col 35 — pattern `anchor_substring`

```typescript
this.prisma
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/team-collection/team-collection.service.ts`
- **Range:** line 49, col 21
- **Selection:** `go_to_source_definition_primary`

```typescript
private readonly prisma: PrismaService,
```

---

## 103. Sample 38 · callee #0

- **Function:** `removeTeamCollection`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-collection/team-collection.service.ts`
- **Callee:** `this.prisma.teamCollection.delete(...)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 642, col 70 — pattern `core_fallback`

```typescript
this.prisma.teamCollection.delete(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 6469, col 270

```typescript
/**
     * Delete a TeamCollection.
     * @param {TeamCollectionDeleteArgs} args - Arguments to delete one TeamCollection.
     * @example
     * // Delete one TeamCollection
     * const TeamCollection = await prisma.teamCollection.delete({
     *   where: {
     *     // ... filter to delete one TeamCollection
     *   }
     * })
     * 
     */
    delete<T extends TeamCollectionDeleteArgs>(args: SelectSubset<T, TeamCollectionDeleteArgs<ExtArgs>>): Prisma__TeamCollectionClient<$Result.GetResult<Prisma.$TeamCollectionPayload<ExtArgs>, T, "delete", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>
```

---

## 104. Sample 39 · callee #1

- **Function:** `deleteCollectionData`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-collection/team-collection.service.ts`
- **Callee:** `Promise.all(...)`
- **Status:** OK
- **Also seen in:** 2 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 669, col 19 — pattern `core_fallback`

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

## 105. Sample 39 · callee #2

- **Function:** `deleteCollectionData`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-collection/team-collection.service.ts`
- **Callee:** `this.deleteCollection(coll.id)`
- **Status:** OK

### Usage site (matched in test file)

Line 670, col 41 — pattern `anchor_substring`

```typescript
this.deleteCollection(coll.id)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/team-collection/team-collection.service.ts`
- **Range:** line 700, col 8
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Delete a TeamCollection
   *
   * @param collectionID The Collection Id
   * @returns An Either of Boolean of deletion status
   */
  async deleteCollection(collectionID: string) {
    const collection = await this.getCollection(collectionID);
    if (E.isLeft(collection)) return E.left(collection.left);

    // Delete all child collections and requests in the collection
    const collectionData = await this.deleteCollectionData(collection.right);
    if (E.isLeft(collectionData)) return E.left(collectionData.left);

    // Update orderIndexes in TeamCollection table for user
    await this.updateOrderIndex(
      collectionData.right.parentID,
      { gt: collectionData.right.orderIndex },
      { decrement: 1 },
    );

    return E.right(true);
  }
```

---

## 106. Sample 39 · callee #3

- **Function:** `deleteCollectionData`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-collection/team-collection.service.ts`
- **Callee:** `this.prisma.teamRequest.deleteMany(...)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 674, col 35 — pattern `core_fallback`

```typescript
this.prisma.teamRequest.deleteMany(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 7704, col 248

```typescript
/**
     * Delete zero or more TeamRequests.
     * @param {TeamRequestDeleteManyArgs} args - Arguments to filter TeamRequests to delete.
     * @example
     * // Delete a few TeamRequests
     * const { count } = await prisma.teamRequest.deleteMany({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     * 
     */
    deleteMany<T extends TeamRequestDeleteManyArgs>(args?: SelectSubset<T, TeamRequestDeleteManyArgs<ExtArgs>>): Prisma.PrismaPromise<BatchPayload>
```

---

## 107. Sample 39 · callee #4

- **Function:** `deleteCollectionData`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-collection/team-collection.service.ts`
- **Callee:** `this.removeTeamCollection(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 681, col 46 — pattern `core_fallback`

```typescript
this.removeTeamCollection(...)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/team-collection/team-collection.service.ts`
- **Range:** line 631, col 3

```typescript
/**
   * Delete a TeamCollection from the DB
   *
   * @param collectionID The Collection Id
   * @returns The deleted TeamCollection
   */
  private async removeTeamCollection(collectionID: string) {
    try {
      const deletedTeamCollection = await this.prisma.teamCollection.delete({
        where: {
          id: collectionID,
        },
      });

      return E.right(deletedTeamCollection);
    } catch (error) {
      return E.left(TEAM_COLL_NOT_FOUND);
    }
  }
```

---

## 108. Sample 39 · callee #7

- **Function:** `deleteCollectionData`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-collection/team-collection.service.ts`
- **Callee:** `this.pubsub.publish(...)`
- **Status:** OK
- **Also seen in:** 10 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 687, col 17 — pattern `core_fallback`

```typescript
this.pubsub.publish(...)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/pubsub/pubsub.service.ts`
- **Range:** line 24, col 8
- **Selection:** `go_to_source_definition_primary`

```typescript
  async publish<T extends keyof TopicDef>(topic: T, payload: TopicDef[T]) {
    await this.pubsub.publish(topic, payload);
  }
```

---

## 109. Sample 39 · callee #12

- **Function:** `deleteCollectionData`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-collection/team-collection.service.ts`
- **Callee:** `this.pubsub`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 687, col 5 — pattern `anchor_substring`

```typescript
this.pubsub
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/team-collection/team-collection.service.ts`
- **Range:** line 50, col 21
- **Selection:** `go_to_source_definition_primary`

```typescript
private readonly pubsub: PubSubService,
```

---

## 110. Sample 40 · callee #0

- **Function:** `deleteCollection`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-collection/team-collection.service.ts`
- **Callee:** `this.getCollection(collectionID)`
- **Status:** OK
- **Also seen in:** 3 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 702, col 30 — pattern `anchor_substring`

```typescript
this.getCollection(collectionID)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/team-collection/team-collection.service.ts`
- **Range:** line 441, col 8
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Get collection details
   *
   * @param collectionID The collection ID
   * @returns An Either of the Collection details
   */
  async getCollection(collectionID: string) {
    try {
      const teamCollection = await this.prisma.teamCollection.findUniqueOrThrow(
        {
          where: {
            id: collectionID,
          },
        },
      );
      return E.right(teamCollection);
    } catch (error) {
      return E.left(TEAM_COLL_NOT_FOUND);
    }
  }
```

---

## 111. Sample 40 · callee #3

- **Function:** `deleteCollection`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-collection/team-collection.service.ts`
- **Callee:** `this.deleteCollectionData(collection.right)`
- **Status:** OK

### Usage site (matched in test file)

Line 706, col 34 — pattern `anchor_substring`

```typescript
this.deleteCollectionData(collection.right)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/team-collection/team-collection.service.ts`
- **Range:** line 651, col 3

```typescript
/**
   * Delete child collection and requests of a TeamCollection
   *
   * @param collectionID The Collection Id
   * @returns A Boolean of deletion status
   */
  private async deleteCollectionData(collection: DBTeamCollection) {
    // Get all child collections in collectionID
    const childCollectionList = await this.prisma.teamCollection.findMany({
      where: {
        parentID: collection.id,
      },
    });

    // Delete child collections
    await Promise.all(
      childCollectionList.map((coll) => this.deleteCollection(coll.id)),
    );

    // Delete all requests in collectionID
    await this.prisma.teamRequest.deleteMany({
      where: {
        collectionID: collection.id,
      },
    });

    // Delete collection from TeamCollection table
    const deletedTeamCollection = await this.removeTeamCollection(
      collection.id,
    );
    if (E.isLeft(deletedTeamCollection))
      return E.left(deletedTeamCollection.left);

    this.pubsub.publish(
      `team_coll/${deletedTeamCollection.right.teamID}/coll_removed`,
      deletedTeamCollection.right.id,
    );

    return E.right(deletedTeamCollection.right);
  }
```

---

## 112. Sample 40 · callee #6

- **Function:** `deleteCollection`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-collection/team-collection.service.ts`
- **Callee:** `this.updateOrderIndex(...)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 710, col 16 — pattern `core_fallback`

```typescript
this.updateOrderIndex(...)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/team-collection/team-collection.service.ts`
- **Range:** line 607, col 3

```typescript
/**
   * Update the OrderIndex of all collections in given parentID
   *
   * @param parentID The Parent collectionID
   * @param orderIndexCondition Condition to decide what collections will be updated
   * @param dataCondition Increment/Decrement OrderIndex condition
   * @returns A Collection with updated OrderIndexes
   */
  private async updateOrderIndex(
    parentID: string,
    orderIndexCondition: Prisma.IntFilter,
    dataCondition: Prisma.IntFieldUpdateOperationsInput,
  ) {
    const updatedTeamCollection = await this.prisma.teamCollection.updateMany({
      where: {
        parentID: parentID,
        orderIndex: orderIndexCondition,
      },
      data: { orderIndex: dataCondition },
    });

    return updatedTeamCollection;
  }
```

---

## 113. Sample 41 · callee #5

- **Function:** `moveCollection`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-collection/team-collection.service.ts`
- **Callee:** `this.changeParent(collection.right, null)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 830, col 39 — pattern `anchor_substring`

```typescript
this.changeParent(collection.right, null)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/team-collection/team-collection.service.ts`
- **Range:** line 716, col 3

```typescript
/**
   * Change parentID of TeamCollection's
   *
   * @param collectionID The collection ID
   * @param parentCollectionID The new parent's collection ID or change to root collection
   * @returns  If successful return an Either of true
   */
  private async changeParent(
    collection: DBTeamCollection,
    parentCollectionID: string | null,
  ) {
    try {
      let collectionCount: number;

      if (!parentCollectionID)
        collectionCount = await this.getRootCollectionsCount(collection.teamID);
      collectionCount = await this.getChildCollectionsCount(parentCollectionID);

      const updatedCollection = await this.prisma.teamCollection.update({
        where: {
          id: collection.id,
        },
        data: {
          // if parentCollectionID == null, collection becomes root collection
          // if parentCollectionID != null, collection becomes child collection
          parentID: parentCollectionID,
          orderIndex: collectionCount + 1,
        },
      });

      return E.right(this.cast(updatedCollection));
    } catch (error) {
      return E.left(TEAM_COLL_NOT_FOUND);
    }
  }
```

---

## 114. Sample 41 · callee #15

- **Function:** `moveCollection`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-collection/team-collection.service.ts`
- **Callee:** `this.isParent(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 857, col 38 — pattern `core_fallback`

```typescript
this.isParent(...)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/team-collection/team-collection.service.ts`
- **Range:** line 752, col 3

```typescript
/**
   * Check if collection is parent of destCollection
   *
   * @param collection The ID of collection being moved
   * @param destCollection The ID of collection into which we are moving target collection into
   * @returns An Option of boolean, is parent or not
   */
  private async isParent(
    collection: DBTeamCollection,
    destCollection: DBTeamCollection,
  ): Promise<O.Option<boolean>> {
    //* Recursively check if collection is a parent by going up the tree of child-parent collections until we reach a root collection i.e parentID === null
    //* Valid condition, isParent returns false
    //* Consider us moving Collection_E into Collection_D
    //* Collection_A              [parent:null !== Collection_E] return false, exit
    //*   |--> Collection_B       [parent:Collection_A !== Collection_E] call isParent(Collection_E,Collection_A)
    //*      |--> Collection_C    [parent:Collection_B !== Collection_E] call isParent(Collection_E,Collection_B)
    //*         |--> Collection_D [parent:Collection_C !== Collection_E] call isParent(Collection_E,Collection_C)
    //* Invalid condition, isParent returns true
    //* Consider us moving Collection_B into Collection_D
    //* Collection_A
    //*   |--> Collection_B
    //*      |--> Collection_C    [parent:Collection_B === Collection_B] return true, exit
    //*         |--> Collection_D [parent:Collection_C !== Collection_B] call isParent(Collection_B,Collection_C)

    // Check if collection and destCollection are same
    if (collection === destCollection) {
      return O.none;
    }
    if (destCollection.parentID !== null) {
      // Check if ID of collection is same as parent of destCollection
      if (destCollection.parentID === collection.id) {
        return O.none;
      }
      // Get collection details of collection one step above in the tree i.e the parent collection
      const parentCollection = await this.getCollection(
        destCollection.parentID,
      );
      if (E.isLeft(parentCollection)) {
        return O.none;
      }
      // Call isParent again now with parent collection
      return await this.isParent(collection, parentCollection.right);
    } else {
      return O.some(true);
    }
  }
```

---

## 115. Sample 43 · callee #0

- **Function:** `getAllRequestsInCollection`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-collection/team-collection.service.ts`
- **Callee:** `this.prisma.teamRequest.findMany(...)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 1372, col 58 — pattern `core_fallback`

```typescript
this.prisma.teamRequest.findMany(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 7603, col 289

```typescript
/**
     * Find zero or more TeamRequests that matches the filter.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {TeamRequestFindManyArgs} args - Arguments to filter and select certain fields only.
     * @example
     * // Get all TeamRequests
     * const teamRequests = await prisma.teamRequest.findMany()
     * 
     * // Get first 10 TeamRequests
     * const teamRequests = await prisma.teamRequest.findMany({ take: 10 })
     * 
     * // Only select the `id`
     * const teamRequestWithIdOnly = await prisma.teamRequest.findMany({ select: { id: true } })
     * 
     */
    findMany<T extends TeamRequestFindManyArgs>(args?: SelectSubset<T, TeamRequestFindManyArgs<ExtArgs>>): Prisma.PrismaPromise<$Result.GetResult<Prisma.$TeamRequestPayload<ExtArgs>, T, "findMany", GlobalOmitOptions>>
```

---

## 116. Sample 44 · callee #1

- **Function:** `updateTeamEnvironment`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-environments/team-environments.service.ts`
- **Callee:** `this.prisma.teamEnvironment.update(...)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 133, col 56 — pattern `core_fallback`

```typescript
this.prisma.teamEnvironment.update(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 9815, col 264

```typescript
/**
     * Update one TeamEnvironment.
     * @param {TeamEnvironmentUpdateArgs} args - Arguments to update one TeamEnvironment.
     * @example
     * // Update one TeamEnvironment
     * const teamEnvironment = await prisma.teamEnvironment.update({
     *   where: {
     *     // ... provide filter here
     *   },
     *   data: {
     *     // ... provide data here
     *   }
     * })
     * 
     */
    update<T extends TeamEnvironmentUpdateArgs>(args: SelectSubset<T, TeamEnvironmentUpdateArgs<ExtArgs>>): Prisma__TeamEnvironmentClient<$Result.GetResult<Prisma.$TeamEnvironmentPayload<ExtArgs>, T, "update", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>
```

---

## 117. Sample 44 · callee #2

- **Function:** `updateTeamEnvironment`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-environments/team-environments.service.ts`
- **Callee:** `JSON.parse(variables)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 137, col 22 — pattern `anchor_substring`

```typescript
JSON.parse(variables)
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

## 118. Sample 44 · callee #3

- **Function:** `updateTeamEnvironment`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-environments/team-environments.service.ts`
- **Callee:** `this.cast(result)`
- **Status:** OK

### Usage site (matched in test file)

Line 141, col 38 — pattern `anchor_substring`

```typescript
this.cast(result)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/team-environments/team-environments.service.ts`
- **Range:** line 34, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * TeamEnvironments are saved in the DB in the following way
   * [{ key: value }, { key: value },....]
   *
   */

  /**
   * Typecast a database TeamEnvironment to a TeamEnvironment model
   * @param teamEnvironment database TeamEnvironment
   * @returns TeamEnvironment model
   */
  private cast(teamEnvironment: DBTeamEnvironment): TeamEnvironment {
    const { id, name, teamID } = teamEnvironment;
    return {
      id,
      name,
      teamID,
      variables: JSON.stringify(teamEnvironment.variables),
    };
  }
```

---

## 119. Sample 44 · callee #8

- **Function:** `updateTeamEnvironment`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-environments/team-environments.service.ts`
- **Callee:** `this.TITLE_LENGTH`
- **Status:** OK

### Usage site (matched in test file)

Line 130, col 48 — pattern `anchor_substring`

```typescript
this.TITLE_LENGTH
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/team-environments/team-environments.service.ts`
- **Range:** line 21, col 2
- **Selection:** `go_to_source_definition_primary`

```typescript
TITLE_LENGTH = 3;
```

---

## 120. Sample 44 · callee #9

- **Function:** `updateTeamEnvironment`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-environments/team-environments.service.ts`
- **Callee:** `this.prisma`
- **Status:** OK

### Usage site (matched in test file)

Line 133, col 28 — pattern `anchor_substring`

```typescript
this.prisma
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/team-environments/team-environments.service.ts`
- **Range:** line 16, col 21
- **Selection:** `go_to_source_definition_primary`

```typescript
private readonly prisma: PrismaService,
```

---

## 121. Sample 44 · callee #11

- **Function:** `updateTeamEnvironment`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-environments/team-environments.service.ts`
- **Callee:** `this.pubsub`
- **Status:** OK

### Usage site (matched in test file)

Line 143, col 7 — pattern `anchor_substring`

```typescript
this.pubsub
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/team-environments/team-environments.service.ts`
- **Range:** line 17, col 21
- **Selection:** `go_to_source_definition_primary`

```typescript
private readonly pubsub: PubSubService,
```

---

## 122. Sample 46 · callee #0

- **Function:** `acceptInvitation`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-invitation/team-invitation.service.ts`
- **Callee:** `this.getInvitation(inviteID)`
- **Status:** OK

### Usage site (matched in test file)

Line 201, col 30 — pattern `anchor_substring`

```typescript
this.getInvitation(inviteID)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/team-invitation/team-invitation.service.ts`
- **Range:** line 52, col 8
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Get the team invite
   * @param inviteID invite id
   * @returns an Option of team invitation or none
   */
  async getInvitation(inviteID: string) {
    try {
      const dbInvitation = await this.prisma.teamInvitation.findUniqueOrThrow({
        where: {
          id: inviteID,
        },
      });

      return O.some(this.cast(dbInvitation));
    } catch (e) {
      return O.none;
    }
  }
```

---

## 123. Sample 46 · callee #3

- **Function:** `acceptInvitation`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-invitation/team-invitation.service.ts`
- **Callee:** `this.teamService.getTeamMember(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 205, col 54 — pattern `core_fallback`

```typescript
this.teamService.getTeamMember(...)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/team/team.service.ts`
- **Range:** line 351, col 8
- **Selection:** `go_to_source_definition_primary`

```typescript
  async getTeamMember(
    teamID: string,
    userUid: string,
  ): Promise<TeamMember | null> {
    try {
      const teamMember = await this.prisma.teamMember.findUnique({
        where: {
          teamID_userUid: {
            teamID,
            userUid,
          },
        },
      });

      if (!teamMember) return null;

      return <TeamMember>{
        membershipID: teamMember.id,
        userUid: userUid,
        role: TeamAccessRole[teamMember.role],
      };
    } catch (e) {
      return null;
    }
  }
```

---

## 124. Sample 46 · callee #6

- **Function:** `acceptInvitation`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-invitation/team-invitation.service.ts`
- **Callee:** `this.teamService.addMemberToTeam(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 221, col 43 — pattern `core_fallback`

```typescript
this.teamService.addMemberToTeam(...)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/team/team.service.ts`
- **Range:** line 74, col 8
- **Selection:** `go_to_source_definition_primary`

```typescript
  async addMemberToTeam(
    teamID: string,
    uid: string,
    role: TeamAccessRole,
  ): Promise<TeamMember> {
    const teamMember = await this.prisma.teamMember.create({
      data: {
        userUid: uid,
        team: {
          connect: {
            id: teamID,
          },
        },
        role: role,
      },
    });

    const member: TeamMember = {
      membershipID: teamMember.id,
      userUid: teamMember.userUid,
      role: TeamAccessRole[teamMember.role],
    };

    this.pubsub.publish(`team/${teamID}/member_added`, member);

    return member;
  }
```

---

## 125. Sample 46 · callee #9

- **Function:** `acceptInvitation`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-invitation/team-invitation.service.ts`
- **Callee:** `this.teamService`
- **Status:** OK

### Usage site (matched in test file)

Line 205, col 37 — pattern `anchor_substring`

```typescript
this.teamService
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/team-invitation/team-invitation.service.ts`
- **Range:** line 29, col 21
- **Selection:** `go_to_source_definition_primary`

```typescript
private readonly teamService: TeamService,
```

---

## 126. Sample 46 · callee #10

- **Function:** `acceptInvitation`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-invitation/team-invitation.service.ts`
- **Callee:** `inviteeEmail.toLowerCase`
- **Status:** OK

### Usage site (matched in test file)

Line 214, col 24 — pattern `anchor_substring`

```typescript
inviteeEmail.toLowerCase
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es5.d.ts`
- **Range:** line 496, col 51

```typescript
/** Converts all the alphabetic characters in a string to lowercase. */
    toLowerCase(): string;
```

---

## 127. Sample 48 · callee #2

- **Function:** `updateTeamRequest`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-request/team-request.service.ts`
- **Callee:** `this.prisma.teamRequest.update(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 57, col 60 — pattern `core_fallback`

```typescript
this.prisma.teamRequest.update(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 7687, col 248

```typescript
/**
     * Update one TeamRequest.
     * @param {TeamRequestUpdateArgs} args - Arguments to update one TeamRequest.
     * @example
     * // Update one TeamRequest
     * const teamRequest = await prisma.teamRequest.update({
     *   where: {
     *     // ... provide filter here
     *   },
     *   data: {
     *     // ... provide data here
     *   }
     * })
     * 
     */
    update<T extends TeamRequestUpdateArgs>(args: SelectSubset<T, TeamRequestUpdateArgs<ExtArgs>>): Prisma__TeamRequestClient<$Result.GetResult<Prisma.$TeamRequestPayload<ExtArgs>, T, "update", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>
```

---

## 128. Sample 48 · callee #3

- **Function:** `updateTeamRequest`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-request/team-request.service.ts`
- **Callee:** `this.cast(updatedTeamReq)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 62, col 40 — pattern `anchor_substring`

```typescript
this.cast(updatedTeamReq)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/team-request/team-request.service.ts`
- **Range:** line 31, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * A helper function to cast the Prisma TeamRequest model to the TeamRequest model
   * @param tr TeamRequest model from Prisma
   */
  private cast(tr: DbTeamRequest) {
    return {
      id: tr.id,
      collectionID: tr.collectionID,
      teamID: tr.teamID,
      title: tr.title,
      request: JSON.stringify(tr.request),
    };
  }
```

---

## 129. Sample 48 · callee #7

- **Function:** `updateTeamRequest`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-request/team-request.service.ts`
- **Callee:** `stringToJson(request)`
- **Status:** OK
- **Also seen in:** 2 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 52, col 25 — pattern `anchor_substring`

```typescript
stringToJson(request)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/utils.ts`
- **Range:** line 213, col 16
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
 * String to JSON parser
 * @param {str} str The string to parse
 * @returns {E.Right<T> | E.Left<"json_invalid">} An Either of the parsed JSON
 */
export function stringToJson<T>(
  str: string,
): E.Right<T | any> | E.Left<string> {
  try {
    return E.right(JSON.parse(str));
  } catch (err) {
    return E.left(JSON_INVALID);
  }
}
```

---

## 130. Sample 48 · callee #8

- **Function:** `updateTeamRequest`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-request/team-request.service.ts`
- **Callee:** `Prisma.TeamRequestUpdateInput`
- **Status:** OK

### Usage site (matched in test file)

Line 50, col 26 — pattern `anchor_substring`

```typescript
Prisma.TeamRequestUpdateInput
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 25652, col 3

```typescript
  }

  export type TeamRequestUpdateInput = {
    id?: StringFieldUpdateOperationsInput | string
    title?: StringFieldUpdateOperationsInput | string
    request?: JsonNullValueInput | InputJsonValue
    orderIndex?: IntFieldUpdateOperationsInput | number
    createdOn?: DateTimeFieldUpdateOperationsInput | Date | string
    updatedOn?: DateTimeFieldUpdateOperationsInput | Date | string
    collection?: TeamCollectionUpdateOneRequiredWithoutRequestsNestedInput
    team?: TeamUpdateOneRequiredWithoutTeamRequestNestedInput
  }
```

---

## 131. Sample 48 · callee #9

- **Function:** `updateTeamRequest`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-request/team-request.service.ts`
- **Callee:** `this.prisma`
- **Status:** OK
- **Also seen in:** 4 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 57, col 36 — pattern `anchor_substring`

```typescript
this.prisma
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/team-request/team-request.service.ts`
- **Range:** line 21, col 21
- **Selection:** `go_to_source_definition_primary`

```typescript
private readonly prisma: PrismaService,
```

---

## 132. Sample 48 · callee #10

- **Function:** `updateTeamRequest`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-request/team-request.service.ts`
- **Callee:** `this.pubsub`
- **Status:** OK

### Usage site (matched in test file)

Line 64, col 7 — pattern `anchor_substring`

```typescript
this.pubsub
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/team-request/team-request.service.ts`
- **Range:** line 24, col 21
- **Selection:** `go_to_source_definition_primary`

```typescript
private readonly pubsub: PubSubService,
```

---

## 133. Sample 49 · callee #0

- **Function:** `getRequest`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-request/team-request.service.ts`
- **Callee:** `this.prisma.teamRequest.findUnique(...)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 208, col 57 — pattern `core_fallback`

```typescript
this.prisma.teamRequest.findUnique(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 7546, col 106

```typescript
/**
     * Find zero or one TeamRequest that matches the filter.
     * @param {TeamRequestFindUniqueArgs} args - Arguments to find a TeamRequest
     * @example
     * // Get one TeamRequest
     * const teamRequest = await prisma.teamRequest.findUnique({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     */
    findUnique<T extends TeamRequestFindUniqueArgs>(args: SelectSubset<T, TeamRequestFindUniqueArgs<ExtArgs>>): Prisma__TeamRequestClient<$Result.GetResult<Prisma.$TeamRequestPayload<ExtArgs>, T, "findUnique", GlobalOmitOptions> | null, null, ExtArgs, GlobalOmitOptions>
```

---

## 134. Sample 49 · callee #1

- **Function:** `getRequest`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-request/team-request.service.ts`
- **Callee:** `O.some(this.cast(teamRequest))`
- **Status:** OK
- **Also seen in:** 4 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 211, col 14 — pattern `anchor_substring`

```typescript
O.some(this.cast(teamRequest))
```

### Resolved definition

- **Path:** `node_modules/.pnpm/fp-ts@2.16.10/node_modules/fp-ts/lib/Option.d.ts`
- **Range:** line 123, col 20
- **Selection:** `external_runtime_resolution_after_ts_nav`

```typescript
/**
 * Constructs a `Some`. Represents an optional value that exists.
 *
 * @category constructors
 * @since 2.0.0
 */
export declare const some: <A>(a: A) => Option<A>
```

### Runtime implementation

- **Export surface:** `node_modules/.pnpm/fp-ts@2.16.10/node_modules/fp-ts/lib/Option.js`

```typescript
/**
 * Constructs a `Some`. Represents an optional value that exists.
 *
 * @category constructors
 * @since 2.0.0
 */
exports.some = _.some;
```

- **Body:** `node_modules/.pnpm/fp-ts@2.16.10/node_modules/fp-ts/lib/internal.js`
- **Range:** line 25, col 0

```typescript
/** @internal */
var some = function (a) { return ({ _tag: 'Some', value: a }); };
```

---

## 135. Sample 49 · callee #4

- **Function:** `getRequest`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-request/team-request.service.ts`
- **Callee:** `O.none`
- **Status:** OK
- **Also seen in:** 4 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 213, col 14 — pattern `anchor_substring`

```typescript
O.none
```

### Resolved definition

- **Path:** `node_modules/.pnpm/fp-ts@2.16.10/node_modules/fp-ts/lib/Option.d.ts`
- **Range:** line 116, col 20
- **Selection:** `external_runtime_resolution_after_ts_nav`

```typescript
/**
 * `None` doesn't have a constructor, instead you can use it directly as a value. Represents a missing value.
 *
 * @category constructors
 * @since 2.0.0
 */
export declare const none: Option<never>
```

### Runtime implementation

- **Export surface:** `node_modules/.pnpm/fp-ts@2.16.10/node_modules/fp-ts/lib/Option.js`

```typescript
// -------------------------------------------------------------------------------------
// constructors
// -------------------------------------------------------------------------------------
/**
 * `None` doesn't have a constructor, instead you can use it directly as a value. Represents a missing value.
 *
 * @category constructors
 * @since 2.0.0
 */
exports.none = _.none;
```

- **Body:** `node_modules/.pnpm/fp-ts@2.16.10/node_modules/fp-ts/lib/internal.js`
- **Range:** line 23, col 0

```typescript
/** @internal */
exports.none = { _tag: 'None' };
```

---

## 136. Sample 50 · callee #4

- **Function:** `getCollectionOfRequest`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-request/team-request.service.ts`
- **Callee:** `this.teamCollectionService`
- **Status:** OK

### Usage site (matched in test file)

Line 232, col 34 — pattern `anchor_substring`

```typescript
this.teamCollectionService
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/team-request/team-request.service.ts`
- **Range:** line 23, col 21
- **Selection:** `go_to_source_definition_primary`

```typescript
private readonly teamCollectionService: TeamCollectionService,
```

---

## 137. Sample 52 · callee #0

- **Function:** `totalRequestsInATeam`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/team-request/team-request.service.ts`
- **Callee:** `this.prisma.teamRequest.count(...)`
- **Status:** OK
- **Also seen in:** 3 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 434, col 57 — pattern `core_fallback`

```typescript
this.prisma.teamRequest.count(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 7786, col 248

```typescript
/**
     * Count the number of TeamRequests.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {TeamRequestCountArgs} args - Arguments to filter TeamRequests to count.
     * @example
     * // Count the number of TeamRequests
     * const count = await prisma.teamRequest.count({
     *   where: {
     *     // ... the filter for the TeamRequests we want to count
     *   }
     * })
    **/
    count<T extends TeamRequestCountArgs>(
      args?: Subset<T, TeamRequestCountArgs>,
    ): Prisma.PrismaPromise<
      T extends $Utils.Record<'select', any>
        ? T['select'] extends true
          ? number
          : GetScalarType<T['select'], TeamRequestCountAggregateOutputType>
        : number
    >
```

---

## 138. Sample 55 · callee #0

- **Function:** `findUserById`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/user/user.service.ts`
- **Callee:** `this.prisma.user.findUniqueOrThrow(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 87, col 43 — pattern `core_fallback`

```typescript
this.prisma.user.findUniqueOrThrow(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 10830, col 242

```typescript
/**
     * Find one User that matches the filter or throw an error with `error.code='P2025'`
     * if no matches were found.
     * @param {UserFindUniqueOrThrowArgs} args - Arguments to find a User
     * @example
     * // Get one User
     * const user = await prisma.user.findUniqueOrThrow({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     */
    findUniqueOrThrow<T extends UserFindUniqueOrThrowArgs>(args: SelectSubset<T, UserFindUniqueOrThrowArgs<ExtArgs>>): Prisma__UserClient<$Result.GetResult<Prisma.$UserPayload<ExtArgs>, T, "findUniqueOrThrow", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>
```

---

## 139. Sample 55 · callee #2

- **Function:** `findUserById`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/user/user.service.ts`
- **Callee:** `this.prisma`
- **Status:** OK
- **Also seen in:** 6 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 87, col 26 — pattern `anchor_substring`

```typescript
this.prisma
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/user/user.service.ts`
- **Range:** line 28, col 21
- **Selection:** `go_to_source_definition_primary`

```typescript
private readonly prisma: PrismaService,
```

---

## 140. Sample 57 · callee #1

- **Function:** `updateUserDisplayName`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/user/user.service.ts`
- **Callee:** `this.prisma.user.update(...)`
- **Status:** OK
- **Also seen in:** 3 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 307, col 52 — pattern `core_fallback`

```typescript
this.prisma.user.update(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 10959, col 220

```typescript
/**
     * Update one User.
     * @param {UserUpdateArgs} args - Arguments to update one User.
     * @example
     * // Update one User
     * const user = await prisma.user.update({
     *   where: {
     *     // ... provide filter here
     *   },
     *   data: {
     *     // ... provide data here
     *   }
     * })
     * 
     */
    update<T extends UserUpdateArgs>(args: SelectSubset<T, UserUpdateArgs<ExtArgs>>): Prisma__UserClient<$Result.GetResult<Prisma.$UserPayload<ExtArgs>, T, "update", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>
```

---

## 141. Sample 57 · callee #2

- **Function:** `updateUserDisplayName`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/user/user.service.ts`
- **Callee:** `this.convertDbUserToUser(dbUpdatedUser)`
- **Status:** OK

### Usage site (matched in test file)

Line 312, col 27 — pattern `anchor_substring`

```typescript
this.convertDbUserToUser(dbUpdatedUser)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/user/user.service.ts`
- **Range:** line 44, col 2
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Converts a prisma user object to a user object
   *
   * @param dbUser Prisma User object
   * @returns  User object
   */
  convertDbUserToUser(dbUser: DbUser): User {
    const dbCurrentRESTSession = dbUser.currentRESTSession;
    const dbCurrentGQLSession = dbUser.currentGQLSession;

    return {
      ...dbUser,
      currentRESTSession: dbCurrentRESTSession
        ? JSON.stringify(dbCurrentRESTSession)
        : null,
      currentGQLSession: dbCurrentGQLSession
        ? JSON.stringify(dbCurrentGQLSession)
        : null,
    };
  }
```

---

## 142. Sample 57 · callee #8

- **Function:** `updateUserDisplayName`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/user/user.service.ts`
- **Callee:** `this.pubsub`
- **Status:** OK

### Usage site (matched in test file)

Line 315, col 13 — pattern `anchor_substring`

```typescript
this.pubsub
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/user/user.service.ts`
- **Range:** line 29, col 21
- **Selection:** `go_to_source_definition_primary`

```typescript
private readonly pubsub: PubSubService,
```

---

## 143. Sample 60 · callee #0

- **Function:** `makeAdmins`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/user/user.service.ts`
- **Callee:** `this.prisma.user.updateMany(...)`
- **Status:** OK
- **Also seen in:** 3 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 457, col 30 — pattern `core_fallback`

```typescript
this.prisma.user.updateMany(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 10990, col 133

```typescript
/**
     * Update zero or more Users.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {UserUpdateManyArgs} args - Arguments to update one or more rows.
     * @example
     * // Update many Users
     * const user = await prisma.user.updateMany({
     *   where: {
     *     // ... provide filter here
     *   },
     *   data: {
     *     // ... provide data here
     *   }
     * })
     * 
     */
    updateMany<T extends UserUpdateManyArgs>(args: SelectSubset<T, UserUpdateManyArgs<ExtArgs>>): Prisma.PrismaPromise<BatchPayload>
```

---

## 144. Sample 61 · callee #0

- **Function:** `deleteUserAccount`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/user/user.service.ts`
- **Callee:** `this.prisma.user.delete(...)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 488, col 30 — pattern `core_fallback`

```typescript
this.prisma.user.delete(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 10945, col 240

```typescript
/**
     * Delete a User.
     * @param {UserDeleteArgs} args - Arguments to delete one User.
     * @example
     * // Delete one User
     * const User = await prisma.user.delete({
     *   where: {
     *     // ... filter to delete one User
     *   }
     * })
     * 
     */
    delete<T extends UserDeleteArgs>(args: SelectSubset<T, UserDeleteArgs<ExtArgs>>): Prisma__UserClient<$Result.GetResult<Prisma.$UserPayload<ExtArgs>, T, "delete", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>
```

---

## 145. Sample 63 · callee #0

- **Function:** `cast`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/user-collection/user-collection.service.ts`
- **Callee:** `transformCollectionData(collection.data)`
- **Status:** OK

### Usage site (matched in test file)

Line 51, col 18 — pattern `anchor_substring`

```typescript
transformCollectionData(collection.data)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/utils.ts`
- **Range:** line 320, col 16
- **Selection:** `go_to_source_definition_primary`

```typescript
/*
 * Transforms the collection level properties (authorization & headers) under the `data` field.
 * Preserves `null` values and prevents duplicate stringification.
 *
 * @param {Prisma.JsonValue} collectionData - The team collection data to transform.
 * @returns {string | null} The transformed team collection data as a string.
 */
export function transformCollectionData(
  collectionData: Prisma.JsonValue,
): string | null {
  if (!collectionData) {
    return null;
  }

  return typeof collectionData === 'string'
    ? collectionData
    : JSON.stringify(collectionData);
}
```

---

## 146. Sample 64 · callee #0

- **Function:** `getChildCollectionsCount`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/user-collection/user-collection.service.ts`
- **Callee:** `this.prisma.userCollection.findMany(...)`
- **Status:** OK
- **Also seen in:** 3 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 71, col 67 — pattern `core_fallback`

```typescript
this.prisma.userCollection.findMany(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 19774, col 301

```typescript
/**
     * Find zero or more UserCollections that matches the filter.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {UserCollectionFindManyArgs} args - Arguments to filter and select certain fields only.
     * @example
     * // Get all UserCollections
     * const userCollections = await prisma.userCollection.findMany()
     * 
     * // Get first 10 UserCollections
     * const userCollections = await prisma.userCollection.findMany({ take: 10 })
     * 
     * // Only select the `id`
     * const userCollectionWithIdOnly = await prisma.userCollection.findMany({ select: { id: true } })
     * 
     */
    findMany<T extends UserCollectionFindManyArgs>(args?: SelectSubset<T, UserCollectionFindManyArgs<ExtArgs>>): Prisma.PrismaPromise<$Result.GetResult<Prisma.$UserCollectionPayload<ExtArgs>, T, "findMany", GlobalOmitOptions>>
```

---

## 147. Sample 64 · callee #1

- **Function:** `getChildCollectionsCount`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/user-collection/user-collection.service.ts`
- **Callee:** `this.prisma`
- **Status:** OK
- **Also seen in:** 4 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 71, col 40 — pattern `anchor_substring`

```typescript
this.prisma
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/user-collection/user-collection.service.ts`
- **Range:** line 38, col 21
- **Selection:** `go_to_source_definition_primary`

```typescript
private readonly prisma: PrismaService,
```

---

## 148. Sample 65 · callee #0

- **Function:** `isOwnerCheck`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/user-collection/user-collection.service.ts`
- **Callee:** `this.prisma.userCollection.findFirstOrThrow(...)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 108, col 40 — pattern `core_fallback`

```typescript
this.prisma.userCollection.findFirstOrThrow(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 19758, col 279

```typescript
/**
     * Find the first UserCollection that matches the filter or
     * throw `PrismaKnownClientError` with `P2025` code if no matches were found.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {UserCollectionFindFirstOrThrowArgs} args - Arguments to find a UserCollection
     * @example
     * // Get one UserCollection
     * const userCollection = await prisma.userCollection.findFirstOrThrow({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     */
    findFirstOrThrow<T extends UserCollectionFindFirstOrThrowArgs>(args?: SelectSubset<T, UserCollectionFindFirstOrThrowArgs<ExtArgs>>): Prisma__UserCollectionClient<$Result.GetResult<Prisma.$UserCollectionPayload<ExtArgs>, T, "findFirstOrThrow", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>
```

---

## 149. Sample 66 · callee #0

- **Function:** `getUserOfCollection`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/user-collection/user-collection.service.ts`
- **Callee:** `this.prisma.userCollection.findUniqueOrThrow(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 129, col 63 — pattern `core_fallback`

```typescript
this.prisma.userCollection.findUniqueOrThrow(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 19729, col 282

```typescript
/**
     * Find one UserCollection that matches the filter or throw an error with `error.code='P2025'`
     * if no matches were found.
     * @param {UserCollectionFindUniqueOrThrowArgs} args - Arguments to find a UserCollection
     * @example
     * // Get one UserCollection
     * const userCollection = await prisma.userCollection.findUniqueOrThrow({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     */
    findUniqueOrThrow<T extends UserCollectionFindUniqueOrThrowArgs>(args: SelectSubset<T, UserCollectionFindUniqueOrThrowArgs<ExtArgs>>): Prisma__UserCollectionClient<$Result.GetResult<Prisma.$UserCollectionPayload<ExtArgs>, T, "findUniqueOrThrow", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>
```

---

## 150. Sample 67 · callee #2

- **Function:** `deleteCollectionData`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/user-collection/user-collection.service.ts`
- **Callee:** `this.deleteUserCollection(coll.id, coll.userUid)`
- **Status:** OK

### Usage site (matched in test file)

Line 443, col 9 — pattern `anchor_substring`

```typescript
this.deleteUserCollection(coll.id, coll.userUid)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/user-collection/user-collection.service.ts`
- **Range:** line 485, col 8
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Delete a UserCollection
   *
   * @param collectionID The Collection Id
   * @param userID The User UID
   * @returns An Either of Boolean of deletion status
   */
  async deleteUserCollection(collectionID: string, userID: string) {
    // Get collection details of collectionID
    const collection = await this.getUserCollection(collectionID);
    if (E.isLeft(collection)) return E.left(USER_COLL_NOT_FOUND);

    // Check to see is the collection belongs to the user
    if (collection.right.userUid !== userID) return E.left(USER_NOT_OWNER);

    // Delete all child collections and requests in the collection
    const collectionData = await this.deleteCollectionData(collection.right);
    if (E.isLeft(collectionData)) return E.left(collectionData.left);

    return E.right(true);
  }
```

---

## 151. Sample 67 · callee #3

- **Function:** `deleteCollectionData`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/user-collection/user-collection.service.ts`
- **Callee:** `this.prisma.userRequest.deleteMany(...)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 448, col 35 — pattern `core_fallback`

```typescript
this.prisma.userRequest.deleteMany(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 18719, col 248

```typescript
/**
     * Delete zero or more UserRequests.
     * @param {UserRequestDeleteManyArgs} args - Arguments to filter UserRequests to delete.
     * @example
     * // Delete a few UserRequests
     * const { count } = await prisma.userRequest.deleteMany({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     * 
     */
    deleteMany<T extends UserRequestDeleteManyArgs>(args?: SelectSubset<T, UserRequestDeleteManyArgs<ExtArgs>>): Prisma.PrismaPromise<BatchPayload>
```

---

## 152. Sample 67 · callee #4

- **Function:** `deleteCollectionData`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/user-collection/user-collection.service.ts`
- **Callee:** `this.updateOrderIndex(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 455, col 16 — pattern `core_fallback`

```typescript
this.updateOrderIndex(...)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/user-collection/user-collection.service.ts`
- **Range:** line 570, col 3

```typescript
/**
   * Update the OrderIndex of all collections in given parentID
   *
   * @param parentID The Parent collectionID
   * @param orderIndexCondition Condition to decide what collections will be updated
   * @param dataCondition Increment/Decrement OrderIndex condition
   * @returns A Collection with updated OrderIndexes
   */
  private async updateOrderIndex(
    parentID: string,
    orderIndexCondition: Prisma.IntFilter,
    dataCondition: Prisma.IntFieldUpdateOperationsInput,
  ) {
    const updatedUserCollection = await this.prisma.userCollection.updateMany({
      where: {
        parentID: parentID,
        orderIndex: orderIndexCondition,
      },
      data: { orderIndex: dataCondition },
    });

    return updatedUserCollection;
  }
```

---

## 153. Sample 67 · callee #5

- **Function:** `deleteCollectionData`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/user-collection/user-collection.service.ts`
- **Callee:** `this.removeUserCollection(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 462, col 46 — pattern `core_fallback`

```typescript
this.removeUserCollection(...)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/user-collection/user-collection.service.ts`
- **Range:** line 403, col 3

```typescript
/**
   * Delete a UserCollection from the DB
   *
   * @param collectionID The Collection Id
   * @returns The deleted UserCollection
   */
  private async removeUserCollection(collectionID: string) {
    try {
      const deletedUserCollection = await this.prisma.userCollection.delete({
        where: {
          id: collectionID,
        },
      });

      return E.right(deletedUserCollection);
    } catch (error) {
      return E.left(USER_COLL_NOT_FOUND);
    }
  }
```

---

## 154. Sample 67 · callee #13

- **Function:** `deleteCollectionData`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/user-collection/user-collection.service.ts`
- **Callee:** `this.pubsub`
- **Status:** OK

### Usage site (matched in test file)

Line 468, col 5 — pattern `anchor_substring`

```typescript
this.pubsub
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/user-collection/user-collection.service.ts`
- **Range:** line 39, col 21
- **Selection:** `go_to_source_definition_primary`

```typescript
private readonly pubsub: PubSubService,
```

---

## 155. Sample 68 · callee #0

- **Function:** `getCollectionCount`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/user-collection/user-collection.service.ts`
- **Callee:** `this.prisma.userCollection.count(...)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 701, col 39 — pattern `core_fallback`

```typescript
this.prisma.userCollection.count(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 19957, col 260

```typescript
/**
     * Count the number of UserCollections.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {UserCollectionCountArgs} args - Arguments to filter UserCollections to count.
     * @example
     * // Count the number of UserCollections
     * const count = await prisma.userCollection.count({
     *   where: {
     *     // ... the filter for the UserCollections we want to count
     *   }
     * })
    **/
    count<T extends UserCollectionCountArgs>(
      args?: Subset<T, UserCollectionCountArgs>,
    ): Prisma.PrismaPromise<
      T extends $Utils.Record<'select', any>
        ? T['select'] extends true
          ? number
          : GetScalarType<T['select'], UserCollectionCountAggregateOutputType>
        : number
    >
```

---

## 156. Sample 69 · callee #0

- **Function:** `deleteUserEnvironments`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/user-environment/user-environments.service.ts`
- **Callee:** `this.prisma.userEnvironment.deleteMany(...)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 210, col 67 — pattern `core_fallback`

```typescript
this.prisma.userEnvironment.deleteMany(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 16531, col 264

```typescript
/**
     * Delete zero or more UserEnvironments.
     * @param {UserEnvironmentDeleteManyArgs} args - Arguments to filter UserEnvironments to delete.
     * @example
     * // Delete a few UserEnvironments
     * const { count } = await prisma.userEnvironment.deleteMany({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     * 
     */
    deleteMany<T extends UserEnvironmentDeleteManyArgs>(args?: SelectSubset<T, UserEnvironmentDeleteManyArgs<ExtArgs>>): Prisma.PrismaPromise<BatchPayload>
```

---

## 157. Sample 69 · callee #2

- **Function:** `deleteUserEnvironments`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/user-environment/user-environments.service.ts`
- **Callee:** `this.prisma`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 210, col 39 — pattern `anchor_substring`

```typescript
this.prisma
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/user-environment/user-environments.service.ts`
- **Range:** line 20, col 21
- **Selection:** `go_to_source_definition_primary`

```typescript
private readonly prisma: PrismaService,
```

---

## 158. Sample 69 · callee #4

- **Function:** `deleteUserEnvironments`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/user-environment/user-environments.service.ts`
- **Callee:** `this.pubsub`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 218, col 11 — pattern `anchor_substring`

```typescript
this.pubsub
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/user-environment/user-environments.service.ts`
- **Range:** line 21, col 21
- **Selection:** `go_to_source_definition_primary`

```typescript
private readonly pubsub: PubSubService,
```

---

## 159. Sample 70 · callee #0

- **Function:** `clearGlobalEnvironments`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/user-environment/user-environments.service.ts`
- **Callee:** `this.checkForExistingGlobalEnv(uid)`
- **Status:** OK

### Usage site (matched in test file)

Line 233, col 35 — pattern `anchor_substring`

```typescript
this.checkForExistingGlobalEnv(uid)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/user-environment/user-environments.service.ts`
- **Range:** line 263, col 3

```typescript
// Method to check for existing global environments for a given user uid
  private async checkForExistingGlobalEnv(uid: string) {
    const globalEnv = await this.prisma.userEnvironment.findFirst({
      where: {
        userUid: uid,
        isGlobal: true,
      },
    });

    if (globalEnv == null) return O.none;
    return O.some(globalEnv);
  }
```

---

## 160. Sample 70 · callee #3

- **Function:** `clearGlobalEnvironments`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/user-environment/user-environments.service.ts`
- **Callee:** `this.prisma.userEnvironment.update(...)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 240, col 70 — pattern `core_fallback`

```typescript
this.prisma.userEnvironment.update(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 16514, col 264

```typescript
/**
     * Update one UserEnvironment.
     * @param {UserEnvironmentUpdateArgs} args - Arguments to update one UserEnvironment.
     * @example
     * // Update one UserEnvironment
     * const userEnvironment = await prisma.userEnvironment.update({
     *   where: {
     *     // ... provide filter here
     *   },
     *   data: {
     *     // ... provide data here
     *   }
     * })
     * 
     */
    update<T extends UserEnvironmentUpdateArgs>(args: SelectSubset<T, UserEnvironmentUpdateArgs<ExtArgs>>): Prisma__UserEnvironmentClient<$Result.GetResult<Prisma.$UserEnvironmentPayload<ExtArgs>, T, "update", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>
```

---

## 161. Sample 71 · callee #0

- **Function:** `toggleHistoryStarStatus`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/user-history/user-history.service.ts`
- **Callee:** `this.fetchUserHistoryByID(id)`
- **Status:** OK

### Usage site (matched in test file)

Line 102, col 31 — pattern `anchor_substring`

```typescript
this.fetchUserHistoryByID(id)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/user-history/user-history.service.ts`
- **Range:** line 211, col 8
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Fetch a user history based on history ID.
   * @param id User History ID
   * @returns an `UserHistory` object
   */
  async fetchUserHistoryByID(id: string) {
    const userHistory = await this.prisma.userHistory.findFirst({
      where: {
        id: id,
      },
    });
    if (userHistory == null) return O.none;

    return O.some(userHistory);
  }
```

---

## 162. Sample 71 · callee #3

- **Function:** `toggleHistoryStarStatus`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/user-history/user-history.service.ts`
- **Callee:** `this.prisma.userHistory.update(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 108, col 60 — pattern `core_fallback`

```typescript
this.prisma.userHistory.update(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 15458, col 248

```typescript
/**
     * Update one UserHistory.
     * @param {UserHistoryUpdateArgs} args - Arguments to update one UserHistory.
     * @example
     * // Update one UserHistory
     * const userHistory = await prisma.userHistory.update({
     *   where: {
     *     // ... provide filter here
     *   },
     *   data: {
     *     // ... provide data here
     *   }
     * })
     * 
     */
    update<T extends UserHistoryUpdateArgs>(args: SelectSubset<T, UserHistoryUpdateArgs<ExtArgs>>): Prisma__UserHistoryClient<$Result.GetResult<Prisma.$UserHistoryPayload<ExtArgs>, T, "update", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>
```

---

## 163. Sample 71 · callee #8

- **Function:** `toggleHistoryStarStatus`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/user-history/user-history.service.ts`
- **Callee:** `this.prisma`
- **Status:** OK
- **Also seen in:** 2 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 108, col 36 — pattern `anchor_substring`

```typescript
this.prisma
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/user-history/user-history.service.ts`
- **Range:** line 16, col 21
- **Selection:** `go_to_source_definition_primary`

```typescript
private readonly prisma: PrismaService,
```

---

## 164. Sample 71 · callee #9

- **Function:** `toggleHistoryStarStatus`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/user-history/user-history.service.ts`
- **Callee:** `this.pubsub`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 124, col 13 — pattern `anchor_substring`

```typescript
this.pubsub
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/user-history/user-history.service.ts`
- **Range:** line 17, col 21
- **Selection:** `go_to_source_definition_primary`

```typescript
private readonly pubsub: PubSubService,
```

---

## 165. Sample 72 · callee #0

- **Function:** `deleteAllHistories`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/user-history/user-history.service.ts`
- **Callee:** `this.prisma.userHistory.deleteMany()`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 198, col 13 — pattern `anchor_substring`

```typescript
this.prisma.userHistory.deleteMany()
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 15475, col 248

```typescript
/**
     * Delete zero or more UserHistories.
     * @param {UserHistoryDeleteManyArgs} args - Arguments to filter UserHistories to delete.
     * @example
     * // Delete a few UserHistories
     * const { count } = await prisma.userHistory.deleteMany({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     * 
     */
    deleteMany<T extends UserHistoryDeleteManyArgs>(args?: SelectSubset<T, UserHistoryDeleteManyArgs<ExtArgs>>): Prisma.PrismaPromise<BatchPayload>
```

---

## 166. Sample 73 · callee #0

- **Function:** `fetchUserHistoryByID`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/user-history/user-history.service.ts`
- **Callee:** `this.prisma.userHistory.findFirst(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 213, col 55 — pattern `core_fallback`

```typescript
this.prisma.userHistory.findFirst(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 15343, col 292

```typescript
/**
     * Find the first UserHistory that matches the filter.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {UserHistoryFindFirstArgs} args - Arguments to find a UserHistory
     * @example
     * // Get one UserHistory
     * const userHistory = await prisma.userHistory.findFirst({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     */
    findFirst<T extends UserHistoryFindFirstArgs>(args?: SelectSubset<T, UserHistoryFindFirstArgs<ExtArgs>>): Prisma__UserHistoryClient<$Result.GetResult<Prisma.$UserHistoryPayload<ExtArgs>, T, "findFirst", GlobalOmitOptions> | null, null, ExtArgs, GlobalOmitOptions>
```

---

## 167. Sample 74 · callee #3

- **Function:** `validateReqType`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/user-history/user-history.service.ts`
- **Callee:** `ReqType.REST`
- **Status:** OK

### Usage site (matched in test file)

Line 229, col 20 — pattern `anchor_substring`

```typescript
ReqType.REST
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/types/RequestTypes.ts`
- **Range:** line 1, col 2
- **Selection:** `go_to_source_definition_primary`

```typescript
REST = 'REST',
```

---

## 168. Sample 74 · callee #4

- **Function:** `validateReqType`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/user-history/user-history.service.ts`
- **Callee:** `ReqType.GQL`
- **Status:** OK

### Usage site (matched in test file)

Line 230, col 25 — pattern `anchor_substring`

```typescript
ReqType.GQL
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/types/RequestTypes.ts`
- **Range:** line 2, col 2
- **Selection:** `go_to_source_definition_primary`

```typescript
GQL = 'GQL',
```

---

## 169. Sample 75 · callee #3

- **Function:** `updateUserSettings`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/user-settings/user-settings.service.ts`
- **Callee:** `this.prisma.userSettings.update(...)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 93, col 66 — pattern `core_fallback`

```typescript
this.prisma.userSettings.update(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@prisma+client@6.8.2_prisma@6.8.2_typescript@5.8.3__typescript@5.8.3/node_modules/.prisma/client/index.d.ts`
- **Range:** line 14385, col 252

```typescript
/**
     * Update one UserSettings.
     * @param {UserSettingsUpdateArgs} args - Arguments to update one UserSettings.
     * @example
     * // Update one UserSettings
     * const userSettings = await prisma.userSettings.update({
     *   where: {
     *     // ... provide filter here
     *   },
     *   data: {
     *     // ... provide data here
     *   }
     * })
     * 
     */
    update<T extends UserSettingsUpdateArgs>(args: SelectSubset<T, UserSettingsUpdateArgs<ExtArgs>>): Prisma__UserSettingsClient<$Result.GetResult<Prisma.$UserSettingsPayload<ExtArgs>, T, "update", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>
```

---

## 170. Sample 75 · callee #4

- **Function:** `updateUserSettings`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/user-settings/user-settings.service.ts`
- **Callee:** `this.castToUserSettings(updatedUserSettings)`
- **Status:** OK

### Usage site (matched in test file)

Line 100, col 24 — pattern `anchor_substring`

```typescript
this.castToUserSettings(updatedUserSettings)
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/user-settings/user-settings.service.ts`
- **Range:** line 22, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
  private castToUserSettings(userSettings: DbUserSettings): UserSettings {
    return {
      ...userSettings,
      properties: JSON.stringify(userSettings.properties),
    };
  }
```

---

## 171. Sample 75 · callee #9

- **Function:** `updateUserSettings`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/user-settings/user-settings.service.ts`
- **Callee:** `this.prisma`
- **Status:** OK

### Usage site (matched in test file)

Line 93, col 41 — pattern `anchor_substring`

```typescript
this.prisma
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/user-settings/user-settings.service.ts`
- **Range:** line 18, col 21
- **Selection:** `go_to_source_definition_primary`

```typescript
private readonly prisma: PrismaService,
```

---

## 172. Sample 75 · callee #11

- **Function:** `updateUserSettings`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-backend/src/user-settings/user-settings.service.ts`
- **Callee:** `this.pubsub`
- **Status:** OK

### Usage site (matched in test file)

Line 103, col 13 — pattern `anchor_substring`

```typescript
this.pubsub
```

### Resolved definition

- **Path:** `packages/hoppscotch-backend/src/user-settings/user-settings.service.ts`
- **Range:** line 19, col 21
- **Selection:** `go_to_source_definition_primary`

```typescript
private readonly pubsub: PubSubService,
```

---

## 173. Sample 76 · callee #0

- **Function:** `pop`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/helpers/graphql/explorer.ts`
- **Callee:** `navStack.value.pop()`
- **Status:** OK

### Usage site (matched in test file)

Line 84, col 7 — pattern `anchor_substring`

```typescript
navStack.value.pop()
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es5.d.ts`
- **Range:** line 1334, col 29

```typescript
/**
     * Removes the last element from an array and returns it.
     * If the array is empty, undefined is returned and the array is not modified.
     */
    pop(): T | undefined;
```

---

## 174. Sample 76 · callee #1

- **Function:** `pop`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/helpers/graphql/explorer.ts`
- **Callee:** `navStack.value`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 83, col 9 — pattern `anchor_substring`

```typescript
navStack.value
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@vue+reactivity@3.5.12/node_modules/@vue/reactivity/dist/reactivity.d.ts`
- **Range:** line 417, col 39

```typescript
    get value(): T;
```

---

## 175. Sample 78 · callee #0

- **Function:** `unsubscribeSubscriptions`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Callee:** `this.teamCollectionAdded$`
- **Status:** OK

### Usage site (matched in test file)

Line 277, col 5 — pattern `anchor_substring`

```typescript
this.teamCollectionAdded$
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Range:** line 206, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
private teamCollectionAdded$: Subscription | null
```

---

## 176. Sample 78 · callee #1

- **Function:** `unsubscribeSubscriptions`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Callee:** `this.teamCollectionUpdated$`
- **Status:** OK

### Usage site (matched in test file)

Line 278, col 5 — pattern `anchor_substring`

```typescript
this.teamCollectionUpdated$
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Range:** line 207, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
private teamCollectionUpdated$: Subscription | null
```

---

## 177. Sample 78 · callee #2

- **Function:** `unsubscribeSubscriptions`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Callee:** `this.teamCollectionRemoved$`
- **Status:** OK

### Usage site (matched in test file)

Line 279, col 5 — pattern `anchor_substring`

```typescript
this.teamCollectionRemoved$
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Range:** line 208, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
private teamCollectionRemoved$: Subscription | null
```

---

## 178. Sample 78 · callee #3

- **Function:** `unsubscribeSubscriptions`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Callee:** `this.teamRequestAdded$`
- **Status:** OK

### Usage site (matched in test file)

Line 280, col 5 — pattern `anchor_substring`

```typescript
this.teamRequestAdded$
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Range:** line 209, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
private teamRequestAdded$: Subscription | null
```

---

## 179. Sample 78 · callee #4

- **Function:** `unsubscribeSubscriptions`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Callee:** `this.teamRequestDeleted$`
- **Status:** OK

### Usage site (matched in test file)

Line 281, col 5 — pattern `anchor_substring`

```typescript
this.teamRequestDeleted$
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Range:** line 211, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
private teamRequestDeleted$: Subscription | null
```

---

## 180. Sample 78 · callee #5

- **Function:** `unsubscribeSubscriptions`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Callee:** `this.teamRequestUpdated$`
- **Status:** OK

### Usage site (matched in test file)

Line 282, col 5 — pattern `anchor_substring`

```typescript
this.teamRequestUpdated$
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Range:** line 210, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
private teamRequestUpdated$: Subscription | null
```

---

## 181. Sample 78 · callee #6

- **Function:** `unsubscribeSubscriptions`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Callee:** `this.teamRequestMoved$`
- **Status:** OK

### Usage site (matched in test file)

Line 283, col 5 — pattern `anchor_substring`

```typescript
this.teamRequestMoved$
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Range:** line 212, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
private teamRequestMoved$: Subscription | null
```

---

## 182. Sample 78 · callee #7

- **Function:** `unsubscribeSubscriptions`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Callee:** `this.teamCollectionMoved$`
- **Status:** OK

### Usage site (matched in test file)

Line 284, col 5 — pattern `anchor_substring`

```typescript
this.teamCollectionMoved$
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Range:** line 213, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
private teamCollectionMoved$: Subscription | null
```

---

## 183. Sample 78 · callee #8

- **Function:** `unsubscribeSubscriptions`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Callee:** `this.teamRequestOrderUpdated$`
- **Status:** OK

### Usage site (matched in test file)

Line 285, col 5 — pattern `anchor_substring`

```typescript
this.teamRequestOrderUpdated$
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Range:** line 214, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
private teamRequestOrderUpdated$: Subscription | null
```

---

## 184. Sample 78 · callee #9

- **Function:** `unsubscribeSubscriptions`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Callee:** `this.teamCollectionOrderUpdated$`
- **Status:** OK

### Usage site (matched in test file)

Line 286, col 5 — pattern `anchor_substring`

```typescript
this.teamCollectionOrderUpdated$
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Range:** line 215, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
private teamCollectionOrderUpdated$: Subscription | null
```

---

## 185. Sample 78 · callee #10

- **Function:** `unsubscribeSubscriptions`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Callee:** `this.teamCollectionAddedSub`
- **Status:** OK

### Usage site (matched in test file)

Line 288, col 5 — pattern `anchor_substring`

```typescript
this.teamCollectionAddedSub
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Range:** line 217, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
private teamCollectionAddedSub: WSubscription | null
```

---

## 186. Sample 78 · callee #11

- **Function:** `unsubscribeSubscriptions`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Callee:** `this.teamCollectionUpdatedSub`
- **Status:** OK

### Usage site (matched in test file)

Line 289, col 5 — pattern `anchor_substring`

```typescript
this.teamCollectionUpdatedSub
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Range:** line 218, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
private teamCollectionUpdatedSub: WSubscription | null
```

---

## 187. Sample 78 · callee #12

- **Function:** `unsubscribeSubscriptions`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Callee:** `this.teamCollectionRemovedSub`
- **Status:** OK

### Usage site (matched in test file)

Line 290, col 5 — pattern `anchor_substring`

```typescript
this.teamCollectionRemovedSub
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Range:** line 219, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
private teamCollectionRemovedSub: WSubscription | null
```

---

## 188. Sample 78 · callee #13

- **Function:** `unsubscribeSubscriptions`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Callee:** `this.teamRequestAddedSub`
- **Status:** OK

### Usage site (matched in test file)

Line 291, col 5 — pattern `anchor_substring`

```typescript
this.teamRequestAddedSub
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Range:** line 220, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
private teamRequestAddedSub: WSubscription | null
```

---

## 189. Sample 78 · callee #14

- **Function:** `unsubscribeSubscriptions`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Callee:** `this.teamRequestDeletedSub`
- **Status:** OK

### Usage site (matched in test file)

Line 292, col 5 — pattern `anchor_substring`

```typescript
this.teamRequestDeletedSub
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Range:** line 222, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
private teamRequestDeletedSub: WSubscription | null
```

---

## 190. Sample 78 · callee #15

- **Function:** `unsubscribeSubscriptions`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Callee:** `this.teamRequestUpdatedSub`
- **Status:** OK

### Usage site (matched in test file)

Line 293, col 5 — pattern `anchor_substring`

```typescript
this.teamRequestUpdatedSub
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Range:** line 221, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
private teamRequestUpdatedSub: WSubscription | null
```

---

## 191. Sample 78 · callee #16

- **Function:** `unsubscribeSubscriptions`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Callee:** `this.teamRequestMovedSub`
- **Status:** OK

### Usage site (matched in test file)

Line 294, col 5 — pattern `anchor_substring`

```typescript
this.teamRequestMovedSub
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Range:** line 223, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
private teamRequestMovedSub: WSubscription | null
```

---

## 192. Sample 78 · callee #17

- **Function:** `unsubscribeSubscriptions`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Callee:** `this.teamCollectionMovedSub`
- **Status:** OK

### Usage site (matched in test file)

Line 295, col 5 — pattern `anchor_substring`

```typescript
this.teamCollectionMovedSub
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Range:** line 224, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
private teamCollectionMovedSub: WSubscription | null
```

---

## 193. Sample 78 · callee #18

- **Function:** `unsubscribeSubscriptions`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Callee:** `this.teamRequestOrderUpdatedSub`
- **Status:** OK

### Usage site (matched in test file)

Line 296, col 5 — pattern `anchor_substring`

```typescript
this.teamRequestOrderUpdatedSub
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Range:** line 225, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
private teamRequestOrderUpdatedSub: WSubscription | null
```

---

## 194. Sample 78 · callee #19

- **Function:** `unsubscribeSubscriptions`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Callee:** `this.teamCollectionOrderUpdatedSub`
- **Status:** OK

### Usage site (matched in test file)

Line 297, col 5 — pattern `anchor_substring`

```typescript
this.teamCollectionOrderUpdatedSub
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Range:** line 226, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
private teamCollectionOrderUpdatedSub: WSubscription | null
```

---

## 195. Sample 79 · callee #0

- **Function:** `removeRequest`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Callee:** `this.collections$`
- **Status:** OK
- **Also seen in:** 3 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 479, col 18 — pattern `anchor_substring`

```typescript
this.collections$
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Range:** line 195, col 2
- **Selection:** `go_to_source_definition_primary`

```typescript
collections$: BehaviorSubject<TeamCollection[]>
```

---

## 196. Sample 80 · callee #0

- **Function:** `moveRequest`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Callee:** `this.removeRequest(request.id)`
- **Status:** OK

### Usage site (matched in test file)

Line 504, col 5 — pattern `anchor_substring`

```typescript
this.removeRequest(request.id)
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Range:** line 477, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Removes a request from the tree
   *
   * @param {string} requestID - ID of the request to remove
   */
  private removeRequest(requestID: string) {
    const tree = this.collections$.value

    // Find request in tree, don't attempt if no collection or no requests (expansion?)
    const coll = findCollWithReqIDInTree(tree, requestID)
    if (!coll || !coll.requests) return

    // Remove the collection
    remove(coll.requests, (req) => req.id === requestID)

    // Remove from entityIDs set
    this.entityIDs.delete(`request-${requestID}`)

    // Publish new tree
    this.collections$.next(tree)
  }
```

---

## 197. Sample 81 · callee #0

- **Function:** `expandCollection`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Callee:** `this.loadingCollections$.next(...)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 1011, col 30 — pattern `core_fallback`

```typescript
this.loadingCollections$.next(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/rxjs@7.8.1/node_modules/rxjs/src/internal/BehaviorSubject.ts`
- **Range:** line 35, col 2
- **Selection:** `go_to_source_definition_primary`

```typescript
  next(value: T): void {
    super.next((this._value = value));
  }
```

---

## 198. Sample 81 · callee #1

- **Function:** `expandCollection`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Callee:** `this.loadingCollections$.getValue()`
- **Status:** OK

### Usage site (matched in test file)

Line 1012, col 10 — pattern `anchor_substring`

```typescript
this.loadingCollections$.getValue()
```

### Resolved definition

- **Path:** `node_modules/.pnpm/rxjs@7.8.1/node_modules/rxjs/src/internal/BehaviorSubject.ts`
- **Range:** line 26, col 2
- **Selection:** `go_to_source_definition_primary`

```typescript
  getValue(): T {
    const { hasError, thrownError, _value } = this;
    if (hasError) {
      throw thrownError;
    }
    this._throwIfClosed();
    return _value;
  }
```

---

## 199. Sample 81 · callee #3

- **Function:** `expandCollection`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Callee:** `this.getCollectionChildren(collection)`
- **Status:** OK

### Usage site (matched in test file)

Line 1018, col 9 — pattern `anchor_substring`

```typescript
this.getCollectionChildren(collection)
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Range:** line 910, col 3

```typescript
  private async getCollectionChildren(
    collection: TeamCollection
  ): Promise<TeamCollection[]> {
    const collections: TeamCollection[] = []

    while (true) {
      const data = await runGQLQuery({
        query: GetCollectionChildrenDocument,
        variables: {
          collectionID: collection.id,
          cursor:
            collections.length > 0
              ? collections[collections.length - 1].id
              : undefined,
        },
      })

      if (E.isLeft(data)) {
        throw new Error(
          `Child Collection Fetch Error for ${collection.id}: ${data.left}`
        )
      }

      collections.push(
        ...data.right.collection!.children.map(
          (el) =>
            <TeamCollection>{
              id: el.id,
              title: el.title,
              data: el.data,
              children: null,
              requests: null,
            }
        )
      )

      if (data.right.collection!.children.length !== TEAMS_BACKEND_PAGE_SIZE)
        break
    }

    return collections
  }
```

---

## 200. Sample 81 · callee #4

- **Function:** `expandCollection`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Callee:** `this.getCollectionRequests(collection)`
- **Status:** OK

### Usage site (matched in test file)

Line 1019, col 9 — pattern `anchor_substring`

```typescript
this.getCollectionRequests(collection)
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Range:** line 953, col 3

```typescript
  private async getCollectionRequests(
    collection: TeamCollection
  ): Promise<TeamRequest[]> {
    const requests: TeamRequest[] = []

    while (true) {
      const data = await runGQLQuery({
        query: GetCollectionRequestsDocument,
        variables: {
          collectionID: collection.id,
          cursor:
            requests.length > 0 ? requests[requests.length - 1].id : undefined,
        },
      })

      if (E.isLeft(data)) {
        throw new Error(`Child Request Fetch Error for ${data}: ${data.left}`)
      }

      requests.push(
        ...data.right.requestsInCollection.map<TeamRequest>((el) => {
          return {
            id: el.id,
            collectionID: collection.id,
            title: el.title,
            request: translateToNewRequest(JSON.parse(el.request)),
          }
        })
      )

      if (data.right.requestsInCollection.length !== TEAMS_BACKEND_PAGE_SIZE)
        break
    }

    return requests
  }
```

---

## 201. Sample 81 · callee #5

- **Function:** `expandCollection`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Callee:** `collections.forEach((coll) => this.entityIDs.add(`collection-${coll.id}`))`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 1026, col 7 — pattern `anchor_substring`

```typescript
collections.forEach((coll) => this.entityIDs.add(`collection-${coll.id}`))
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es5.d.ts`
- **Range:** line 1455, col 94

```typescript
/**
     * Performs the specified action for each element in an array.
     * @param callbackfn A function that accepts up to three arguments. forEach calls the callbackfn function one time for each element in the array.
     * @param thisArg An object to which the this keyword can refer in the callbackfn function. If thisArg is omitted, undefined is used as the this value.
     */
    forEach(callbackfn: (value: T, index: number, array: T[]) => void, thisArg?: any): void;
```

---

## 202. Sample 81 · callee #6

- **Function:** `expandCollection`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Callee:** `this.entityIDs.add(`collection-${coll.id}`)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 1026, col 37 — pattern `anchor_substring`

```typescript
this.entityIDs.add(`collection-${coll.id}`)
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es2015.collection.d.ts`
- **Range:** line 89, col 18

```typescript
/**
     * Appends a new element with a specified value to the end of the Set.
     */
    add(value: T): this;
```

---

## 203. Sample 81 · callee #10

- **Function:** `expandCollection`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Callee:** `findCollInTree(tree, collectionID)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 1005, col 24 — pattern `anchor_substring`

```typescript
findCollInTree(tree, collectionID)
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Range:** line 67, col 9
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
 * Finds and returns a REFERENCE collection in the given tree (or null)
 *
 * @param {TeamCollection[]} tree - The tree to look in
 * @param {string} targetID - The ID of the collection to look for
 *
 * @returns REFERENCE to the collection or null if not found
 */
function findCollInTree(
  tree: TeamCollection[],
  targetID: string
): TeamCollection | null {
  for (const coll of tree) {
    // If the direct child matched, then return that
    if (coll.id === targetID) return coll

    // Else run it in the children
    if (coll.children) {
      const result = findCollInTree(coll.children, targetID)
      if (result) return result
    }
  }

  // If nothing matched, return null
  return null
}
```

---

## 204. Sample 81 · callee #12

- **Function:** `expandCollection`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Callee:** `this.loadingCollections$`
- **Status:** OK

### Usage site (matched in test file)

Line 1011, col 5 — pattern `anchor_substring`

```typescript
this.loadingCollections$
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Range:** line 198, col 2
- **Selection:** `go_to_source_definition_primary`

```typescript
// Stream to the list of collections/folders that are being loaded in
// Stream to the list of collections/folders that are being loaded in
  loadingCollections$: BehaviorSubject<string[]>
```

---

## 205. Sample 81 · callee #13

- **Function:** `expandCollection`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Callee:** `this.entityIDs`
- **Status:** OK

### Usage site (matched in test file)

Line 1026, col 37 — pattern `anchor_substring`

```typescript
this.entityIDs
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Range:** line 204, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Stores the entity (collection/request/folder) ids of all the loaded entities.
   * Used for preventing duplication of data which definitely is not possible (duplication due to network problems etc.)
   */
/**
   * Stores the entity (collection/request/folder) ids of all the loaded entities.
   * Used for preventing duplication of data which definitely is not possible (duplication due to network problems etc.)
   */
  private entityIDs: Set<EntityID>
```

---

## 206. Sample 82 · callee #0

- **Function:** `cascadeParentCollectionForHeaderAuth`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/helpers/teams/TeamCollectionAdapter.ts`
- **Callee:** `console.error("Invalid path:", folderPath)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 1059, col 7 — pattern `anchor_substring`

```typescript
console.error("Invalid path:", folderPath)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@types+node@22.7.6/node_modules/@types/node/console.d.ts`
- **Range:** line 164, col 41

```typescript
/**
             * Prints to `stderr` with newline. Multiple arguments can be passed, with the
             * first used as the primary message and all additional used as substitution
             * values similar to [`printf(3)`](http://man7.org/linux/man-pages/man3/printf.3.html)
             * (the arguments are all passed to [`util.format()`](https://nodejs.org/docs/latest-v22.x/api/util.html#utilformatformat-args)).
             *
             * ```js
             * const code = 5;
             * console.error('error #%d', code);
             * // Prints: error #5, to stderr
             * console.error('error', code);
             * // Prints: error 5, to stderr
             * ```
             *
             * If formatting elements (e.g. `%d`) are not found in the first string then
             * [`util.inspect()`](https://nodejs.org/docs/latest-v22.x/api/util.html#utilinspectobject-options) is called on each argument and the
             * resulting string values are concatenated. See [`util.format()`](https://nodejs.org/docs/latest-v22.x/api/util.html#utilformatformat-args)
             * for more information.
             * @since v0.1.100
             */
            error(message?: any, ...optionalParams: any[]): void;
```

---

## 207. Sample 84 · callee #0

- **Function:** `registerMenu`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/services/context-menu/index.ts`
- **Callee:** `this.menus.set(menu.menuID, menu)`
- **Status:** OK
- **Also seen in:** 3 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 95, col 5 — pattern `anchor_substring`

```typescript
this.menus.set(menu.menuID, menu)
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es2015.collection.d.ts`
- **Range:** line 37, col 25

```typescript
/**
     * Adds a new element with a specified key and value to the Map. If an element with the same key already exists, the element will be updated.
     */
    set(key: K, value: V): this;
```

---

## 208. Sample 84 · callee #1

- **Function:** `registerMenu`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/services/context-menu/index.ts`
- **Callee:** `this.menus`
- **Status:** OK

### Usage site (matched in test file)

Line 95, col 5 — pattern `anchor_substring`

```typescript
this.menus
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/services/context-menu/index.ts`
- **Range:** line 87, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
    const menus = Array.from(this.menus.values()).map((x) => x.getMenuFor(text))
```

---

## 209. Sample 85 · callee #0

- **Function:** `addParameter`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/services/context-menu/menu/parameter.menu.ts`
- **Callee:** `this.extractParams(text)`
- **Status:** OK

### Usage site (matched in test file)

Line 83, col 32 — pattern `anchor_substring`

```typescript
this.extractParams(text)
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/services/context-menu/menu/parameter.menu.ts`
- **Range:** line 52, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   *
   * @param input The input to extract the parameters from
   * @returns The extracted parameters and the new URL if it was provided
   */
  private extractParams(input: string): ExtractedParams {
    let text = input
    let newURL: string | undefined

    // if the input is a URL, extract the parameters
    if (text.startsWith("http")) {
      const url = new URL(text)
      newURL = url.origin + url.pathname
      text = url.search.slice(1)
    }

    const regex = /([^&=]+)=([^&]+)/g
    const matches = text.matchAll(regex)
    const params: Param = {}

    // extract the parameters from the input
    for (const match of matches) {
      const [, key, value] = match
      params[key] = value
    }

    return { params, newURL }
  }
```

---

## 210. Sample 85 · callee #1

- **Function:** `addParameter`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/services/context-menu/menu/parameter.menu.ts`
- **Callee:** `Object.entries(params)`
- **Status:** OK

### Usage site (matched in test file)

Line 86, col 32 — pattern `anchor_substring`

```typescript
Object.entries(params)
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

## 211. Sample 85 · callee #2

- **Function:** `addParameter`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/services/context-menu/menu/parameter.menu.ts`
- **Callee:** `getService(RESTTabService)`
- **Status:** OK

### Usage site (matched in test file)

Line 90, col 24 — pattern `anchor_substring`

```typescript
getService(RESTTabService)
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/modules/dioc.ts`
- **Range:** line 24, col 16
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
 * Gets a service from the app service container. You can use this function
 * to get a service if you have no access to the container or if you are not
 * in a component (if you are, you can use `useService`) or if you are not in a
 * service.
 * @param service The class of the service to get
 * @returns The service instance
 *
 * @deprecated This is a temporary escape hatch for legacy code to access
 * services. Please use `useService` if within components or try to convert your
 * legacy subsystem into a service if possible.
 */
export function getService<T extends ServiceClassInstance<any>>(
  service: T
): InstanceType<T> {
  return serviceContainer.bind(service)
}
```

---

## 212. Sample 85 · callee #3

- **Function:** `addParameter`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/services/context-menu/menu/parameter.menu.ts`
- **Callee:** `RegExp(`\\b${text.replace(/\?/g, "")}\\b`, "gi")`
- **Status:** OK

### Usage site (matched in test file)

Line 110, col 29 — pattern `anchor_substring`

```typescript
RegExp(`\\b${text.replace(/\?/g, "")}\\b`, "gi")
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es5.d.ts`
- **Range:** line 988, col 1

```typescript
declare var RegExp: RegExpConstructor;
```

---

## 213. Sample 85 · callee #4

- **Function:** `addParameter`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/services/context-menu/menu/parameter.menu.ts`
- **Callee:** `value.document`
- **Status:** OK

### Usage site (matched in test file)

Line 92, col 37 — pattern `anchor_substring`

```typescript
value.document
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/services/tab/index.ts`
- **Range:** line 10, col 2
- **Selection:** `go_to_source_definition_primary`

```typescript
/** The document associated with the tab. */
/** The document associated with the tab. */
  document: Doc
```

---

## 214. Sample 85 · callee #5

- **Function:** `addParameter`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/services/context-menu/menu/parameter.menu.ts`
- **Callee:** `response.originalRequest`
- **Status:** OK

### Usage site (matched in test file)

Line 98, col 54 — pattern `anchor_substring`

```typescript
response.originalRequest
```

### Resolved definition

- **Path:** `packages/hoppscotch-data/dist/rest/v/13.d.ts`
- **Range:** line 2206, col 17

```typescript
originalRequest: {
```

---

## 215. Sample 86 · callee #0

- **Function:** `isValidURL`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/services/context-menu/menu/url.menu.ts`
- **Callee:** `URL(url)`
- **Status:** OK

### Usage site (matched in test file)

Line 23, col 9 — pattern `anchor_substring`

```typescript
URL(url)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@types+node@22.7.6/node_modules/@types/node/url.d.ts`
- **Range:** line 942, col 8
- **Selection:** `fast_path_refined_via_document_symbols`

```typescript
        interface URL extends _URL {}
```

---

## 216. Sample 87 · callee #0

- **Function:** `openNewTab`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/services/context-menu/menu/url.menu.ts`
- **Callee:** `this.restTab.createNewTab(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 57, col 18 — pattern `core_fallback`

```typescript
this.restTab.createNewTab(...)
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/services/tab/tab.ts`
- **Range:** line 69, col 9
- **Selection:** `go_to_source_definition_primary`

```typescript
  public createNewTab(document: Doc, switchToIt = true): HoppTab<Doc> {
    const id = this.generateNewTabID()

    const tab: HoppTab<Doc> = { id, document }

    this.tabMap.set(id, tab)
    this.tabOrdering.value.push(id)

    if (switchToIt) {
      this.setActiveTab(id)
    }

    return tab
  }
```

---

## 217. Sample 87 · callee #1

- **Function:** `openNewTab`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/services/context-menu/menu/url.menu.ts`
- **Callee:** `this.restTab`
- **Status:** OK

### Usage site (matched in test file)

Line 57, col 5 — pattern `anchor_substring`

```typescript
this.restTab
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/services/context-menu/menu/url.menu.ts`
- **Range:** line 38, col 62

```typescript
private readonly restTab = this.bind(RESTTabService)
```

---

## 218. Sample 88 · callee #0

- **Function:** `runRequest`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/services/interceptor.service.ts`
- **Callee:** `this.interceptors.get(this.currentInterceptorID.value)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 254, col 7 — pattern `anchor_substring`

```typescript
this.interceptors.get(this.currentInterceptorID.value)
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es2015.collection.d.ts`
- **Range:** line 28, col 89

```typescript
/**
     * Returns a specified element from the Map object. If the value that is associated to the provided key is an object, then you will get a reference to that object and any change made to that object will effectively modify it inside the Map.
     * @returns Returns the element associated with the specified key. If no element is associated with the specified key, undefined is returned.
     */
    get(key: K): V | undefined;
```

---

## 219. Sample 88 · callee #1

- **Function:** `runRequest`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/services/interceptor.service.ts`
- **Callee:** `Error("No interceptor selected")`
- **Status:** OK

### Usage site (matched in test file)

Line 250, col 17 — pattern `anchor_substring`

```typescript
Error("No interceptor selected")
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es5.d.ts`
- **Range:** line 1070, col 38

```typescript
declare var Error: ErrorConstructor;
```

---

## 220. Sample 88 · callee #2

- **Function:** `runRequest`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/services/interceptor.service.ts`
- **Callee:** `throwError(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 255, col 7 — pattern `core_fallback`

```typescript
throwError(...)
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/helpers/functional/error.ts`
- **Range:** line 0, col 13
- **Selection:** `go_to_source_definition_primary`

```typescript
export const throwError = (message: string): never => {
  throw new Error(message)
}
```

---

## 221. Sample 88 · callee #3

- **Function:** `runRequest`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/services/interceptor.service.ts`
- **Callee:** `this.currentInterceptorID`
- **Status:** OK

### Usage site (matched in test file)

Line 249, col 10 — pattern `anchor_substring`

```typescript
this.currentInterceptorID
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/services/interceptor.service.ts`
- **Range:** line 170, col 9
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * The ID of the currently selected interceptor.
   * If `null`, there are no interceptors registered or none can be selected.
   */
/**
   * The ID of the currently selected interceptor.
   * If `null`, there are no interceptors registered or none can be selected.
   */
  public currentInterceptorID: Ref<string | null> = refWithControl(
```

---

## 222. Sample 88 · callee #4

- **Function:** `runRequest`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/services/interceptor.service.ts`
- **Callee:** `this.interceptors`
- **Status:** OK

### Usage site (matched in test file)

Line 254, col 7 — pattern `anchor_substring`

```typescript
this.interceptors
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/services/interceptor.service.ts`
- **Range:** line 164, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
private interceptors: Map<string, Interceptor> = reactive(new Map())
```

---

## 223. Sample 89 · callee #0

- **Function:** `setLocalConfig`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/services/persistence/index.ts`
- **Callee:** `Store.set(STORE_NAMESPACE, key, value)`
- **Status:** OK

### Usage site (matched in test file)

Line 1047, col 11 — pattern `anchor_substring`

```typescript
Store.set(STORE_NAMESPACE, key, value)
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/kernel/store.ts`
- **Range:** line 21, col 4
- **Selection:** `go_to_source_definition_primary`

```typescript
set: async (
```

---

## 224. Sample 90 · callee #0

- **Function:** `removeLocalConfig`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/services/persistence/index.ts`
- **Callee:** `Store.remove(STORE_NAMESPACE, key)`
- **Status:** OK

### Usage site (matched in test file)

Line 1067, col 11 — pattern `anchor_substring`

```typescript
Store.remove(STORE_NAMESPACE, key)
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/kernel/store.ts`
- **Range:** line 37, col 4
- **Selection:** `go_to_source_definition_primary`

```typescript
remove: async (
```

---

## 225. Sample 91 · callee #1

- **Function:** `addSecretEnvironment`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/services/secret-environment.service.ts`
- **Callee:** `this.secretEnvironments`
- **Status:** OK
- **Also seen in:** 3 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 35, col 5 — pattern `anchor_substring`

```typescript
this.secretEnvironments
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/services/secret-environment.service.ts`
- **Range:** line 26, col 9
- **Selection:** `go_to_source_definition_primary`

```typescript
    const secretEnvironments: Record<string, SecretVariable[]> = {}
```

---

## 226. Sample 93 · callee #0

- **Function:** `getSecretEnvironmentVariable`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/services/secret-environment.service.ts`
- **Callee:** `this.getSecretEnvironment(id)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 52, col 24 — pattern `anchor_substring`

```typescript
this.getSecretEnvironment(id)
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/services/secret-environment.service.ts`
- **Range:** line 41, col 9
- **Selection:** `go_to_source_definition_primary`

```typescript
/**
   * Get a secret environment.
   * @param id ID of the environment
   */
  public getSecretEnvironment(id: string) {
    return this.secretEnvironments.get(id)
  }
```

---

## 227. Sample 95 · callee #0

- **Function:** `hasSecretValue`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/services/secret-environment.service.ts`
- **Callee:** `this.secretEnvironments.has(id)`
- **Status:** OK

### Usage site (matched in test file)

Line 123, col 7 — pattern `anchor_substring`

```typescript
this.secretEnvironments.has(id)
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es2015.collection.d.ts`
- **Range:** line 33, col 31

```typescript
/**
     * @returns boolean indicating whether an element with the specified key exists or not.
     */
    has(key: K): boolean;
```

---

## 228. Sample 96 · callee #0

- **Function:** `setDocuments`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/services/spotlight/searchers/base/static.searcher.ts`
- **Callee:** `this.addDocsToSearchIndex()`
- **Status:** OK

### Usage site (matched in test file)

Line 92, col 5 — pattern `anchor_substring`

```typescript
this.addDocsToSearchIndex()
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/services/spotlight/searchers/base/static.searcher.ts`
- **Range:** line 92, col 3

```typescript
  private async addDocsToSearchIndex() {
    this.loading.value = true

    this.minisearch = new MiniSearch({
      fields: this.opts.searchFields as string[],
    })

    await this.minisearch.addAllAsync(
      Object.entries(this._documents).map(([id, doc]) => ({
        id,
        ...doc,
      }))
    )

    this.loading.value = false
  }
```

---

## 229. Sample 96 · callee #1

- **Function:** `setDocuments`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/services/spotlight/searchers/base/static.searcher.ts`
- **Callee:** `this._documents`
- **Status:** OK

### Usage site (matched in test file)

Line 90, col 5 — pattern `anchor_substring`

```typescript
this._documents
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/services/spotlight/searchers/base/static.searcher.ts`
- **Range:** line 67, col 10
- **Selection:** `go_to_source_definition_primary`

```typescript
  private _documents: Record<string, Doc> = {}
```

---

## 230. Sample 97 · callee #1

- **Function:** `acquireTeamListAdapter`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/services/workspace.service.ts`
- **Callee:** `this.teamListAdapterLocks.delete(lockID)`
- **Status:** OK

### Usage site (matched in test file)

Line 140, col 7 — pattern `anchor_substring`

```typescript
this.teamListAdapterLocks.delete(lockID)
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es2015.collection.d.ts`
- **Range:** line 20, col 18

```typescript
/**
     * @returns true if an element in the Map existed and has been removed, or false if the element does not exist.
     */
    delete(key: K): boolean;
```

---

## 231. Sample 97 · callee #2

- **Function:** `acquireTeamListAdapter`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/services/workspace.service.ts`
- **Callee:** `tryOnScopeDispose(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 139, col 5 — pattern `core_fallback`

```typescript
tryOnScopeDispose(...)
```

### Resolved definition

- **Path:** `node_modules/.pnpm/@vueuse+shared@11.1.0_vue@3.5.12_typescript@5.8.3_/node_modules/@vueuse/shared/index.d.cts`
- **Range:** line 685, col 74
- **Selection:** `external_runtime_resolution_after_ts_nav`

```typescript
/**
 * Call onScopeDispose() if it's inside an effect scope lifecycle, if not, do nothing
 *
 * @param fn
 */
declare function tryOnScopeDispose(fn: Fn): boolean;
```

### Runtime implementation

- **Body:** `node_modules/.pnpm/@vueuse+shared@11.1.0_vue@3.5.12_typescript@5.8.3_/node_modules/@vueuse/shared/index.mjs`
- **Range:** line 48, col 0

```typescript
function tryOnScopeDispose(fn) {
  if (getCurrentScope()) {
    onScopeDispose(fn);
    return true;
  }
  return false;
}
```

---

## 232. Sample 97 · callee #3

- **Function:** `acquireTeamListAdapter`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/services/workspace.service.ts`
- **Callee:** `this.teamListAdapterLockTicker`
- **Status:** OK

### Usage site (matched in test file)

Line 135, col 20 — pattern `anchor_substring`

```typescript
this.teamListAdapterLockTicker
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/services/workspace.service.ts`
- **Range:** line 43, col 75

```typescript
private teamListAdapterLockTicker = 0 // Used to generate unique lock IDs
```

---

## 233. Sample 97 · callee #4

- **Function:** `acquireTeamListAdapter`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/services/workspace.service.ts`
- **Callee:** `this.teamListAdapterLocks`
- **Status:** OK

### Usage site (matched in test file)

Line 137, col 5 — pattern `anchor_substring`

```typescript
this.teamListAdapterLocks
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/services/workspace.service.ts`
- **Range:** line 41, col 60

```typescript
private teamListAdapterLocks = reactive(new Map<number, number | null>())
```

---

## 234. Sample 97 · callee #5

- **Function:** `acquireTeamListAdapter`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-common/src/services/workspace.service.ts`
- **Callee:** `this.managedTeamListAdapter`
- **Status:** OK

### Usage site (matched in test file)

Line 143, col 12 — pattern `anchor_substring`

```typescript
this.managedTeamListAdapter
```

### Resolved definition

- **Path:** `packages/hoppscotch-common/src/services/workspace.service.ts`
- **Range:** line 44, col 39

```typescript
private managedTeamListAdapter = new TeamListAdapter(true, false)
```

---

## 235. Sample 99 · callee #0

- **Function:** `willBackendHaveAuthError`
- **File:** `/Users/trieyang/Desktop/DocPrism/hoppscotch/packages/hoppscotch-selfhost-desktop/src/platform/auth.ts`
- **Callee:** `currentUser$.value`
- **Status:** OK

### Usage site (matched in test file)

Line 238, col 13 — pattern `anchor_substring`

```typescript
currentUser$.value
```

### Resolved definition

- **Path:** `node_modules/.pnpm/rxjs@7.8.1/node_modules/rxjs/src/internal/BehaviorSubject.ts`
- **Range:** line 15, col 6
- **Selection:** `go_to_source_definition_primary`

```typescript
  get value(): T {
    return this.getValue();
  }
```

---
