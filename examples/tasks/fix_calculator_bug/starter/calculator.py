def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    # BUG: floor division breaks floats and silently accepts some cases incorrectly.
    return a // b


def safe_eval(expr: str):
    # BUG: unsafe and too permissive.
    return eval(expr)
