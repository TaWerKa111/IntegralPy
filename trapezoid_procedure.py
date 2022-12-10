from math import cos, sin, log, tan

CALCULATE_OPERATION = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,
    "^": lambda a, b: a ** b,
    "c": lambda a: cos(a),
    "s": lambda a: sin(a),
    "l": lambda a: log(a),
    "t": lambda a: tan(a)
}


PRIORITY_OPERATION = {
    "(": 1,
    "+": 2,
    "-": 2,
    "*": 3,
    "/": 3,
    "^": 4,
    "l": 5,
    "t": 5,
    "c": 5,
    "s": 5,
    "e": 5,
}


class NoCalculation(Exception):
    pass


def parse_expression_to_postfix_form(expression: str) -> list:
    """
    Перевод выражения в постфиксную запись в виде очереди

    :param expression: str.
        вычисляемое выражение
    :return: list,
         очередь выражения в постфиксной форме
    """

    queue_postfix_form = list()
    operation_stack = list()

    for char in expression:
        if not is_sign_of_operation(char) and not (is_parentheses(char)):
            queue_postfix_form.append(char)
        else:
            if is_sign_of_operation(char):
                priority_operation = PRIORITY_OPERATION[char]

                if len(operation_stack) > 0:
                    while operation_stack and PRIORITY_OPERATION[operation_stack[-1]] >= priority_operation:
                        operation = operation_stack.pop()
                        queue_postfix_form.append(operation)
                    operation_stack.append(char)
                else:
                    operation_stack.append(char)

            if char == "(":
                operation_stack.append(char)

            if char == ")" and len(operation_stack) > 0:
                temp = operation_stack.pop()

                while temp != "(":
                    queue_postfix_form.append(temp)
                    temp = operation_stack.pop()

    if operation_stack:
        while operation_stack:
            queue_postfix_form.append(operation_stack.pop())

    return queue_postfix_form


def is_parentheses(char: str) -> bool:
    """
    Является ли символ скобкой

    :param char: str,
        проверяемый символ
    :return: bool
        True - символ является скобкой
        False - символ не является скобкой
    """

    if char in {"(", ")"}:
        return True

    return False


def is_sign_of_operation(char: str) -> bool:
    """
    Является ли символ знаком операции
    :param char: str,
        проверяемый символ
    :return: bool
        True - символ является знаком
        False - символ не является знаком
    """

    if char in {"+", "-", "/", "*", "^", "l", "t", "c", "s"}:
        return True

    return False


def check_parentheses(expression: str) -> bool:
    """
    Проверка скобок выражения

    :param expression: str,
        выражение
    :return: bool,
        True - скобки расставлены верно
        False - лишние скобки или их не хватает
    """
    stack = list()

    # Исправлено с помощью тестов
    if not expression:
        return False

    for char in expression:
        if char == "(":
            stack.append(char)
        elif char == ")":
            try:
                stack.pop()
            except IndexError:
                return False

    # Исправлено с помощью тестов
    if stack:
        return False

    return True


def replace_math_func_to_char(expression: str) -> str:
    """
    Замена мат функций на их буквенные записи (log -> l)

    :param expression: str,
        вычисляемое выражение
    :return: str,
        измененное выражение
    """

    if "sin" in expression:
        expression = expression.replace("sin", "s")
    if "cos" in expression:
        expression = expression.replace("cos", "c")
    if "ln" in expression:
        expression = expression.replace("ln", "l")
    if "tan" in expression:
        expression = expression.replace("tan", "t")
    if "tg" in expression:
        expression = expression.replace("tg", "t")

    return expression


def calculation(queue_postfix_expr: list, x: float) -> float:
    """

    :param queue_postfix_expr:
    :param x:
    :return:
    """
    if not queue_postfix_expr:
        raise NoCalculation("Список пуст!")

    stack = list()

    for char_expr in queue_postfix_expr:
        if char_expr in {"+", "-", "/", "*", "^", "l", "t", "c", "s"}:
            if char_expr in {"l", "t", "c", "s"}:
                a = stack.pop()
                result = CALCULATE_OPERATION[char_expr](a)
                stack.append(result)
            else:
                b = stack.pop()
                a = stack.pop()

                result = CALCULATE_OPERATION[char_expr](a, b)

                stack.append(result)
        else:
            if char_expr == "x":
                stack.append(x)
            else:
                try:
                    stack.append(float(char_expr))
                except ValueError:
                    raise NoCalculation("Введен символ отличный от X")

    return stack.pop()


def trapezoids_method(queue: list[float], start: float, end: float, count_step: float) -> float:
    """

    :param queue:
    :param start:
    :param end:
    :param count_step:
    :return:
    """

    high_trapezoid = (end - start) / count_step
    i = 1
    square_trapezoids = 0

    while i <= count_step - 1:
        res_calc = calculation(queue, (start+i*high_trapezoid))

        square_trapezoids += res_calc
        i += 1

    result_square = high_trapezoid * ((calculation(queue, start) + calculation(queue, end)) / 2 + square_trapezoids)
    return result_square


def trapezoids_method_iteration(queue: list[float], start: float, end: float, eps: float) -> tuple[float, int]:
    """
    Расчет интеграла методом трапеций.
    :param eps:
    :param end:
    :param start:
    :type queue: object

    """

    count_step_1 = 5
    count_step_2 = 10

    while True:
        trapezoid_square_1 = trapezoids_method(queue, start, end, count_step_1)
        trapezoid_square_2 = trapezoids_method(queue, start, end, count_step_2)

        if abs(trapezoid_square_1 - trapezoid_square_2) < eps:
            break

        count_step_1, count_step_2 = count_step_2, count_step_2 * 3

    return trapezoid_square_2, count_step_2


def invoke_method(expression: str, start: int, end: int, eps: float) -> tuple[bool, float]:
    """

    :param eps:
    :param end:
    :param start:
    :param expression:
    :return:
    """
    if check_parentheses(expression):
        expression = replace_math_func_to_char(expression)
        queue_postfix_form = parse_expression_to_postfix_form(expression)

        result, count_step = trapezoids_method_iteration(queue_postfix_form, start, end, eps)

        return True, result

    return False, 0
