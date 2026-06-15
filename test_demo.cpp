// Minimal demo for testing code_navigation_Cpp.
// Resolving get_value() inside main() should find the function below.

int get_value() {
  return 42;
}

int main() {
  // Use the helper and print it
  int x = get_value();
  return x;
}
