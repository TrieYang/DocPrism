# nest code navigation results

Generated from `code_navigation_TypeScript.resolve_from_snippet` on samples in `nest.json`.

## Summary

- Runtime: 47.21s
- Samples with at least one callee: 88
- Callee rows evaluated: 209 (205 ok, 4 failed)
- Samples skipped (no extractable callees): 6
- Unique resolved definitions shown below: 142 (deduped from 209 callee rows)

---

## 1. Sample 2 · callee #0

- **Function:** `initCause`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/exceptions/http.exception.ts`
- **Callee:** `this.options`
- **Status:** OK

### Usage site (matched in test file)

Line 85, col 9 — pattern `anchor_substring`

```typescript
this.options
```

### Resolved definition

- **Path:** `packages/common/exceptions/http.exception.ts`
- **Range:** line 69, col 21
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
private readonly options?: HttpExceptionOptions,
```

---

## 2. Sample 2 · callee #1

- **Function:** `initCause`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/exceptions/http.exception.ts`
- **Callee:** `this.cause`
- **Status:** OK

### Usage site (matched in test file)

Line 86, col 7 — pattern `anchor_substring`

```typescript
this.cause
```

### Resolved definition

- **Path:** `packages/common/exceptions/http.exception.ts`
- **Range:** line 31, col 9
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
   * Exception cause. Indicates the specific original cause of the error.
   * It is used when catching and re-throwing an error with a more-specific or useful error message in order to still have access to the original error.
   */
  public cause: unknown;
```

---

## 3. Sample 3 · callee #0

- **Function:** `setClassMethodName`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/module-utils/configurable-module.builder.ts`
- **Callee:** `this.options`
- **Status:** OK

### Usage site (matched in test file)

Line 136, col 7 — pattern `anchor_substring`

```typescript
this.options
```

### Resolved definition

- **Path:** `packages/common/module-utils/configurable-module.builder.ts`
- **Range:** line 69, col 23
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
protected readonly options: ConfigurableModuleBuilderOptions = {},
```

---

## 4. Sample 4 · callee #0

- **Function:** `getValidators`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/pipes/file/parse-file.pipe.ts`
- **Callee:** `this.validators`
- **Status:** OK

### Usage site (matched in test file)

Line 88, col 12 — pattern `anchor_substring`

```typescript
this.validators
```

### Resolved definition

- **Path:** `packages/common/pipes/file/parse-file.pipe.ts`
- **Range:** line 21, col 19
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  private readonly validators: FileValidator[];
```

---

## 5. Sample 5 · callee #0

- **Function:** `transform`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/pipes/parse-array.pipe.ts`
- **Callee:** `this.exceptionFactory(VALIDATION_ERROR_MESSAGE)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 82, col 13 — pattern `anchor_substring`

```typescript
this.exceptionFactory(VALIDATION_ERROR_MESSAGE)
```

### Resolved definition

- **Path:** `packages/common/pipes/parse-array.pipe.ts`
- **Range:** line 56, col 12
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  protected exceptionFactory: (error: string) => any;
```

---

## 6. Sample 5 · callee #1

- **Function:** `transform`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/pipes/parse-array.pipe.ts`
- **Callee:** `Array.isArray(value)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 87, col 10 — pattern `anchor_substring`

```typescript
Array.isArray(value)
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es5.d.ts`
- **Range:** line 1516, col 28

```typescript
    isArray(arg: any): arg is any[];
```

---

## 7. Sample 5 · callee #2

- **Function:** `transform`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/pipes/parse-array.pipe.ts`
- **Callee:** `this.isExpectedTypePrimitive()`
- **Status:** OK

### Usage site (matched in test file)

Line 106, col 39 — pattern `anchor_substring`

```typescript
this.isExpectedTypePrimitive()
```

### Resolved definition

- **Path:** `packages/common/pipes/parse-array.pipe.ts`
- **Range:** line 156, col 12
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  protected isExpectedTypePrimitive(): boolean {
    return [Boolean, Number, String].includes(this.options.items as any);
  }
```

---

## 8. Sample 5 · callee #3

- **Function:** `transform`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/pipes/parse-array.pipe.ts`
- **Callee:** `JSON.parse(item)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 110, col 20 — pattern `anchor_substring`

```typescript
JSON.parse(item)
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

## 9. Sample 5 · callee #4

- **Function:** `transform`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/pipes/parse-array.pipe.ts`
- **Callee:** `this.validatePrimitive(item, index)`
- **Status:** OK

### Usage site (matched in test file)

Line 116, col 18 — pattern `anchor_substring`

```typescript
this.validatePrimitive(item, index)
```

### Resolved definition

- **Path:** `packages/common/pipes/parse-array.pipe.ts`
- **Range:** line 160, col 12
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  protected validatePrimitive(originalValue: any, index?: number) {
    if (this.options.items === Number) {
      const value =
        originalValue !== null && originalValue !== '' ? +originalValue : NaN;
      if (isNaN(value)) {
        throw this.exceptionFactory(
          `${isUndefined(index) ? '' : `[${index}] `}item must be a number`,
        );
      }
      return value;
    } else if (this.options.items === String) {
      if (!isString(originalValue)) {
        return `${originalValue}`;
      }
    } else if (this.options.items === Boolean) {
      if (typeof originalValue !== 'boolean') {
        throw this.exceptionFactory(
          `${
            isUndefined(index) ? '' : `[${index}] `
          }item must be a boolean value`,
        );
      }
    }
    return originalValue;
  }
```

---

## 10. Sample 5 · callee #5

- **Function:** `transform`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/pipes/parse-array.pipe.ts`
- **Callee:** `this.validationPipe.transform(item, validationMetadata)`
- **Status:** OK

### Usage site (matched in test file)

Line 118, col 16 — pattern `anchor_substring`

```typescript
this.validationPipe.transform(item, validationMetadata)
```

### Resolved definition

- **Path:** `packages/common/pipes/validation.pipe.ts`
- **Range:** line 104, col 3

```typescript
  public async transform(value: any, metadata: ArgumentMetadata) {
    if (this.expectedType) {
      metadata = { ...metadata, metatype: this.expectedType };
    }

    const metatype = metadata.metatype;
    if (!metatype || !this.toValidate(metadata)) {
      return this.isTransformEnabled
        ? this.transformPrimitive(value, metadata)
        : value;
    }
    const originalValue = value;
    value = this.toEmptyIfNil(value, metatype);

    const isNil = value !== originalValue;
    const isPrimitive = this.isPrimitive(value);
    this.stripProtoKeys(value);
    let entity = classTransformer.plainToInstance(
      metatype,
      value,
      this.transformOptions,
    );

    const originalEntity = entity;
    const isCtorNotEqual = entity.constructor !== metatype;

    if (isCtorNotEqual && !isPrimitive) {
      entity.constructor = metatype;
    } else if (isCtorNotEqual) {
      // when "entity" is a primitive value, we have to temporarily
      // replace the entity to perform the validation against the original
      // metatype defined inside the handler
      entity = { constructor: metatype };
    }

    const errors = await this.validate(entity, this.validatorOptions);
    if (errors.length > 0) {
      throw await this.exceptionFactory(errors);
    }

    if (originalValue === undefined && originalEntity === '') {
      // Since SWC requires empty string for validation (to avoid an error),
      // a fallback is needed to revert to the original value (when undefined).
      // @see https://github.com/nestjs/nest/issues/14430
      return originalValue;
    }
    if (isPrimitive) {
      // if the value is a primitive value and the validation process has been successfully completed
      // we have to revert the original value passed through the pipe
      entity = originalEntity;
    }
    if (this.isTransformEnabled) {
      return entity;
    }
    if (isNil) {
      // if the value was originally undefined or null, revert it back
      return originalValue;
    }

    // we check if the number of keys of the "validatorOptions" is higher than 1 (instead of 0)
    // because the "forbidUnknownValues" now fallbacks to "false" (in case it wasn't explicitly specified)
    const shouldTransformToPlain =
      Object.keys(this.validatorOptions).length > 1;
    return shouldTransformToPlain
      ? classTransformer.classToPlain(entity, this.transformOptions)
      : value;
  }
```

---

## 11. Sample 5 · callee #6

- **Function:** `transform`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/pipes/parse-array.pipe.ts`
- **Callee:** `err.getResponse()`
- **Status:** FAILED
- **Error:** No definition found from TypeScript LSP.

### Usage site (matched in test file)

Line 132, col 32 — pattern `anchor_substring`

```typescript
err.getResponse()
```

---

## 12. Sample 5 · callee #9

- **Function:** `transform`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/pipes/parse-array.pipe.ts`
- **Callee:** `Promise.all(value.map(toClassInstance))`
- **Status:** OK

### Usage site (matched in test file)

Line 151, col 23 — pattern `anchor_substring`

```typescript
Promise.all(value.map(toClassInstance))
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

## 13. Sample 5 · callee #10

- **Function:** `transform`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/pipes/parse-array.pipe.ts`
- **Callee:** `isNil(value)`
- **Status:** OK
- **Also seen in:** 4 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 83, col 16 — pattern `anchor_substring`

```typescript
isNil(value)
```

### Resolved definition

- **Path:** `packages/common/utils/shared.utils.ts`
- **Range:** line 47, col 13
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
export const isNil = (val: any): val is null | undefined =>
  isUndefined(val) || val === null;
```

---

## 14. Sample 5 · callee #11

- **Function:** `transform`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/pipes/parse-array.pipe.ts`
- **Callee:** `isString(value)`
- **Status:** OK

### Usage site (matched in test file)

Line 88, col 12 — pattern `anchor_substring`

```typescript
isString(value)
```

### Resolved definition

- **Path:** `packages/common/utils/shared.utils.ts`
- **Range:** line 44, col 13
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
export const isString = (val: any): val is string => typeof val === 'string';
```

---

## 15. Sample 5 · callee #12

- **Function:** `transform`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/pipes/parse-array.pipe.ts`
- **Callee:** `this.options`
- **Status:** OK

### Usage site (matched in test file)

Line 81, col 20 — pattern `anchor_substring`

```typescript
this.options
```

### Resolved definition

- **Path:** `packages/common/pipes/parse-array.pipe.ts`
- **Range:** line 58, col 45
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
constructor(@Optional() protected readonly options: ParseArrayOptions = {}) {
```

---

## 16. Sample 5 · callee #13

- **Function:** `transform`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/pipes/parse-array.pipe.ts`
- **Callee:** `this.validationPipe`
- **Status:** OK

### Usage site (matched in test file)

Line 118, col 16 — pattern `anchor_substring`

```typescript
this.validationPipe
```

### Resolved definition

- **Path:** `packages/common/pipes/parse-array.pipe.ts`
- **Range:** line 55, col 21
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  protected readonly validationPipe: ValidationPipe;
```

---

## 17. Sample 8 · callee #0

- **Function:** `transform`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/pipes/parse-enum.pipe.ts`
- **Callee:** `this.isEnum(value)`
- **Status:** OK

### Usage site (matched in test file)

Line 71, col 10 — pattern `anchor_substring`

```typescript
this.isEnum(value)
```

### Resolved definition

- **Path:** `packages/common/pipes/parse-enum.pipe.ts`
- **Range:** line 78, col 12
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  protected isEnum(value: T): boolean {
    const enumValues = Object.keys(this.enumType as object).map(
      item => this.enumType[item],
    );
    return enumValues.includes(value);
  }
```

---

## 18. Sample 8 · callee #1

