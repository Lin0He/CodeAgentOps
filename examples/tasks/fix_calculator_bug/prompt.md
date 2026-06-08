Fix the calculator implementation.

Requirements:
- `divide(a, b)` must return true division.
- Division by zero must raise `ZeroDivisionError`.
- `safe_eval(expr)` should evaluate simple arithmetic expressions using numbers and operators `+ - * / ( )` only.
- `safe_eval` must reject names, attributes, function calls, imports, and any non-arithmetic Python syntax by raising `ValueError`.
- Preserve the behavior of `add`, `subtract`, and `multiply`.
