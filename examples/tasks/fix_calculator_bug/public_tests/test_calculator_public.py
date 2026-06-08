import pytest
from calculator import add, divide, multiply, safe_eval, subtract


def test_basic_arithmetic_regression():
    assert add(2, 3) == 5
    assert subtract(5, 2) == 3
    assert multiply(4, 3) == 12


def test_divide_true_division():
    assert divide(5, 2) == 2.5


def test_safe_eval_simple_expression():
    assert safe_eval("2 + 3 * (4 - 1)") == 11
