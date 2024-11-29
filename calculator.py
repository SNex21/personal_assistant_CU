import re


def validate_expression(expression):
    if not re.fullmatch(r'[0-9+\-*/(). ]+', expression):
        raise ValueError('недопустимые символы')


def calculator():
    print('Калькулятор')
    print('Введите арифметическое выражение  или "выход" для возврата в меню')

    while True:
        expression = input('Введите выражение:').strip()

        if expression.lower() == 'выход':
            print('Возвращение в главное меню')
            break

        try:
            validate_expression(expression)

            result = eval(expression)
            print(f'{result}')
        except ZeroDivisionError:
            print('Ошибка - Деление на ноль')
        except ValueError as e:
            print(f'Ошибка - {e}')
        except Exception as e:
            print(f'Некорректное выражение ({e})')
