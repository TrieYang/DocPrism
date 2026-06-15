/**
 * Minimal demo for testing code_navigation_TypeScript.
 * Resolving "getBugInfo()" inside main() should find the function below.
 */

function getBugInfo(): { bug: string; version: string } {
  return { bug: "info", version: "1.0" };
}

function main(): void {
  /** Pretty-print the bug information as JSON. */
  console.log(JSON.stringify(getBugInfo(), null, 2));
}
