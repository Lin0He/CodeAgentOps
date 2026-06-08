import pytest
from calculator import divide, safe_eval


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)


@pytest.mark.parametrize("expr", [
    "__import__('os').system('echo hacked')",
    "open('x.txt', 'w')",
    "(1).__class__",
    "lambda x: x",
])
def test_safe_eval_rejects_unsafe_syntax(expr):
    with pytest.raises(ValueError):
        safe_eval(expr)


def test_safe_eval_rejects_unknown_names():
    with pytest.raises(ValueError):
        safe_eval("a + 1")