- **Function:** `transform`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/pipes/parse-enum.pipe.ts`
- **Callee:** `this.exceptionFactory(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 72, col 18 — pattern `core_fallback`

```typescript
this.exceptionFactory(...)
```

### Resolved definition

- **Path:** `packages/common/pipes/parse-enum.pipe.ts`
- **Range:** line 40, col 12
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  protected exceptionFactory: (error: string) => any;
```

---

## 19. Sample 8 · callee #3

- **Function:** `transform`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/pipes/parse-enum.pipe.ts`
- **Callee:** `this.options`
- **Status:** OK

### Usage site (matched in test file)

Line 68, col 25 — pattern `anchor_substring`

```typescript
this.options
```

### Resolved definition

- **Path:** `packages/common/pipes/parse-enum.pipe.ts`
- **Range:** line 43, col 35
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
@Optional() protected readonly options?: ParseEnumPipeOptions,
```

---

## 20. Sample 9 · callee #0

- **Function:** `transform`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/pipes/parse-float.pipe.ts`
- **Callee:** `this.isNumeric(value)`
- **Status:** OK

### Usage site (matched in test file)

Line 64, col 10 — pattern `anchor_substring`

```typescript
this.isNumeric(value)
```

### Resolved definition

- **Path:** `packages/common/pipes/parse-float.pipe.ts`
- **Range:** line 75, col 12
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
   * @param value currently processed route argument
   * @returns `true` if `value` is a valid float number
   */
  protected isNumeric(value: string): boolean {
    return (
      ['string', 'number'].includes(typeof value) &&
      !isNaN(parseFloat(value)) &&
      isFinite(value as any)
    );
  }
```

---

## 21. Sample 9 · callee #1

- **Function:** `transform`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/pipes/parse-float.pipe.ts`
- **Callee:** `this.exceptionFactory(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 65, col 18 — pattern `core_fallback`

```typescript
this.exceptionFactory(...)
```

### Resolved definition

- **Path:** `packages/common/pipes/parse-float.pipe.ts`
- **Range:** line 40, col 12
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  protected exceptionFactory: (error: string) => any;
```

---

## 22. Sample 9 · callee #3

- **Function:** `transform`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/pipes/parse-float.pipe.ts`
- **Callee:** `parseFloat(value)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 69, col 12 — pattern `anchor_substring`

```typescript
parseFloat(value)
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es5.d.ts`
- **Range:** line 39, col 66

```typescript
/**
 * Converts a string to a floating-point number.
 * @param string A string that contains a floating-point number.
 */
declare function parseFloat(string: string): number;
```

---

## 23. Sample 9 · callee #4

- **Function:** `transform`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/pipes/parse-float.pipe.ts`
- **Callee:** `this.options`
- **Status:** OK

### Usage site (matched in test file)

Line 61, col 25 — pattern `anchor_substring`

```typescript
this.options
```

### Resolved definition

- **Path:** `packages/common/pipes/parse-float.pipe.ts`
- **Range:** line 42, col 45
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
options = options || {};
```

---

## 24. Sample 10 · callee #0

- **Function:** `isNumeric`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/pipes/parse-float.pipe.ts`
- **Callee:** `isNaN(parseFloat(value))`
- **Status:** OK

### Usage site (matched in test file)

Line 79, col 8 — pattern `anchor_substring`

```typescript
isNaN(parseFloat(value))
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es5.d.ts`
- **Range:** line 45, col 52

```typescript
/**
 * Returns a Boolean value that indicates whether a value is the reserved value NaN (not a number).
 * @param number A numeric value.
 */
declare function isNaN(number: number): boolean;
```

---

## 25. Sample 10 · callee #2

- **Function:** `isNumeric`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/pipes/parse-float.pipe.ts`
- **Callee:** `isFinite(value as any)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 80, col 7 — pattern `anchor_substring`

```typescript
isFinite(value as any)
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es5.d.ts`
- **Range:** line 51, col 48

```typescript
/**
 * Determines whether a supplied number is finite.
 * @param number Any numeric value.
 */
declare function isFinite(number: number): boolean;
```

---

## 26. Sample 11 · callee #0

- **Function:** `transform`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/pipes/parse-int.pipe.ts`
- **Callee:** `this.isNumeric(value)`
- **Status:** OK

### Usage site (matched in test file)

Line 68, col 10 — pattern `anchor_substring`

```typescript
this.isNumeric(value)
```

### Resolved definition

- **Path:** `packages/common/pipes/parse-int.pipe.ts`
- **Range:** line 79, col 12
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
   * @param value currently processed route argument
   * @returns `true` if `value` is a valid integer number
   */
  protected isNumeric(value: string): boolean {
    return (
      ['string', 'number'].includes(typeof value) &&
      /^-?\d+$/.test(value) &&
      isFinite(value as any)
    );
  }
```

---

## 27. Sample 11 · callee #1

- **Function:** `transform`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/pipes/parse-int.pipe.ts`
- **Callee:** `this.exceptionFactory(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 69, col 18 — pattern `core_fallback`

```typescript
this.exceptionFactory(...)
```

### Resolved definition

- **Path:** `packages/common/pipes/parse-int.pipe.ts`
- **Range:** line 44, col 12
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  protected exceptionFactory: (error: string) => any;
```

---

## 28. Sample 11 · callee #3

- **Function:** `transform`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/pipes/parse-int.pipe.ts`
- **Callee:** `parseInt(value, 10)`
- **Status:** OK

### Usage site (matched in test file)

Line 73, col 12 — pattern `anchor_substring`

```typescript
parseInt(value, 10)
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

## 29. Sample 11 · callee #4

- **Function:** `transform`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/pipes/parse-int.pipe.ts`
- **Callee:** `this.options`
- **Status:** OK

### Usage site (matched in test file)

Line 65, col 25 — pattern `anchor_substring`

```typescript
this.options
```

### Resolved definition

- **Path:** `packages/common/pipes/parse-int.pipe.ts`
- **Range:** line 46, col 45
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
options = options || {};
```

---

## 30. Sample 13 · callee #0

- **Function:** `setLogLevels`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/services/console-logger.service.ts`
- **Callee:** `this.options`
- **Status:** OK

### Usage site (matched in test file)

Line 277, col 10 — pattern `anchor_substring`

```typescript
this.options
```

### Resolved definition

- **Path:** `packages/common/services/console-logger.service.ts`
- **Range:** line 119, col 12
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
   * The options of the logger.
   */
  protected options: ConsoleLoggerOptions;
```

---

## 31. Sample 14 · callee #0

- **Function:** `setContext`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/services/console-logger.service.ts`
- **Callee:** `this.context`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 288, col 5 — pattern `anchor_substring`

```typescript
this.context
```

### Resolved definition

- **Path:** `packages/common/services/console-logger.service.ts`
- **Range:** line 123, col 12
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
   * The context of the logger (can be set manually or automatically inferred).
   */
  protected context?: string;
```

---

## 32. Sample 15 · callee #1

- **Function:** `resetContext`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/services/console-logger.service.ts`
- **Callee:** `this.originalContext`
- **Status:** OK

### Usage site (matched in test file)

Line 295, col 20 — pattern `anchor_substring`

```typescript
this.originalContext
```

### Resolved definition

- **Path:** `packages/common/services/console-logger.service.ts`
- **Range:** line 127, col 12
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
   * The original context of the logger (set in the constructor).
   */
  protected originalContext?: string;
```

---

## 33. Sample 16 · callee #0

- **Function:** `flush`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/services/logger.service.ts`
- **Callee:** `this.logBuffer.forEach(...)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 286, col 20 — pattern `core_fallback`

```typescript
this.logBuffer.forEach(...)
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

## 34. Sample 16 · callee #1

- **Function:** `flush`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/services/logger.service.ts`
- **Callee:** `item.methodRef(...(item.arguments as [string]))`
- **Status:** OK

### Usage site (matched in test file)

Line 287, col 7 — pattern `anchor_substring`

```typescript
item.methodRef(...(item.arguments as [string]))
```

### Resolved definition

- **Path:** `packages/common/services/logger.service.ts`
- **Range:** line 64, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
   * Method to execute.
   */
  methodRef: Function;
```

---

## 35. Sample 16 · callee #2

- **Function:** `flush`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/services/logger.service.ts`
- **Callee:** `this.isBufferAttached`
- **Status:** OK
- **Also seen in:** 2 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 285, col 5 — pattern `anchor_substring`

```typescript
this.isBufferAttached
```

### Resolved definition

- **Path:** `packages/common/services/logger.service.ts`
- **Range:** line 91, col 17
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  private static isBufferAttached: boolean;
```

---

## 36. Sample 16 · callee #3

- **Function:** `flush`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/services/logger.service.ts`
- **Callee:** `this.logBuffer`
- **Status:** OK

### Usage site (matched in test file)

Line 286, col 5 — pattern `anchor_substring`

```typescript
this.logBuffer
```

### Resolved definition

- **Path:** `packages/common/services/logger.service.ts`
- **Range:** line 87, col 46

```typescript
protected static logBuffer = new Array<LogBufferRecord>();
```

---

## 37. Sample 16 · callee #4

- **Function:** `flush`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/common/services/logger.service.ts`
- **Callee:** `item.arguments`
- **Status:** OK

### Usage site (matched in test file)

Line 287, col 26 — pattern `anchor_substring`

```typescript
item.arguments
```

### Resolved definition

- **Path:** `packages/common/services/logger.service.ts`
- **Range:** line 69, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
   * Arguments to pass to the method.
   */
  arguments: unknown[];
```

---

## 38. Sample 19 · callee #0

- **Function:** `createDecorator`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/discovery/discovery-service.ts`
- **Callee:** `DiscoverableMetaHostCollection.addClassMetaHostLink(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 65, col 42 — pattern `core_fallback`

```typescript
DiscoverableMetaHostCollection.addClassMetaHostLink(...)
```

### Resolved definition

- **Path:** `packages/core/discovery/discoverable-meta-host-collection.ts`
- **Range:** line 33, col 16
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
   * Adds a link between a class reference and a metadata key.
   * @param target The class reference.
   * @param metadataKey The metadata key.
   */
  public static addClassMetaHostLink(
    target: Type | Function,
    metadataKey: string,
  ) {
    this.metaHostLinks.set(target, metadataKey);
  }
```

---

## 39. Sample 19 · callee #1

- **Function:** `createDecorator`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/discovery/discovery-service.ts`
- **Callee:** `uid(21)`
- **Status:** OK

### Usage site (matched in test file)

Line 60, col 25 — pattern `anchor_substring`

```typescript
uid(21)
```

### Resolved definition

- **Path:** `node_modules/uid/dist/index.js`
- **Range:** line 3, col 9
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
function uid(len) {
	var i=0, tmp=(len || 11);
	if (!BUFFER || ((IDX + tmp) > SIZE*2)) {
		for (BUFFER='',IDX=0; i < SIZE; i++) {
			BUFFER += HEX[Math.random() * 256 | 0];
		}
	}

	return BUFFER.substring(IDX, IDX++ + tmp);
}
```

---

## 40. Sample 19 · callee #2

- **Function:** `createDecorator`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/discovery/discovery-service.ts`
- **Callee:** `SetMetadata(metadataKey, opts ?? {})`
- **Status:** OK

### Usage site (matched in test file)

Line 70, col 9 — pattern `anchor_substring`

```typescript
SetMetadata(metadataKey, opts ?? {})
```

### Resolved definition

- **Path:** `packages/common/decorators/core/set-metadata.decorator.ts`
- **Range:** line 21, col 13
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
 * Decorator that assigns metadata to the class/function using the
 * specified `key`.
 *
 * Requires two parameters:
 * - `key` - a value defining the key under which the metadata is stored
 * - `value` - metadata to be associated with `key`
 *
 * This metadata can be reflected using the `Reflector` class.
 *
 * Example: `@SetMetadata('roles', ['admin'])`
 *
 * @see [Reflection](https://docs.nestjs.com/fundamentals/execution-context#reflection-and-metadata)
 *
 * @publicApi
 */
export const SetMetadata = <K = string, V = any>(
  metadataKey: K,
  metadataValue: V,
): CustomDecorator<K> => {
  const decoratorFactory = (target: object, key?: any, descriptor?: any) => {
    if (descriptor) {
      Reflect.defineMetadata(metadataKey, metadataValue, descriptor.value);
      return descriptor;
    }
    Reflect.defineMetadata(metadataKey, metadataValue, target);
    return target;
  };
  decoratorFactory.KEY = metadataKey;
  return decoratorFactory;
};
```

---

## 41. Sample 20 · callee #0

- **Function:** `getModules`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/discovery/discovery-service.ts`
- **Callee:** `this.modulesContainer.values()`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 154, col 30 — pattern `anchor_substring`

```typescript
this.modulesContainer.values()
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es2015.iterable.d.ts`
- **Range:** line 150, col 27

```typescript
/**
     * Returns an iterable of values in the map
     */
    values(): MapIterator<V>;
```

---

## 42. Sample 20 · callee #1

- **Function:** `getModules`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/discovery/discovery-service.ts`
- **Callee:** `this.includeWhitelisted(options.include!)`
- **Status:** OK

### Usage site (matched in test file)

Line 157, col 25 — pattern `anchor_substring`

```typescript
this.includeWhitelisted(options.include!)
```

### Resolved definition

- **Path:** `packages/core/discovery/discovery-service.ts`
- **Range:** line 160, col 10
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  private includeWhitelisted(include: Function[]): Module[] {
    const moduleRefs = [...this.modulesContainer.values()];
    return moduleRefs.filter(({ metatype }) =>
      include.some(item => item === metatype),
    );
  }
```

---

## 43. Sample 20 · callee #2

- **Function:** `getModules`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/discovery/discovery-service.ts`
- **Callee:** `this.modulesContainer`
- **Status:** OK

### Usage site (matched in test file)

Line 154, col 30 — pattern `anchor_substring`

```typescript
this.modulesContainer
```

### Resolved definition

- **Path:** `packages/core/discovery/discovery-service.ts`
- **Range:** line 50, col 31
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  constructor(private readonly modulesContainer: ModulesContainer) {}
```

---

## 44. Sample 22 · callee #0

- **Function:** `create`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/helpers/context-id-factory.ts`
- **Callee:** `createContextId()`
- **Status:** OK

### Usage site (matched in test file)

Line 50, col 12 — pattern `anchor_substring`

```typescript
createContextId()
```

### Resolved definition

- **Path:** `packages/core/helpers/context-id-factory.ts`
- **Range:** line 4, col 16
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
export function createContextId(): ContextId {
  /**
   * We are generating random identifier to track asynchronous
   * execution context. An identifier does not have to be neither unique
   * nor unpredictable because WeakMap uses objects as keys (reference comparison).
   * Thus, even though identifier number might be equal, WeakMap would properly
   * associate asynchronous context with its internal map values using object reference.
   * Object is automatically removed once request has been processed (closure).
   */
  return { id: Math.random() };
}
```

---

## 45. Sample 23 · callee #0

- **Function:** `apply`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/helpers/context-id-factory.ts`
- **Callee:** `this.strategy`
- **Status:** OK

### Usage site (matched in test file)

Line 92, col 5 — pattern `anchor_substring`

```typescript
this.strategy
```

### Resolved definition

- **Path:** `packages/core/helpers/context-id-factory.ts`
- **Range:** line 43, col 17
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  private static strategy?: ContextIdStrategy;
```

---

## 46. Sample 24 · callee #0

- **Function:** `httpAdapter`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/helpers/http-adapter-host.ts`
- **Callee:** `this._httpAdapter`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 29, col 5 — pattern `anchor_substring`

```typescript
this._httpAdapter
```

### Resolved definition

- **Path:** `packages/core/helpers/http-adapter-host.ts`
- **Range:** line 18, col 10
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  private _httpAdapter?: T;
```

---

## 47. Sample 26 · callee #0

- **Function:** `?`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/helpers/http-adapter-host.ts`
- **Callee:** ``
- **Status:** FAILED
- **Error:** could not extract tested_function

---

## 48. Sample 27 · callee #0

- **Function:** `listening`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/helpers/http-adapter-host.ts`
- **Callee:** `this._listen$.next()`
- **Status:** OK

### Usage site (matched in test file)

Line 57, col 7 — pattern `anchor_substring`

```typescript
this._listen$.next()
```

### Resolved definition

- **Path:** `node_modules/rxjs/src/internal/Subject.ts`
- **Range:** line 58, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  next(value: T) {
    errorContext(() => {
      this._throwIfClosed();
      if (!this.isStopped) {
        if (!this.currentObservers) {
          this.currentObservers = Array.from(this.observers);
        }
        for (const observer of this.currentObservers) {
          observer.next(value);
        }
      }
    });
  }
```

---

## 49. Sample 27 · callee #1

- **Function:** `listening`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/helpers/http-adapter-host.ts`
- **Callee:** `this._listen$.complete()`
- **Status:** OK

### Usage site (matched in test file)

Line 58, col 7 — pattern `anchor_substring`

```typescript
this._listen$.complete()
```

### Resolved definition

- **Path:** `node_modules/rxjs/src/internal/Subject.ts`
- **Range:** line 86, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  complete() {
    errorContext(() => {
      this._throwIfClosed();
      if (!this.isStopped) {
        this.isStopped = true;
        const { observers } = this;
        while (observers.length) {
          observers.shift()!.complete();
        }
      }
    });
  }
```

---

## 50. Sample 27 · callee #2

- **Function:** `listening`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/helpers/http-adapter-host.ts`
- **Callee:** `this.isListening`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 54, col 5 — pattern `anchor_substring`

```typescript
this.isListening
```

### Resolved definition

- **Path:** `packages/core/helpers/http-adapter-host.ts`
- **Range:** line 19, col 41

```typescript
private isListening = false;
```

---

## 51. Sample 27 · callee #3

- **Function:** `listening`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/helpers/http-adapter-host.ts`
- **Callee:** `this._listen$`
- **Status:** OK

### Usage site (matched in test file)

Line 57, col 7 — pattern `anchor_substring`

```typescript
this._listen$
```

### Resolved definition

- **Path:** `packages/core/helpers/http-adapter-host.ts`
- **Range:** line 18, col 27

```typescript
private _listen$ = new Subject<void>();
```

---

## 52. Sample 29 · callee #0

- **Function:** `callOperator`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/hooks/on-module-destroy.hook.ts`
- **Callee:** `iterate(instances)`
- **Status:** OK
- **Also seen in:** 2 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 26, col 10 — pattern `anchor_substring`

```typescript
iterate(instances)
```

### Resolved definition

- **Path:** `node_modules/iterare/lib/iterate.js`
- **Range:** line 207, col 9
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
 * Creates an Iterator with advanced chainable operator methods for any Iterable or Iterator
 */
function iterate(collection) {
    return new IteratorWithOperators(utils_1.toIterator(collection));
}
```

---

## 53. Sample 30 · callee #0

- **Function:** `hasOnModuleInitHook`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/hooks/on-module-init.hook.ts`
- **Callee:** `isFunction((instance as OnModuleInit).onModuleInit)`
- **Status:** OK

### Usage site (matched in test file)

Line 17, col 10 — pattern `anchor_substring`

```typescript
isFunction((instance as OnModuleInit).onModuleInit)
```

### Resolved definition

- **Path:** `packages/common/utils/shared.utils.ts`
- **Range:** line 42, col 13
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
export const isFunction = (val: any): val is Function =>
  typeof val === 'function';
```

---

## 54. Sample 31 · callee #0

- **Function:** `isOptionalFactoryDependency`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/injector/injector.ts`
- **Callee:** `isUndefined((value as OptionalFactoryDependency).token)`
- **Status:** OK
- **Also seen in:** 2 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 360, col 10 — pattern `anchor_substring`

```typescript
isUndefined((value as OptionalFactoryDependency).token)
```

### Resolved definition

- **Path:** `packages/common/utils/shared.utils.ts`
- **Range:** line 0, col 13
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
export const isUndefined = (obj: any): obj is undefined =>
  typeof obj === 'undefined';
```

---

## 55. Sample 32 · callee #0

- **Function:** `complete`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/injector/settlement-signal.ts`
- **Callee:** `this.settleFn()`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 23, col 5 — pattern `anchor_substring`

```typescript
this.settleFn()
```

### Resolved definition

- **Path:** `packages/core/injector/settlement-signal.ts`
- **Range:** line 7, col 52

```typescript
  private readonly settledPromise: Promise<unknown>;
  private settleFn!: (err?: unknown) => void;
```

---

## 56. Sample 32 · callee #1

- **Function:** `complete`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/injector/settlement-signal.ts`
- **Callee:** `this.completed`
- **Status:** OK
- **Also seen in:** 2 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 22, col 5 — pattern `anchor_substring`

```typescript
this.completed
```

### Resolved definition

- **Path:** `packages/core/injector/settlement-signal.ts`
- **Range:** line 8, col 45

```typescript
private completed = false;
```

---

## 57. Sample 34 · callee #0

- **Function:** `asPromise`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/injector/settlement-signal.ts`
- **Callee:** `this.settledPromise`
- **Status:** OK

### Usage site (matched in test file)

Line 40, col 12 — pattern `anchor_substring`

```typescript
this.settledPromise
```

### Resolved definition

- **Path:** `packages/core/injector/settlement-signal.ts`
- **Range:** line 7, col 19
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  private readonly settledPromise: Promise<unknown>;
```

---

## 58. Sample 35 · callee #0

- **Function:** `insertRef`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/injector/settlement-signal.ts`
- **Callee:** `this._refs.add(wrapperId)`
- **Status:** OK

### Usage site (matched in test file)

Line 48, col 5 — pattern `anchor_substring`

```typescript
this._refs.add(wrapperId)
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

## 59. Sample 35 · callee #1

- **Function:** `insertRef`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/injector/settlement-signal.ts`
- **Callee:** `this._refs`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 48, col 5 — pattern `anchor_substring`

```typescript
this._refs
```

### Resolved definition

- **Path:** `packages/core/injector/settlement-signal.ts`
- **Range:** line 5, col 31

```typescript
private readonly _refs = new Set();
```

---

## 60. Sample 36 · callee #0

- **Function:** `isCycle`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/injector/settlement-signal.ts`
- **Callee:** `this._refs.has(wrapperId)`
- **Status:** OK

### Usage site (matched in test file)

Line 57, col 31 — pattern `anchor_substring`

```typescript
this._refs.has(wrapperId)
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es2015.collection.d.ts`
- **Range:** line 106, col 89

```typescript
/**
     * @returns a boolean indicating whether an element with the specified value exists in the Set or not.
     */
    has(value: T): boolean;
```

---

## 61. Sample 37 · callee #0

- **Function:** `registerRequestByContextId`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/nest-application-context.ts`
- **Callee:** `this.container.registerRequestProvider(request, contextId)`
- **Status:** OK

### Usage site (matched in test file)

Line 243, col 5 — pattern `anchor_substring`

```typescript
this.container.registerRequestProvider(request, contextId)
```

### Resolved definition

- **Path:** `packages/core/injector/container.ts`
- **Range:** line 351, col 9
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  public registerRequestProvider<T = any>(request: T, contextId: ContextId) {
    const wrapper = this.internalCoreModule.getProviderByKey(REQUEST);
    wrapper.setInstanceByContextId(contextId, {
      instance: request,
      isResolved: true,
    });
  }
```

---

## 62. Sample 37 · callee #1

- **Function:** `registerRequestByContextId`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/nest-application-context.ts`
- **Callee:** `this.container`
- **Status:** OK

### Usage site (matched in test file)

Line 243, col 5 — pattern `anchor_substring`

```typescript
this.container
```

### Resolved definition

- **Path:** `packages/core/nest-application-context.ts`
- **Range:** line 67, col 23
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
protected readonly container: NestContainer,
```

---

## 63. Sample 38 · callee #0

- **Function:** `init`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/nest-application-context.ts`
- **Callee:** `this.callInitHook()`
- **Status:** OK

### Usage site (matched in test file)

Line 259, col 15 — pattern `anchor_substring`

```typescript
this.callInitHook()
```

### Resolved definition

- **Path:** `packages/core/nest-application-context.ts`
- **Range:** line 398, col 3

```typescript
/**
   * Calls the `onModuleInit` function on the registered
   * modules and its children.
   */
  protected async callInitHook(): Promise<void> {
    const modulesSortedByDistance = this.getModulesToTriggerHooksOn();
    for (const module of modulesSortedByDistance) {
      await callModuleInitHook(module);
    }
  }
```

---

## 64. Sample 38 · callee #1

- **Function:** `init`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/nest-application-context.ts`
- **Callee:** `this.callBootstrapHook()`
- **Status:** OK

### Usage site (matched in test file)

Line 260, col 15 — pattern `anchor_substring`

```typescript
this.callBootstrapHook()
```

### Resolved definition

- **Path:** `packages/core/nest-application-context.ts`
- **Range:** line 423, col 3

```typescript
/**
   * Calls the `onApplicationBootstrap` function on the registered
   * modules and its children.
   */
  protected async callBootstrapHook(): Promise<void> {
    const modulesSortedByDistance = this.getModulesToTriggerHooksOn();
    for (const module of modulesSortedByDistance) {
      await callModuleBootstrapHook(module);
    }
  }
```

---

## 65. Sample 38 · callee #2

- **Function:** `init`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/nest-application-context.ts`
- **Callee:** `Promise(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 257, col 38 — pattern `core_fallback`

```typescript
Promise(...)
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es5.d.ts`
- **Range:** line 1542, col 1

```typescript
/**
 * Represents the completion of an asynchronous operation
 */
interface Promise<T> {
    /**
     * Attaches callbacks for the resolution and/or rejection of the Promise.
     * @param onfulfilled The callback to execute when the Promise is resolved.
     * @param onrejected The callback to execute when the Promise is rejected.
     * @returns A Promise for the completion of which ever callback is executed.
     */
    then<TResult1 = T, TResult2 = never>(onfulfilled?: ((value: T) => TResult1 | PromiseLike<TResult1>) | undefined | null, onrejected?: ((reason: any) => TResult2 | PromiseLike<TResult2>) | undefined | null): Promise<TResult1 | TResult2>;

    /**
     * Attaches a callback for only the rejection of the Promise.
     * @param onrejected The callback to execute when the Promise is rejected.
     * @returns A Promise for the completion of the callback.
     */
    catch<TResult = never>(onrejected?: ((reason: any) => TResult | PromiseLike<TResult>) | undefined | null): Promise<T | TResult>;
}
```

---

## 66. Sample 38 · callee #3

- **Function:** `init`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/nest-application-context.ts`
- **Callee:** `this.isInitialized`
- **Status:** OK

### Usage site (matched in test file)

Line 253, col 9 — pattern `anchor_substring`

```typescript
this.isInitialized
```

### Resolved definition

- **Path:** `packages/core/nest-application-context.ts`
- **Range:** line 44, col 1

```typescript
protected isInitialized = false;
```

---

## 67. Sample 38 · callee #4

- **Function:** `init`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/nest-application-context.ts`
- **Callee:** `this.initializationPromise`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 257, col 5 — pattern `anchor_substring`

```typescript
this.initializationPromise
```

### Resolved definition

- **Path:** `packages/core/nest-application-context.ts`
- **Range:** line 57, col 10
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  private initializationPromise?: Promise<void>;
```

---

## 68. Sample 39 · callee #0

- **Function:** `close`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/nest-application-context.ts`
- **Callee:** `this.callDestroyHook()`
- **Status:** OK

### Usage site (matched in test file)

Line 278, col 11 — pattern `anchor_substring`

```typescript
this.callDestroyHook()
```

### Resolved definition

- **Path:** `packages/core/nest-application-context.ts`
- **Range:** line 409, col 3

```typescript
/**
   * Calls the `onModuleDestroy` function on the registered
   * modules and its children.
   */
  protected async callDestroyHook(): Promise<void> {
    const modulesSortedByDistance = [
      ...this.getModulesToTriggerHooksOn(),
    ].reverse();

    for (const module of modulesSortedByDistance) {
      await callModuleDestroyHook(module);
    }
  }
```

---

## 69. Sample 39 · callee #1

- **Function:** `close`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/nest-application-context.ts`
- **Callee:** `this.callBeforeShutdownHook(signal)`
- **Status:** OK

### Usage site (matched in test file)

Line 279, col 11 — pattern `anchor_substring`

```typescript
this.callBeforeShutdownHook(signal)
```

### Resolved definition

- **Path:** `packages/core/nest-application-context.ts`
- **Range:** line 448, col 3

```typescript
/**
   * Calls the `beforeApplicationShutdown` function on the registered
   * modules and children.
   */
  protected async callBeforeShutdownHook(signal?: string): Promise<void> {
    const modulesSortedByDistance = [
      ...this.getModulesToTriggerHooksOn(),
    ].reverse();

    for (const module of modulesSortedByDistance) {
      await callBeforeAppShutdownHook(module, signal);
    }
  }
```

---

## 70. Sample 39 · callee #2

- **Function:** `close`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/nest-application-context.ts`
- **Callee:** `this.dispose()`
- **Status:** OK

### Usage site (matched in test file)

Line 280, col 11 — pattern `anchor_substring`

```typescript
this.dispose()
```

### Resolved definition

- **Path:** `packages/core/nest-application-context.ts`
- **Range:** line 340, col 3

```typescript
  protected async dispose(): Promise<void> {
    // Nest application context has no server
    // to dispose, therefore just call a noop
    return Promise.resolve();
  }
```

---

## 71. Sample 39 · callee #3

- **Function:** `close`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/nest-application-context.ts`
- **Callee:** `this.callShutdownHook(signal)`
- **Status:** OK

### Usage site (matched in test file)

Line 281, col 11 — pattern `anchor_substring`

```typescript
this.callShutdownHook(signal)
```

### Resolved definition

- **Path:** `packages/core/nest-application-context.ts`
- **Range:** line 434, col 3

```typescript
/**
   * Calls the `onApplicationShutdown` function on the registered
   * modules and children.
   */
  protected async callShutdownHook(signal?: string): Promise<void> {
    const modulesSortedByDistance = [
      ...this.getModulesToTriggerHooksOn(),
    ].reverse();

    for (const module of modulesSortedByDistance) {
      await callAppShutdownHook(module, signal);
    }
  }
```

---

## 72. Sample 39 · callee #4

- **Function:** `close`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/nest-application-context.ts`
- **Callee:** `this.unsubscribeFromProcessSignals()`
- **Status:** OK

### Usage site (matched in test file)

Line 282, col 5 — pattern `anchor_substring`

```typescript
this.unsubscribeFromProcessSignals()
```

### Resolved definition

- **Path:** `packages/core/nest-application-context.ts`
- **Range:** line 391, col 12
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
   * Unsubscribes from shutdown signals (process events)
   */
  protected unsubscribeFromProcessSignals() {
    if (!this.shutdownCleanupRef) {
      return;
    }
    this.activeShutdownSignals.forEach(signal => {
      process.removeListener(signal, this.shutdownCleanupRef!);
    });
  }
```

---

## 73. Sample 40 · callee #0

- **Function:** `useLogger`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/nest-application-context.ts`
- **Callee:** `Logger.overrideLogger(logger)`
- **Status:** OK

### Usage site (matched in test file)

Line 291, col 5 — pattern `anchor_substring`

```typescript
Logger.overrideLogger(logger)
```

### Resolved definition

- **Path:** `packages/common/services/logger.service.ts`
- **Range:** line 311, col 9
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  static overrideLogger(logger: LoggerService | LogLevel[] | boolean) {
    if (Array.isArray(logger)) {
      Logger.logLevels = logger;
      return this.staticInstanceRef?.setLogLevels?.(logger);
    }
    if (isObject(logger)) {
      if (logger instanceof Logger && logger.constructor !== Logger) {
        const errorMessage = `Using the "extends Logger" instruction is not allowed in Nest v9. Please, use "extends ConsoleLogger" instead.`;
        this.staticInstanceRef?.error(errorMessage);
        throw new Error(errorMessage);
      }
      this.staticInstanceRef = logger as LoggerService;
    } else {
      this.staticInstanceRef = undefined;
    }
  }
```

---

## 74. Sample 40 · callee #1

- **Function:** `useLogger`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/nest-application-context.ts`
- **Callee:** `this.flushLogs()`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 294, col 7 — pattern `anchor_substring`

```typescript
this.flushLogs()
```

### Resolved definition

- **Path:** `packages/core/nest-application-context.ts`
- **Range:** line 301, col 9
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
   * Prints buffered logs and detaches buffer.
   * @returns {void}
   */
  public flushLogs() {
    Logger.flush();
  }
```

---

## 75. Sample 40 · callee #2

- **Function:** `useLogger`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/nest-application-context.ts`
- **Callee:** `this.shouldFlushLogsOnOverride`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 293, col 9 — pattern `anchor_substring`

```typescript
this.shouldFlushLogsOnOverride
```

### Resolved definition

- **Path:** `packages/core/nest-application-context.ts`
- **Range:** line 49, col 5

```typescript
private shouldFlushLogsOnOverride = false;
```

---

## 76. Sample 41 · callee #0

- **Function:** `flushLogs`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/nest-application-context.ts`
- **Callee:** `Logger.flush()`
- **Status:** OK

### Usage site (matched in test file)

Line 303, col 5 — pattern `anchor_substring`

```typescript
Logger.flush()
```

### Resolved definition

- **Path:** `packages/common/services/logger.service.ts`
- **Range:** line 283, col 9
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
   * Print buffered logs and detach buffer.
   */
  static flush() {
    this.isBufferAttached = false;
    this.logBuffer.forEach(item =>
      item.methodRef(...(item.arguments as [string])),
    );
    this.logBuffer = [];
  }
```

---

## 77. Sample 43 · callee #0

- **Function:** `enableShutdownHooks`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/nest-application-context.ts`
- **Callee:** `Object.keys(ShutdownSignal)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 324, col 17 — pattern `anchor_substring`

```typescript
Object.keys(ShutdownSignal)
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es5.d.ts`
- **Range:** line 255, col 34

```typescript
/**
     * Returns the names of the enumerable string properties and methods of an object.
     * @param o Object that contains the properties and methods. This can be an object that you created or an existing Document Object Model (DOM) object.
     */
    keys(o: object): string[];
```

---

## 78. Sample 43 · callee #1

- **Function:** `enableShutdownHooks`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/nest-application-context.ts`
- **Callee:** `isEmpty(signals)`
- **Status:** OK

### Usage site (matched in test file)

Line 323, col 9 — pattern `anchor_substring`

```typescript
isEmpty(signals)
```

### Resolved definition

- **Path:** `packages/common/utils/shared.utils.ts`
- **Range:** line 49, col 13
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
export const isEmpty = (array: any): boolean => !(array && array.length > 0);
```

---

## 79. Sample 45 · callee #1

- **Function:** `unsubscribeFromProcessSignals`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/nest-application-context.ts`
- **Callee:** `process.removeListener(signal, this.shutdownCleanupRef!)`
- **Status:** OK

### Usage site (matched in test file)

Line 397, col 7 — pattern `anchor_substring`

```typescript
process.removeListener(signal, this.shutdownCleanupRef!)
```

### Resolved definition

- **Path:** `node_modules/@types/node/events.d.ts`
- **Range:** line 741, col 16
- **Selection:** `fast_path_refined_via_document_symbols`

```typescript
/**
                 * Removes the specified `listener` from the listener array for the event named `eventName`.
                 *
                 * ```js
                 * const callback = (stream) => {
                 *   console.log('someone connected!');
                 * };
                 * server.on('connection', callback);
                 * // ...
                 * server.removeListener('connection', callback);
                 * ```
                 *
                 * `removeListener()` will remove, at most, one instance of a listener from the
                 * listener array. If any single listener has been added multiple times to the
                 * listener array for the specified `eventName`, then `removeListener()` must be
                 * called multiple times to remove each instance.
                 *
                 * Once an event is emitted, all listeners attached to it at the
                 * time of emitting are called in order. This implies that any `removeListener()` or `removeAllListeners()` calls _after_ emitting and _before_ the last listener finishes execution
                 * will not remove them from`emit()` in progress. Subsequent events behave as expected.
                 *
                 * ```js
                 * import { EventEmitter } from 'node:events';
                 * class MyEmitter extends EventEmitter {}
                 * const myEmitter = new MyEmitter();
                 *
                 * const callbackA = () => {
                 *   console.log('A');
                 *   myEmitter.removeListener('event', callbackB);
                 * };
                 *
                 * const callbackB = () => {
                 *   console.log('B');
                 * };
                 *
                 * myEmitter.on('event', callbackA);
                 *
                 * myEmitter.on('event', callbackB);
                 *
                 * // callbackA removes listener callbackB but it will still be called.
                 * // Internal listener array at time of emit [callbackA, callbackB]
                 * myEmitter.emit('event');
                 * // Prints:
                 * //   A
                 * //   B
                 *
                 * // callbackB is now removed.
                 * // Internal listener array [callbackA]
                 * myEmitter.emit('event');
                 * // Prints:
                 * //   A
                 * ```
                 *
                 * Because listeners are managed using an internal array, calling this will
                 * change the position indices of any listener registered _after_ the listener
                 * being removed. This will not impact the order in which listeners are called,
                 * but it means that any copies of the listener array as returned by
                 * the `emitter.listeners()` method will need to be recreated.
                 *
                 * When a single function has been added as a handler multiple times for a single
                 * event (as in the example below), `removeListener()` will remove the most
                 * recently added instance. In the example the `once('ping')` listener is removed:
                 *
                 * ```js
                 * import { EventEmitter } from 'node:events';
                 * const ee = new EventEmitter();
                 *
                 * function pong() {
                 *   console.log('pong');
                 * }
                 *
                 * ee.on('ping', pong);
                 * ee.once('ping', pong);
                 * ee.removeListener('ping', pong);
                 *
                 * ee.emit('ping');
                 * ee.emit('ping');
                 * ```
                 *
                 * Returns a reference to the `EventEmitter`, so that calls can be chained.
                 * @since v0.1.26
                 */
                removeListener<K>(eventName: Key<K, T>, listener: Listener1<K, T>): this;
```

---

## 80. Sample 45 · callee #2

- **Function:** `unsubscribeFromProcessSignals`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/nest-application-context.ts`
- **Callee:** `this.shutdownCleanupRef`
- **Status:** OK

### Usage site (matched in test file)

Line 393, col 10 — pattern `anchor_substring`

```typescript
this.shutdownCleanupRef
```

### Resolved definition

- **Path:** `packages/core/nest-application-context.ts`
- **Range:** line 54, col 10
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  private shutdownCleanupRef?: (...args: unknown[]) => unknown;
```

---

## 81. Sample 45 · callee #3

- **Function:** `unsubscribeFromProcessSignals`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/nest-application-context.ts`
- **Callee:** `this.activeShutdownSignals`
- **Status:** OK

### Usage site (matched in test file)

Line 396, col 5 — pattern `anchor_substring`

```typescript
this.activeShutdownSignals
```

### Resolved definition

- **Path:** `packages/core/nest-application-context.ts`
- **Range:** line 51, col 44

```typescript
private readonly activeShutdownSignals = new Array<string>();
```

---

## 82. Sample 46 · callee #0

- **Function:** `callInitHook`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/nest-application-context.ts`
- **Callee:** `this.getModulesToTriggerHooksOn()`
- **Status:** OK
- **Also seen in:** 4 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 406, col 37 — pattern `anchor_substring`

```typescript
this.getModulesToTriggerHooksOn()
```

### Resolved definition

- **Path:** `packages/core/nest-application-context.ts`
- **Range:** line 472, col 10
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  private getModulesToTriggerHooksOn(): Module[] {
    if (this._moduleRefsForHooksByDistance) {
      return this._moduleRefsForHooksByDistance;
    }
    const modulesContainer = this.container.getModules();
    const compareFn = (a: Module, b: Module) => b.distance - a.distance;
    const modulesSortedByDistance = Array.from(modulesContainer.values()).sort(
      compareFn,
    );

    this._moduleRefsForHooksByDistance = this.appOptions?.preview
      ? modulesSortedByDistance.filter(moduleRef => moduleRef.initOnPreview)
      : modulesSortedByDistance;
    return this._moduleRefsForHooksByDistance;
  }
```

---

## 83. Sample 46 · callee #1

- **Function:** `callInitHook`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/nest-application-context.ts`
- **Callee:** `callModuleInitHook(module)`
- **Status:** OK

### Usage site (matched in test file)

Line 408, col 13 — pattern `anchor_substring`

```typescript
callModuleInitHook(module)
```

### Resolved definition

- **Path:** `packages/core/hooks/on-module-init.hook.ts`
- **Range:** line 36, col 22
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
 * Calls the `onModuleInit` function on the module and its children
 * (providers / controllers).
 *
 * @param module The module which will be initialized
 */
export async function callModuleInitHook(module: Module): Promise<void> {
  const providers = module.getNonAliasProviders();
  // Module (class) instance is the first element of the providers array
  // Lifecycle hook has to be called once all classes are properly initialized
  const [_, moduleClassHost] = providers.shift()!;
  const instances = [
    ...module.controllers,
    ...providers,
    ...module.injectables,
    ...module.middlewares,
  ];

  const nonTransientInstances = getNonTransientInstances(instances);
  await Promise.all(callOperator(nonTransientInstances));

  const transientInstances = getTransientInstances(instances);
  await Promise.all(callOperator(transientInstances));

  // Call the instance itself
  const moduleClassInstance = moduleClassHost.instance;
  if (
    moduleClassInstance &&
    hasOnModuleInitHook(moduleClassInstance) &&
    moduleClassHost.isDependencyTreeStatic()
  ) {
    await moduleClassInstance.onModuleInit();
  }
}
```

---

## 84. Sample 47 · callee #1

- **Function:** `callDestroyHook`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/nest-application-context.ts`
- **Callee:** `callModuleDestroyHook(module)`
- **Status:** OK

### Usage site (matched in test file)

Line 422, col 13 — pattern `anchor_substring`

```typescript
callModuleDestroyHook(module)
```

### Resolved definition

- **Path:** `packages/core/hooks/on-module-destroy.hook.ts`
- **Range:** line 40, col 22
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
 * Calls the `onModuleDestroy` function on the module and its children
 * (providers / controllers).
 *
 * @param module The module which will be initialized
 */
export async function callModuleDestroyHook(module: Module): Promise<any> {
  const providers = module.getNonAliasProviders();
  // Module (class) instance is the first element of the providers array
  // Lifecycle hook has to be called once all classes are properly destroyed
  const [_, moduleClassHost] = providers.shift()!;
  const instances = [
    ...module.controllers,
    ...providers,
    ...module.injectables,
    ...module.middlewares,
  ];

  const nonTransientInstances = getNonTransientInstances(instances);
  await Promise.all(callOperator(nonTransientInstances));

  const transientInstances = getTransientInstances(instances);
  await Promise.all(callOperator(transientInstances));

  // Call the module instance itself
  const moduleClassInstance = moduleClassHost.instance;
  if (
    moduleClassInstance &&
    hasOnModuleDestroyHook(moduleClassInstance) &&
    moduleClassHost.isDependencyTreeStatic()
  ) {
    await moduleClassInstance.onModuleDestroy();
  }
}
```

---

## 85. Sample 48 · callee #1

- **Function:** `callBootstrapHook`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/nest-application-context.ts`
- **Callee:** `callModuleBootstrapHook(module)`
- **Status:** OK

### Usage site (matched in test file)

Line 433, col 13 — pattern `anchor_substring`

```typescript
callModuleBootstrapHook(module)
```

### Resolved definition

- **Path:** `packages/core/hooks/on-app-bootstrap.hook.ts`
- **Range:** line 42, col 22
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
 * Calls the `onApplicationBootstrap` function on the module and its children
 * (providers / controllers).
 *
 * @param module The module which will be initialized
 */
export async function callModuleBootstrapHook(module: Module): Promise<any> {
  const providers = module.getNonAliasProviders();
  // Module (class) instance is the first element of the providers array
  // Lifecycle hook has to be called once all classes are properly initialized
  const [_, moduleClassHost] = providers.shift()!;
  const instances = [
    ...module.controllers,
    ...providers,
    ...module.injectables,
    ...module.middlewares,
  ];

  const nonTransientInstances = getNonTransientInstances(instances);
  await Promise.all(callOperator(nonTransientInstances));
  const transientInstances = getTransientInstances(instances);
  await Promise.all(callOperator(transientInstances));

  // Call the instance itself
  const moduleClassInstance = moduleClassHost.instance;
  if (
    moduleClassInstance &&
    hasOnAppBootstrapHook(moduleClassInstance) &&
    moduleClassHost.isDependencyTreeStatic()
  ) {
    await moduleClassInstance.onApplicationBootstrap();
  }
}
```

---

## 86. Sample 49 · callee #1

- **Function:** `callShutdownHook`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/nest-application-context.ts`
- **Callee:** `callAppShutdownHook(module, signal)`
- **Status:** OK

### Usage site (matched in test file)

Line 447, col 13 — pattern `anchor_substring`

```typescript
callAppShutdownHook(module, signal)
```

### Resolved definition

- **Path:** `packages/core/hooks/on-app-shutdown.hook.ts`
- **Range:** line 44, col 22
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
 * Calls the `onApplicationShutdown` function on the module and its children
 * (providers / controllers).
 *
 * @param module The module which will be initialized
 * @param signal
 */
export async function callAppShutdownHook(
  module: Module,
  signal?: string,
): Promise<any> {
  const providers = module.getNonAliasProviders();
  // Module (class) instance is the first element of the providers array
  // Lifecycle hook has to be called once all classes are properly initialized
  const [_, moduleClassHost] = providers.shift()!;
  const instances = [
    ...module.controllers,
    ...providers,
    ...module.injectables,
    ...module.middlewares,
  ];

  const nonTransientInstances = getNonTransientInstances(instances);
  await Promise.all(callOperator(nonTransientInstances, signal));
  const transientInstances = getTransientInstances(instances);
  await Promise.all(callOperator(transientInstances, signal));

  // Call the instance itself
  const moduleClassInstance = moduleClassHost.instance;
  if (
    moduleClassInstance &&
    hasOnAppShutdownHook(moduleClassInstance) &&
    moduleClassHost.isDependencyTreeStatic()
  ) {
    await moduleClassInstance.onApplicationShutdown(signal);
  }
}
```

---

## 87. Sample 50 · callee #1

- **Function:** `callBeforeShutdownHook`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/nest-application-context.ts`
- **Callee:** `callBeforeAppShutdownHook(module, signal)`
- **Status:** OK

### Usage site (matched in test file)

Line 461, col 13 — pattern `anchor_substring`

```typescript
callBeforeAppShutdownHook(module, signal)
```

### Resolved definition

- **Path:** `packages/core/hooks/before-app-shutdown.hook.ts`
- **Range:** line 48, col 22
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
 * Calls the `beforeApplicationShutdown` function on the module and its children
 * (providers / controllers).
 *
 * @param module The module which will be initialized
 * @param signal The signal which caused the shutdown
 */
export async function callBeforeAppShutdownHook(
  module: Module,
  signal?: string,
): Promise<void> {
  const providers = module.getNonAliasProviders();
  const [_, moduleClassHost] = providers.shift()!;
  const instances = [
    ...module.controllers,
    ...providers,
    ...module.injectables,
    ...module.middlewares,
  ];

  const nonTransientInstances = getNonTransientInstances(instances);
  await Promise.all(callOperator(nonTransientInstances, signal));
  const transientInstances = getTransientInstances(instances);
  await Promise.all(callOperator(transientInstances, signal));

  const moduleClassInstance = moduleClassHost.instance;
  if (
    moduleClassInstance &&
    hasBeforeApplicationShutdownHook(moduleClassInstance) &&
    moduleClassHost.isDependencyTreeStatic()
  ) {
    await moduleClassInstance.beforeApplicationShutdown(signal);
  }
}
```

---

## 88. Sample 51 · callee #0

- **Function:** `makeHelpMessage`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/repl/repl-function.ts`
- **Callee:** `clc.yellow(description)`
- **Status:** OK

### Usage site (matched in test file)

Line 32, col 15 — pattern `anchor_substring`

```typescript
clc.yellow(description)
```

### Resolved definition

- **Path:** `packages/common/utils/cli-colors.util.ts`
- **Range:** line 3, col 49
- **Selection:** `preferred_implementation_over_declaration_kept=2`

```typescript
export const yellow = colorIfAllowed(
  (text: string) => `\x1B[38;5;3m${text}\x1B[39m`,
);
```

---

## 89. Sample 51 · callee #1

- **Function:** `makeHelpMessage`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/repl/repl-function.ts`
- **Callee:** `clc.magentaBright(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 32, col 47 — pattern `core_fallback`

```typescript
clc.magentaBright(...)
```

### Resolved definition

- **Path:** `packages/common/utils/cli-colors.util.ts`
- **Range:** line 3, col 49
- **Selection:** `preferred_implementation_over_declaration_kept=2`

```typescript
magentaBright: colorIfAllowed((text: string) => `\x1B[95m${text}\x1B[39m`),
```

---

## 90. Sample 51 · callee #2

- **Function:** `makeHelpMessage`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/repl/repl-function.ts`
- **Callee:** `clc.bold(fnSignatureWithName)`
- **Status:** OK

### Usage site (matched in test file)

Line 34, col 10 — pattern `anchor_substring`

```typescript
clc.bold(fnSignatureWithName)
```

### Resolved definition

- **Path:** `packages/common/utils/cli-colors.util.ts`
- **Range:** line 3, col 49
- **Selection:** `preferred_implementation_over_declaration_kept=2`

```typescript
bold: colorIfAllowed((text: string) => `\x1B[1m${text}\x1B[0m`),
```

---

## 91. Sample 51 · callee #3

- **Function:** `makeHelpMessage`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/repl/repl-function.ts`
- **Callee:** `this.fnDefinition`
- **Status:** OK

### Usage site (matched in test file)

Line 28, col 46 — pattern `anchor_substring`

```typescript
this.fnDefinition
```

### Resolved definition

- **Path:** `packages/core/repl/repl-function.ts`
- **Range:** line 10, col 18
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/** Metadata that describes the built-in function itself. */
  public abstract fnDefinition: ReplFnDefinition;
```

---

## 92. Sample 53 · callee #0

- **Function:** `addScopedEnhancersMetadata`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/scanner.ts`
- **Callee:** `this.isRequestOrTransient(wrapper.scope!)`
- **Status:** OK

### Usage site (matched in test file)

Line 631, col 26 — pattern `anchor_substring`

```typescript
this.isRequestOrTransient(wrapper.scope!)
```

### Resolved definition

- **Path:** `packages/core/scanner.ts`
- **Range:** line 751, col 10
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  private isRequestOrTransient(scope: Scope): boolean {
    return scope === Scope.REQUEST || scope === Scope.TRANSIENT;
  }
```

---

## 93. Sample 53 · callee #1

- **Function:** `addScopedEnhancersMetadata`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/scanner.ts`
- **Callee:** `this.container.getModules()`
- **Status:** OK

### Usage site (matched in test file)

Line 633, col 34 — pattern `anchor_substring`

```typescript
this.container.getModules()
```

### Resolved definition

- **Path:** `packages/core/injector/container.ts`
- **Range:** line 217, col 9
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  public getModules(): ModulesContainer {
    return this.modules;
  }
```

---

## 94. Sample 53 · callee #2

- **Function:** `addScopedEnhancersMetadata`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/scanner.ts`
- **Callee:** `injectables.get(providerKey)`
- **Status:** OK

### Usage site (matched in test file)

Line 635, col 33 — pattern `anchor_substring`

```typescript
injectables.get(providerKey)
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

## 95. Sample 53 · callee #4

- **Function:** `addScopedEnhancersMetadata`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/scanner.ts`
- **Callee:** `controllerOrEntryProvider.addEnhancerMetadata(instanceWrapper!)`
- **Status:** OK

### Usage site (matched in test file)

Line 646, col 13 — pattern `anchor_substring`

```typescript
controllerOrEntryProvider.addEnhancerMetadata(instanceWrapper!)
```

### Resolved definition

- **Path:** `packages/core/injector/instance-wrapper.ts`
- **Range:** line 216, col 9
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  public addEnhancerMetadata(wrapper: InstanceWrapper) {
    if (!this[INSTANCE_METADATA_SYMBOL].enhancers) {
      this[INSTANCE_METADATA_SYMBOL].enhancers = [];
    }
    this[INSTANCE_METADATA_SYMBOL].enhancers.push(wrapper);
  }
```

---

## 96. Sample 53 · callee #7

- **Function:** `addScopedEnhancersMetadata`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/scanner.ts`
- **Callee:** `this.applicationProvidersApplyMap`
- **Status:** OK

### Usage site (matched in test file)

Line 630, col 13 — pattern `anchor_substring`

```typescript
this.applicationProvidersApplyMap
```

### Resolved definition

- **Path:** `packages/core/scanner.ts`
- **Range:** line 75, col 19
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
private readonly applicationProvidersApplyMap: ApplicationProviderWrapper[] =
```

---

## 97. Sample 53 · callee #8

- **Function:** `addScopedEnhancersMetadata`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/scanner.ts`
- **Callee:** `wrapper.scope`
- **Status:** OK

### Usage site (matched in test file)

Line 631, col 52 — pattern `anchor_substring`

```typescript
wrapper.scope
```

### Resolved definition

- **Path:** `packages/core/scanner.ts`
- **Range:** line 63, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  scope?: Scope;
```

---

## 98. Sample 53 · callee #9

- **Function:** `addScopedEnhancersMetadata`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/scanner.ts`
- **Callee:** `this.container`
- **Status:** OK

### Usage site (matched in test file)

Line 633, col 34 — pattern `anchor_substring`

```typescript
this.container
```

### Resolved definition

- **Path:** `packages/core/scanner.ts`
- **Range:** line 79, col 21
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
private readonly container: NestContainer,
```

---

## 99. Sample 53 · callee #10

- **Function:** `addScopedEnhancersMetadata`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/scanner.ts`
- **Callee:** `Array.from`
- **Status:** OK

### Usage site (matched in test file)

Line 640, col 13 — pattern `anchor_substring`

```typescript
Array.from
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es2015.core.d.ts`
- **Range:** line 64, col 28

```typescript
/**
     * Creates an array from an array-like object.
     * @param arrayLike An array-like object to convert to an array.
     */
    from<T>(arrayLike: ArrayLike<T>): T[];
```

---

## 100. Sample 53 · callee #11

- **Function:** `addScopedEnhancersMetadata`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/scanner.ts`
- **Callee:** `moduleRef.controllers`
- **Status:** OK

### Usage site (matched in test file)

Line 640, col 41 — pattern `anchor_substring`

```typescript
moduleRef.controllers
```

### Resolved definition

- **Path:** `packages/core/injector/module.ts`
- **Range:** line 126, col 6
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  get controllers(): Map<InjectionToken, InstanceWrapper<Controller>> {
    return this._controllers;
  }
```

---

## 101. Sample 53 · callee #12

- **Function:** `addScopedEnhancersMetadata`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/scanner.ts`
- **Callee:** `moduleRef.entryProviders`
- **Status:** OK

### Usage site (matched in test file)

Line 641, col 15 — pattern `anchor_substring`

```typescript
moduleRef.entryProviders
```

### Resolved definition

- **Path:** `packages/core/injector/module.ts`
- **Range:** line 130, col 6
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  get entryProviders(): Array<InstanceWrapper<Injectable>> {
    return Array.from(this._entryProviderKeys).map(
      token => this.providers.get(token)!,
    );
  }
```

---

## 102. Sample 54 · callee #0

- **Function:** `isInjectable`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/core/scanner.ts`
- **Callee:** `Reflect.getMetadata(INJECTABLE_WATERMARK, metatype)`
- **Status:** OK
- **Also seen in:** 2 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 727, col 14 — pattern `anchor_substring`

```typescript
Reflect.getMetadata(INJECTABLE_WATERMARK, metatype)
```

### Resolved definition

- **Path:** `node_modules/reflect-metadata/Reflect.js`
- **Range:** line 364, col 17
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
         * Gets the metadata value for the provided metadata key on the target object or its prototype chain.
         * @param metadataKey A key used to store and retrieve metadata.
         * @param target The target object on which the metadata is defined.
         * @param propertyKey (Optional) The property key for the target.
         * @returns The metadata value for the metadata key if found; otherwise, `undefined`.
         * @example
         *
         *     class Example {
         *         // property declarations are not part of ES6, though they are valid in TypeScript:
         *         // static staticProperty;
         *         // property;
         *
         *         constructor(p) { }
         *         static staticMethod(p) { }
         *         method(p) { }
         *     }
         *
         *     // constructor
         *     result = Reflect.getMetadata("custom:annotation", Example);
         *
         *     // property (on constructor)
         *     result = Reflect.getMetadata("custom:annotation", Example, "staticProperty");
         *
         *     // property (on prototype)
         *     result = Reflect.getMetadata("custom:annotation", Example.prototype, "property");
         *
         *     // method (on constructor)
         *     result = Reflect.getMetadata("custom:annotation", Example, "staticMethod");
         *
         *     // method (on prototype)
         *     result = Reflect.getMetadata("custom:annotation", Example.prototype, "method");
         *
         */
        function getMetadata(metadataKey, target, propertyKey) {
            if (!IsObject(target))
                throw new TypeError();
            if (!IsUndefined(propertyKey))
                propertyKey = ToPropertyKey(propertyKey);
            return OrdinaryGetMetadata(metadataKey, target, propertyKey);
        }
```

---

## 103. Sample 57 · callee #0

- **Function:** `?`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/microservices/client/client-proxy.ts`
- **Callee:** ``
- **Status:** FAILED
- **Error:** could not extract tested_function

---

## 104. Sample 58 · callee #0

- **Function:** `getArgs`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/microservices/ctx-host/base-rpc.context.ts`
- **Callee:** `this.args`
- **Status:** OK
- **Also seen in:** 16 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 11, col 12 — pattern `anchor_substring`

```typescript
this.args
```

### Resolved definition

- **Path:** `packages/microservices/ctx-host/base-rpc.context.ts`
- **Range:** line 4, col 33
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  constructor(protected readonly args: T) {}
```

---

## 105. Sample 75 · callee #0

- **Function:** `status`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/microservices/nest-microservice.ts`
- **Callee:** `this.serverInstance`
- **Status:** OK
- **Also seen in:** 4 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 56, col 12 — pattern `anchor_substring`

```typescript
this.serverInstance
```

### Resolved definition

- **Path:** `packages/microservices/nest-microservice.ts`
- **Range:** line 47, col 10
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  private serverInstance: Server;
```

---

## 106. Sample 76 · callee #0

- **Function:** `useWebSocketAdapter`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/microservices/nest-microservice.ts`
- **Callee:** `this.applicationConfig.setIoAdapter(adapter)`
- **Status:** OK

### Usage site (matched in test file)

Line 147, col 5 — pattern `anchor_substring`

```typescript
this.applicationConfig.setIoAdapter(adapter)
```

### Resolved definition

- **Path:** `packages/core/application-config.ts`
- **Range:** line 47, col 9
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  public setIoAdapter(ioAdapter: WebSocketAdapter) {
    this.ioAdapter = ioAdapter;
  }
```

---

## 107. Sample 76 · callee #1

- **Function:** `useWebSocketAdapter`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/microservices/nest-microservice.ts`
- **Callee:** `this.applicationConfig`
- **Status:** OK
- **Also seen in:** 3 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 147, col 5 — pattern `anchor_substring`

```typescript
this.applicationConfig
```

### Resolved definition

- **Path:** `packages/microservices/nest-microservice.ts`
- **Range:** line 62, col 21
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
private readonly applicationConfig: ApplicationConfig,
```

---

## 108. Sample 77 · callee #0

- **Function:** `useGlobalFilters`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/microservices/nest-microservice.ts`
- **Callee:** `this.applicationConfig.useGlobalFilters(...filters)`
- **Status:** OK

### Usage site (matched in test file)

Line 157, col 5 — pattern `anchor_substring`

```typescript
this.applicationConfig.useGlobalFilters(...filters)
```

### Resolved definition

- **Path:** `packages/core/application-config.ts`
- **Range:** line 71, col 9
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  public useGlobalFilters(...filters: ExceptionFilter[]) {
    this.globalFilters = this.globalFilters.concat(filters);
  }
```

---

## 109. Sample 77 · callee #1

- **Function:** `useGlobalFilters`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/microservices/nest-microservice.ts`
- **Callee:** `this.graphInspector.insertOrphanedEnhancer(...)`
- **Status:** OK
- **Also seen in:** 2 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 159, col 27 — pattern `core_fallback`

```typescript
this.graphInspector.insertOrphanedEnhancer(...)
```

### Resolved definition

- **Path:** `packages/core/inspector/graph-inspector.ts`
- **Range:** line 85, col 9
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  public insertOrphanedEnhancer(entry: OrphanedEnhancerDefinition) {
    this.graph.insertOrphanedEnhancer({
      ...entry,
      ref: entry.ref?.constructor?.name ?? 'Object',
    });
  }
```

---

## 110. Sample 77 · callee #3

- **Function:** `useGlobalFilters`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/microservices/nest-microservice.ts`
- **Callee:** `this.graphInspector`
- **Status:** OK
- **Also seen in:** 2 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 159, col 7 — pattern `anchor_substring`

```typescript
this.graphInspector
```

### Resolved definition

- **Path:** `packages/microservices/nest-microservice.ts`
- **Range:** line 61, col 21
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
private readonly graphInspector: GraphInspector,
```

---

## 111. Sample 78 · callee #0

- **Function:** `useGlobalPipes`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/microservices/nest-microservice.ts`
- **Callee:** `this.applicationConfig.useGlobalPipes(...pipes)`
- **Status:** OK

### Usage site (matched in test file)

Line 173, col 5 — pattern `anchor_substring`

```typescript
this.applicationConfig.useGlobalPipes(...pipes)
```

### Resolved definition

- **Path:** `packages/core/application-config.ts`
- **Range:** line 59, col 9
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  public useGlobalPipes(...pipes: PipeTransform<any>[]) {
    this.globalPipes = this.globalPipes.concat(pipes);
  }
```

---

## 112. Sample 79 · callee #0

- **Function:** `useGlobalInterceptors`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/microservices/nest-microservice.ts`
- **Callee:** `this.applicationConfig.useGlobalInterceptors(...interceptors)`
- **Status:** OK

### Usage site (matched in test file)

Line 189, col 5 — pattern `anchor_substring`

```typescript
this.applicationConfig.useGlobalInterceptors(...interceptors)
```

### Resolved definition

- **Path:** `packages/core/application-config.ts`
- **Range:** line 87, col 9
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  public useGlobalInterceptors(...interceptors: NestInterceptor[]) {
    this.globalInterceptors = this.globalInterceptors.concat(interceptors);
  }
```

---

## 113. Sample 80 · callee #0

- **Function:** `listen`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/microservices/nest-microservice.ts`
- **Callee:** `this.assertNotInPreviewMode('listen')`
- **Status:** OK

### Usage site (matched in test file)

Line 225, col 5 — pattern `anchor_substring`

```typescript
this.assertNotInPreviewMode('listen')
```

### Resolved definition

- **Path:** `packages/core/nest-application-context.ts`
- **Range:** line 464, col 12
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  protected assertNotInPreviewMode(methodName: string) {
    if (this.appOptions.preview) {
      const error = `Calling the "${methodName}" in the preview mode is not supported.`;
      this.logger.error(error);
      throw new Error(error);
    }
  }
```

---

## 114. Sample 80 · callee #1

- **Function:** `listen`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/microservices/nest-microservice.ts`
- **Callee:** `this.registerModules()`
- **Status:** OK

### Usage site (matched in test file)

Line 226, col 35 — pattern `anchor_substring`

```typescript
this.registerModules()
```

### Resolved definition

- **Path:** `packages/microservices/nest-microservice.ts`
- **Range:** line 107, col 3

```typescript
  public async registerModules(): Promise<any> {
    this.socketModule &&
      this.socketModule.register(
        this.container,
        this.applicationConfig,
        this.graphInspector,
        this.appOptions,
      );

    if (!this.appOptions.preview) {
      this.microservicesModule.setupClients(this.container);
      this.registerListeners();
    }

    this.setIsInitialized(true);

    if (!this.wasInitHookCalled) {
      await this.callInitHook();
      await this.callBootstrapHook();
    }
  }
```

---

## 115. Sample 80 · callee #2

- **Function:** `listen`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/microservices/nest-microservice.ts`
- **Callee:** `this.serverInstance.listen(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 224, col 16 — pattern `core_fallback`

```typescript
this.serverInstance.listen(...)
```

### Resolved definition

- **Path:** `packages/microservices/nest-microservice.ts`
- **Range:** line 216, col 3

```typescript
/**
   * Starts the microservice.
   *
   * @returns {void}
   */
  public async listen(): Promise<any> {
    this.assertNotInPreviewMode('listen');
    !this.isInitialized && (await this.registerModules());

    return new Promise<any>((resolve, reject) => {
      this.serverInstance.listen((err, info) => {
        if (this.microserviceConfig?.autoFlushLogs ?? true) {
          this.flushLogs();
        }
        if (err) {
          return reject(err as Error);
        }
        this.logger.log(MESSAGES.MICROSERVICE_READY);
        resolve(info);
      });
    });
  }
```

---

## 116. Sample 80 · callee #4

- **Function:** `listen`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/microservices/nest-microservice.ts`
- **Callee:** `this.logger.log(MESSAGES.MICROSERVICE_READY)`
- **Status:** OK

### Usage site (matched in test file)

Line 236, col 9 — pattern `anchor_substring`

```typescript
this.logger.log(MESSAGES.MICROSERVICE_READY)
```

### Resolved definition

- **Path:** `packages/common/services/logger.service.ts`
- **Range:** line 152, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript

  /**
   * Write a 'log' level log.
   */
  log(message: any, context?: string): void;
```

---

## 117. Sample 80 · callee #5

- **Function:** `listen`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/microservices/nest-microservice.ts`
- **Callee:** `this.isInitialized`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 226, col 6 — pattern `anchor_substring`

```typescript
this.isInitialized
```

### Resolved definition

- **Path:** `node_modules/@nestjs/core/nest-application-context.d.ts`
- **Range:** line 16, col 27

```typescript
protected isInitialized: boolean;
```

---

## 118. Sample 80 · callee #7

- **Function:** `listen`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/microservices/nest-microservice.ts`
- **Callee:** `this.microserviceConfig`
- **Status:** OK

### Usage site (matched in test file)

Line 230, col 13 — pattern `anchor_substring`

```typescript
this.microserviceConfig
```

### Resolved definition

- **Path:** `packages/microservices/nest-microservice.ts`
- **Range:** line 43, col 10
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
private microserviceConfig: Exclude<
```

---

## 119. Sample 80 · callee #8

- **Function:** `listen`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/microservices/nest-microservice.ts`
- **Callee:** `this.logger`
- **Status:** OK

### Usage site (matched in test file)

Line 236, col 9 — pattern `anchor_substring`

```typescript
this.logger
```

### Resolved definition

- **Path:** `packages/microservices/nest-microservice.ts`
- **Range:** line 37, col 1

```typescript
protected readonly logger = new Logger(NestMicroservice.name, {
```

---

## 120. Sample 80 · callee #9

- **Function:** `listen`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/microservices/nest-microservice.ts`
- **Callee:** `MESSAGES.MICROSERVICE_READY`
- **Status:** OK

### Usage site (matched in test file)

Line 236, col 25 — pattern `anchor_substring`

```typescript
MESSAGES.MICROSERVICE_READY
```

### Resolved definition

- **Path:** `packages/core/constants.ts`
- **Range:** line 5, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
MICROSERVICE_READY: `Nest microservice successfully started`,
```

---

## 121. Sample 81 · callee #0

- **Function:** `close`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/microservices/nest-microservice.ts`
- **Callee:** `this.serverInstance.close()`
- **Status:** OK

### Usage site (matched in test file)

Line 248, col 11 — pattern `anchor_substring`

```typescript
this.serverInstance.close()
```

### Resolved definition

- **Path:** `packages/microservices/server/server.ts`
- **Range:** line 99, col 18
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  /**
   * Method called when server is being terminated.
   */
  public abstract close(): any;
```

---

## 122. Sample 81 · callee #1

- **Function:** `close`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/microservices/nest-microservice.ts`
- **Callee:** `this.setIsTerminated(true)`
- **Status:** OK

### Usage site (matched in test file)

Line 252, col 5 — pattern `anchor_substring`

```typescript
this.setIsTerminated(true)
```

### Resolved definition

- **Path:** `packages/microservices/nest-microservice.ts`
- **Range:** line 267, col 9
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
   * Sets the flag indicating that the application is terminated.
   * @param isTerminated Value to set
   */
  public setIsTerminated(isTerminated: boolean) {
    this.isTerminated = isTerminated;
  }
```

---

## 123. Sample 81 · callee #2

- **Function:** `close`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/microservices/nest-microservice.ts`
- **Callee:** `this.closeApplication()`
- **Status:** OK

### Usage site (matched in test file)

Line 253, col 11 — pattern `anchor_substring`

```typescript
this.closeApplication()
```

### Resolved definition

- **Path:** `packages/microservices/nest-microservice.ts`
- **Range:** line 300, col 3

```typescript
  protected async closeApplication(): Promise<any> {
    this.socketModule && (await this.socketModule.close());
    this.microservicesModule && (await this.microservicesModule.close());

    await super.close();
    this.setIsTerminated(true);
  }
```

---

## 124. Sample 81 · callee #4

- **Function:** `close`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/microservices/nest-microservice.ts`
- **Callee:** `this.isTerminated`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 249, col 9 — pattern `anchor_substring`

```typescript
this.isTerminated
```

### Resolved definition

- **Path:** `packages/microservices/nest-microservice.ts`
- **Range:** line 47, col 33

```typescript
private isTerminated = false;
```

---

## 125. Sample 84 · callee #0

- **Function:** `setIsInitHookCalled`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/microservices/nest-microservice.ts`
- **Callee:** `this.wasInitHookCalled`
- **Status:** OK

### Usage site (matched in test file)

Line 277, col 5 — pattern `anchor_substring`

```typescript
this.wasInitHookCalled
```

### Resolved definition

- **Path:** `packages/microservices/nest-microservice.ts`
- **Range:** line 48, col 31

```typescript
private wasInitHookCalled = false;
```

---

## 126. Sample 85 · callee #0

- **Function:** `on`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/microservices/nest-microservice.ts`
- **Callee:** `this.serverInstance.on(event as string, callback)`
- **Status:** OK

### Usage site (matched in test file)

Line 287, col 14 — pattern `anchor_substring`

```typescript
this.serverInstance.on(event as string, callback)
```

### Resolved definition

- **Path:** `packages/microservices/server/server.ts`
- **Range:** line 81, col 18
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
   * Registers an event listener for the given event.
   * @param event Event name
   * @param callback Callback to be executed when the event is emitted
   */
  public abstract on<
    EventKey extends keyof EventsMap = keyof EventsMap,
    EventCallback extends EventsMap[EventKey] = EventsMap[EventKey],
  >(event: EventKey, callback: EventCallback): any;
```

---

## 127. Sample 85 · callee #1

- **Function:** `on`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/microservices/nest-microservice.ts`
- **Callee:** `Error('"on" method not supported by the underlying server')`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 289, col 15 — pattern `anchor_substring`

```typescript
Error('"on" method not supported by the underlying server')
```

### Resolved definition

- **Path:** `/Users/trieyang/Desktop/DocPrism/node_modules/typescript/lib/lib.es5.d.ts`
- **Range:** line 1070, col 38

```typescript
declare var Error: ErrorConstructor;
```

---

## 128. Sample 86 · callee #0

- **Function:** `unwrap`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/microservices/nest-microservice.ts`
- **Callee:** `this.serverInstance.unwrap()`
- **Status:** OK

### Usage site (matched in test file)

Line 298, col 14 — pattern `anchor_substring`

```typescript
this.serverInstance.unwrap()
```

### Resolved definition

- **Path:** `packages/microservices/server/server.ts`
- **Range:** line 89, col 18
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  /**
   * Returns an instance of the underlying server/broker instance,
   * or a group of servers if there are more than one.
   */
  public abstract unwrap<T>(): T;
```

---

## 129. Sample 87 · callee #0

- **Function:** `getServiceNames`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/microservices/server/server-grpc.ts`
- **Callee:** `this.collectDeepServices('', grpcPkg, services)`
- **Status:** OK

### Usage site (matched in test file)

Line 128, col 5 — pattern `anchor_substring`

```typescript
this.collectDeepServices('', grpcPkg, services)
```

### Resolved definition

- **Path:** `packages/microservices/server/server-grpc.ts`
- **Range:** line 590, col 10
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
   * Recursively fetch all of the service methods available on loaded
   * protobuf descriptor object, and collect those as an objects with
   * dot-syntax full-path names.
   *
   * Example:
   *  for proto package Bundle.FirstService with service Events { rpc...
   *  will be resolved to object of (while loaded for Bundle package):
   *    {
   *      name: "FirstService.Events",
   *      service: {Object}
   *    }
   */
  private collectDeepServices(
    name: string,
    grpcDefinition: any,
    accumulator: { name: string; service: any }[],
  ) {
    if (!isObject(grpcDefinition)) {
      return;
    }
    const keysToTraverse = Object.keys(grpcDefinition);
    // Traverse definitions or namespace extensions
    for (const key of keysToTraverse) {
      const nameExtended = this.parseDeepServiceName(name, key);
      const deepDefinition = grpcDefinition[key];

      const isServiceDefined =
        deepDefinition && !isUndefined(deepDefinition.service);
      const isServiceBoolean = isServiceDefined
        ? deepDefinition.service !== false
        : false;

      // grpc namespace object does not have 'format' or 'service' properties defined
      const isFormatDefined =
        deepDefinition && !isUndefined(deepDefinition.format);

      if (isServiceDefined && isServiceBoolean) {
        accumulator.push({
          name: nameExtended,
          service: deepDefinition,
        });
      } else if (isFormatDefined) {
        // Do nothing
      } else {
        // Continue recursion for namespace object until objects end or service definition found
        this.collectDeepServices(nameExtended, deepDefinition, accumulator);
      }
    }
  }
```

---

## 130. Sample 88 · callee #0

- **Function:** `createService`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/microservices/server/server-grpc.ts`
- **Callee:** `this.getMessageHandler(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 152, col 30 — pattern `core_fallback`

```typescript
this.getMessageHandler(...)
```

### Resolved definition

- **Path:** `packages/microservices/server/server-grpc.ts`
- **Range:** line 191, col 9
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  public getMessageHandler(
    serviceName: string,
    methodName: string,
    streaming: GrpcMethodStreamingType,
    grpcMethod: { path?: string },
  ): MessageHandler {
    let pattern = this.createPattern(serviceName, methodName, streaming);
    let methodHandler = this.messageHandlers.get(pattern)!;
    if (!methodHandler) {
      const packageServiceName = grpcMethod.path?.split?.('/')[1];
      pattern = this.createPattern(packageServiceName!, methodName, streaming);
      methodHandler = this.messageHandlers.get(pattern)!;
    }
    return methodHandler;
  }
```

---

## 131. Sample 88 · callee #2

- **Function:** `createService`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/microservices/server/server-grpc.ts`
- **Callee:** `GrpcMethodStreamingType.NO_STREAMING`
- **Status:** OK

### Usage site (matched in test file)

Line 144, col 27 — pattern `anchor_substring`

```typescript
GrpcMethodStreamingType.NO_STREAMING
```

### Resolved definition

- **Path:** `packages/microservices/decorators/message-pattern.decorator.ts`
- **Range:** line 22, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
NO_STREAMING = 'no_stream',
```

---

## 132. Sample 88 · callee #3

- **Function:** `createService`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/microservices/server/server-grpc.ts`
- **Callee:** `GrpcMethodStreamingType.RX_STREAMING`
- **Status:** OK

### Usage site (matched in test file)

Line 155, col 11 — pattern `anchor_substring`

```typescript
GrpcMethodStreamingType.RX_STREAMING
```

### Resolved definition

- **Path:** `packages/microservices/decorators/message-pattern.decorator.ts`
- **Range:** line 23, col 2
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
RX_STREAMING = 'rx_stream',
```

---

## 133. Sample 89 · callee #1

- **Function:** `getRouteFromPattern`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/packages/microservices/server/server.ts`
- **Callee:** `this.normalizePattern(validPattern)`
- **Status:** OK

### Usage site (matched in test file)

Line 290, col 12 — pattern `anchor_substring`

```typescript
this.normalizePattern(validPattern)
```

### Resolved definition

- **Path:** `packages/microservices/server/server.ts`
- **Range:** line 292, col 12
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
  protected normalizePattern(pattern: MsPattern): string {
    return transformPatternToRoute(pattern);
  }
```

---

## 134. Sample 91 · callee #0

- **Function:** `cleanOutput`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/tools/gulp/tasks/clean.ts`
- **Callee:** `src(...)`
- **Status:** OK
- **Also seen in:** 1 other callee row with the same resolved definition

### Usage site (matched in test file)

Line 10, col 10 — pattern `core_fallback`

```typescript
src(...)
```

### Resolved definition

- **Path:** `node_modules/@types/gulp/index.d.ts`
- **Range:** line 18, col 39

```typescript
/**
         * Emits files matching provided glob or array of globs. Returns a stream of Vinyl files that can be piped to plugins.
         * @param globs Glob or array of globs to read.
         * @param options Options to pass to node-glob through glob-stream.
         */
        src: SrcMethod;
```

---

## 135. Sample 91 · callee #1

- **Function:** `cleanOutput`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/tools/gulp/tasks/clean.ts`
- **Callee:** `clean()`
- **Status:** OK

### Usage site (matched in test file)

Line 20, col 10 — pattern `anchor_substring`

```typescript
clean()
```

### Resolved definition

- **Path:** `node_modules/gulp-clean/index.js`
- **Range:** line 6, col 0
- **Selection:** `definition_via_node_module_import`

```typescript
module.exports = function (options) {
  return through2.obj(function (file, enc, cb) {
    // Paths are resolved by gulp
    var filepath = file.path;
    var cwd = file.cwd;
    var relative = path.relative(cwd, filepath);

    // Prevent mistakes with paths
    if (!(relative.substr(0, 2) === '..') && relative !== '' || (options ? (options.force && typeof options.force === 'boolean') : false)) {
      rimraf(filepath, function (error) {
        if (error) {
          this.emit('error', new utils.PluginError('gulp-clean', 'Unable to delete "' + filepath + '" file (' + error.message + ').'));
        }
        this.push(file);
        cb();
      }.bind(this));
    } else if (relative === '') {
      var msgCurrent = 'Cannot delete current working directory. (' + filepath + '). Use option force.';
      utils.log('gulp-clean: ' + msgCurrent);
      this.emit('error', new utils.PluginError('gulp-clean', msgCurrent));
      this.push(file);
      cb();
    } else {
      var msgOutside = 'Cannot delete files outside the current working directory. (' + filepath + '). Use option force.';
      utils.log('gulp-clean: ' + msgOutside);
      this.emit('error', new utils.PluginError('gulp-clean', msgOutside));
      this.push(file);
      cb();
    }
  });
};
```

---

## 136. Sample 92 · callee #0

- **Function:** `copyMisc`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/tools/gulp/tasks/copy-misc.ts`
- **Callee:** `packagePaths.reduce(...)`
- **Status:** OK

### Usage site (matched in test file)

Line 12, col 23 — pattern `core_fallback`

```typescript
packagePaths.reduce(...)
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

## 137. Sample 92 · callee #2

- **Function:** `copyMisc`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/tools/gulp/tasks/copy-misc.ts`
- **Callee:** `dest(packagePath)`
- **Status:** OK
- **Also seen in:** 2 other callee rows with the same resolved definition

### Usage site (matched in test file)

Line 13, col 42 — pattern `anchor_substring`

```typescript
dest(packagePath)
```

### Resolved definition

- **Path:** `node_modules/@types/gulp/index.d.ts`
- **Range:** line 24, col 23

```typescript
/**
         * Emits files matching provided glob or array of globs. Returns a stream of Vinyl files that can be piped to plugins.
         * @param globs Glob or array of globs to read.
         * @param options Options to pass to node-glob through glob-stream.
         */
/**
         * Can be piped to and it will write files. Re-emits all data passed to it so you can pipe to multiple folders.
         * Folders that don't exist will be created.
         * @param path The path (output folder) to write files to. Or a function that returns it, the function will be provided a vinyl File instance.
         */
        dest: DestMethod;
```

---

## 138. Sample 93 · callee #0

- **Function:** `moveToNodeModules`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/tools/gulp/tasks/move.ts`
- **Callee:** `distFiles.pipe(dest('node_modules/@nestjs'))`
- **Status:** OK

### Usage site (matched in test file)

Line 12, col 10 — pattern `anchor_substring`

```typescript
distFiles.pipe(dest('node_modules/@nestjs'))
```

### Resolved definition

- **Path:** `node_modules/@types/node/globals.d.ts`
- **Range:** line 206, col 32

```typescript
            pipe<T extends WritableStream>(destination: T, options?: { end?: boolean | undefined }): T;
```

---

## 139. Sample 94 · callee #0

- **Function:** `moveToSamples`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/tools/gulp/tasks/move.ts`
- **Callee:** `getDirs(samplePath)`
- **Status:** OK

### Usage site (matched in test file)

Line 19, col 23 — pattern `anchor_substring`

```typescript
getDirs(samplePath)
```

### Resolved definition

- **Path:** `tools/gulp/util/task-helpers.ts`
- **Range:** line 11, col 16
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
export function getDirs(base: string) {
  return getFolders(base).map(path => `${base}/${path}`);
}
```

---

## 140. Sample 94 · callee #1

- **Function:** `moveToSamples`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/tools/gulp/tasks/move.ts`
- **Callee:** `containsPackageJson(sampleDir)`
- **Status:** OK

### Usage site (matched in test file)

Line 29, col 9 — pattern `anchor_substring`

```typescript
containsPackageJson(sampleDir)
```

### Resolved definition

- **Path:** `tools/gulp/util/task-helpers.ts`
- **Range:** line 20, col 16
- **Selection:** `dropped_import_export_sites_kept=1`

```typescript
/**
 * Checks if the directory contains a package.json file
 * @param dir Path to the directory
 * @returns True if the directory contains a package.json
 */
export function containsPackageJson(dir: string) {
  return readdirSync(dir).some(file => file === 'package.json');
}
```

---

## 141. Sample 94 · callee #3

- **Function:** `moveToSamples`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/tools/gulp/tasks/move.ts`
- **Callee:** `join(dir, '/node_modules/@nestjs')`
- **Status:** OK

### Usage site (matched in test file)

Line 37, col 43 — pattern `anchor_substring`

```typescript
join(dir, '/node_modules/@nestjs')
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

## 142. Sample 94 · callee #4

- **Function:** `moveToSamples`
- **File:** `/Users/trieyang/Desktop/DocPrism/nest/tools/gulp/tasks/move.ts`
- **Callee:** `package.json`
- **Status:** FAILED
- **Error:** No candidates found by anchor inside tested_function (or file if range unknown).

---
