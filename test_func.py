import pytest

from trapezoid_procedure import (
    parse_expression_to_postfix_form,
    is_parentheses,
    is_sign_of_operation,
    check_parentheses,
    replace_math_func_to_char,
    calculation,
    invoke_method, NoCalculation
)


# TEST is_parentheses
@pytest.mark.parametrize("char", ["(", ")"])
def test_is_parentheses(char):
    assert is_parentheses(char) is True


negative_parentheses = ["{", "}", "1", "", "A", ";"]


@pytest.mark.parametrize("char", negative_parentheses)
def test_is_parentheses_negative(char):
    assert is_parentheses(char) is False


# TEST is_sign_of_operation
SIGN_OF_OPERATION = ["+", "-", "/", "*", "^", "l", "t", "c", "s"]
NO_SIGN_OF_OPERATION = ["h", "//", ":", ".", "", "", "#", "2"]


@pytest.mark.parametrize("char", SIGN_OF_OPERATION)
def test_is_sign_of_operation(char):
    assert is_sign_of_operation(char) is True


@pytest.mark.parametrize("char", NO_SIGN_OF_OPERATION)
def test_is_sign_of_operation_negative(char):
    assert is_sign_of_operation(char) is False


# TEST check_parentheses

DATA_FOR_CHECK_PARENTHESES = [
    "()",
    "()()()()()",
    "((()))",
    "((())(())(()))"
]
DATA_FOR_CHECK_PARENTHESES_NEGATIVE = [
    "(",
    ")",
    "",
    "((())",
    "(1",
    "((((((((((((((((((((((()))",
]


@pytest.mark.parametrize("string", DATA_FOR_CHECK_PARENTHESES)
def test_check_parentheses(string):
    assert check_parentheses(string) is True


@pytest.mark.parametrize("string", DATA_FOR_CHECK_PARENTHESES_NEGATIVE)
def test_check_parentheses_negative(string):
    assert check_parentheses(string) is False


# TEST replace_math_func_to_char
data_for_replace_math_func_to_char = [
    ("sin", "s"),
    ("cos", "c"),
    ("ln", "l"),
    ("tg", "t"),
    ("tan", "t"),
    ("tan(4+x)+cos(2)*ln(x)", "t(4+x)+c(2)*l(x)")
]
data_for_replace_math_func_to_char_negative = [
    ("", ""),
    ("lg", "lg"),
    ("log", "log")
]


@pytest.mark.parametrize(
    "string, right_ans", data_for_replace_math_func_to_char)
def test_replace_math_func_to_char(string, right_ans):
    assert replace_math_func_to_char(string) == right_ans


@pytest.mark.parametrize(
    "string, right_ans", data_for_replace_math_func_to_char_negative)
def test_replace_math_func_to_char_negative(string, right_ans):
    assert replace_math_func_to_char(string) == right_ans


# TEST parse_expression_to_postfix_form
data_for_parse = [
    ("3+x", "3x+"),
    ("2+2", "22+"),
    ("l(2+(x*5)*2)*(3+x^2)", "2x5*2*+l3x2^+*")
]


@pytest.mark.parametrize("expression, result", data_for_parse)
def test_parse_expression_to_postfix_form(expression, result):
    postfix = parse_expression_to_postfix_form(expression)
    assert "".join(postfix) == result


# TEST calculation
data_for_calculation = [
    (["2", "2", "+"], 0, 4),
    (["x", "1", "+"], 1, 2)
]
data_for_calculation_negative = [
    (["2", "y", "+"], 1, 4),
    ([], 1, 4),
]


@pytest.mark.parametrize("postfix, x, result", data_for_calculation)
def test_calculation(postfix, x, result):
    assert calculation(postfix, x) == result


@pytest.mark.parametrize("postfix, x, result", data_for_calculation_negative)
def test_calculation_negative(postfix, x, result):
    try:
        calculation(postfix, x)
    except Exception as err:
        assert NoCalculation == type(err)


# TEST invoke_method
def test_invoke_method():
    # any expression, without 'X'
    result, ans = invoke_method("2+2")
    assert result is True
    assert ans == 4

    result, ans = invoke_method("sin(x)")
    assert result is True
    assert ans.__round__(3) == 0.956

    result, ans = invoke_method("x")
    assert result is True
    assert ans.__round__(3) == 1.5

    result, ans = invoke_method("3^x/x+x^2-4")
    assert result is True
    assert ans.__round__(3) == 1.895

    # invoke_method("0.9x+2")
    # assert result is True


# TEST invoke_method
def test_invoke_method_negative():
    # empty string
    result, ans = invoke_method("", 1, 1, 0.1)
    assert result is False


    result, ans = invoke_method("(x+2")
    assert result is False

    result, ans = invoke_method("(()()")
    assert result is False

    # result, ans = invoke_method("222")
    # assert result is False

    try:
        invoke_method("asd")
    except Exception as err:
        assert type(err) is NoCalculation



