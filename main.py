from trapezoid_procedure import invoke_method, calculation


def main():
    """
    Запуск программы.
    :return: None
    """

    expression = input("Введите подинтегральную функцию: ")
    start_end = input("Введите начало и конец отрезка интеграла (через пробел):  ")
    eps = input("Введите точность вычисления интеграла (через точку, пример 0.1): ")

    try:
        start, end = map(int, start_end) if start_end.strip() else 1, 2
        eps = 0.1 if not eps.strip() else float(eps)

        result, integral = invoke_method(expression, start, end, eps)

        if result:
            print("Значение интеграла = ", integral)
        else:
            print("Неверное количество скобок!")

    except ValueError:
        print("Начало, конец отрезка и точность должны быть числами!")


if __name__ == "__main__":
    main()
