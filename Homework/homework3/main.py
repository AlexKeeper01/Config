import operator
import math
import json
import sys


# Операции для вычислений
OPERATIONS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "sqrt": math.sqrt,
}

def translate(json_input, context=None, indent_level=0): # Рекурсивная функция учитывающуя вложенность конфигурационного языка
    if context is None:
        context = {}

    indent = "\t" * indent_level  # Добавляем нужное количество табуляций для текущего уровня вложенности

    try:
        data = json.loads(json_input)

        # Проверяем тип данных (должен быть словарь)
        if not isinstance(data, dict):
            raise ValueError("Входной JSON должен быть объектом (словарём).")

        # Перевод в конфигурационный язык
        config_lines = []
        for key, value in data.items():
            # Проверка имени (допустимые символы: a-z, A-Z, 0-9, _)
            if not isinstance(key, str) or not key.isidentifier():
                raise ValueError(f"Недопустимое имя переменной: {key}")

            if isinstance(value, (int, float)):  # Числа
                value = float(value)  # Преобразуем все числа в float
                config_lines.append(f"{indent}var {key} {value:.2f};")  # Ограничиваем до 2 знаков после запятой
                context[key] = value

            elif isinstance(value, str) and value.startswith("^("):  # Префиксные выражения
                expr_content = value[2:-1].strip()  # Убираем "^(" и ")"
                parts = expr_content.split()
                operation = parts[0]
                operands = []

                for op in parts[1:]:
                    # Проверка, является ли операнд переменной
                    if op in context:
                        operands.append(context[op])  # Используем ранее объявленную переменную
                    else:
                        try:
                            operands.append(float(op))  # Преобразуем в число
                        except ValueError:  # Если не можем преобразовать в float, значит переменная не объявлена
                            raise ValueError(f"Необъявленный идентификатор '{op}'")

                # Выполнение операции
                if operation not in OPERATIONS:
                    raise ValueError(f"Неизвестная операция: {operation}")

                func = OPERATIONS[operation]
                computed_value = func(*operands) if len(operands) > 1 else func(operands[0])
                computed_value = float(computed_value)

                config_lines.append(
                    f"{indent}var {key} {computed_value:.2f};")
                context[key] = computed_value

            elif isinstance(value, dict):  # Словари (рекурсивная обработка)
                nested_lines = translate(json.dumps(value), context, indent_level + 1)
                config_lines.append(f"{indent}var {key} {{\n{nested_lines}\n{indent}}};")

            else:
                raise ValueError(f"Недопустимое значение для {key}: {value}")

        return "\n".join(config_lines)

    except json.JSONDecodeError:
        print("Ошибка: Некорректный JSON.")
        sys.exit(1)
    except ValueError as e:
        raise ValueError(f"{e}")


# Чтение данных из input.json
try:
    with open('input.json', 'r') as input_file:
        json_data = input_file.read()
        result = translate(json_data)
        print(result)

except FileNotFoundError:
    print("Файл input.json не найден.")
except Exception as e:
    print(f"Ошибка при обработке файла: {e}")
