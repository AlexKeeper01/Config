# input.json

```
{
    "dict1": {
        "a": 10,
        "b": 20,
        "c": "^(+ a b)"
    },
    "dict3": {
        "sum": "^(+ c b)",
        "difference": "^(- sum a)"
    },
    "dict2": {
        "x": 5,
        "y": 15
    }
}
```

# main.py

```
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
```

# tests.py

```
import pytest
import json
from main import translate

# --- Тесты для корректного ввода ---

def test_translate_simple_numbers():
    json_input = json.dumps({"a": 5, "b": 3})
    expected_output = "var a 5.00;\nvar b 3.00;"
    assert translate(json_input) == expected_output


def test_translate_simple_operation():
    json_input = json.dumps({"c": "^(+ 2 3)"})
    expected_output = "var c 5.00;"
    assert translate(json_input) == expected_output


def test_translate_with_variables():
    json_input = json.dumps({"a": 2, "b": 3, "c": "^(+ a b)"})
    expected_output = "var a 2.00;\nvar b 3.00;\nvar c 5.00;"
    assert translate(json_input) == expected_output


def test_translate_nested_structure():
    json_input = json.dumps({"nested": {"x": 1, "y": "^(+ x 4)"}})
    expected_output = "var nested {\n\tvar x 1.00;\n\tvar y 5.00;\n};"
    assert translate(json_input) == expected_output


# --- Тесты для ошибок ввода ---

def test_translate_invalid_identifier():
    json_input = json.dumps({"1invalid": 2})
    with pytest.raises(ValueError, match="Недопустимое имя переменной: 1invalid"):
        translate(json_input)


def test_translate_unknown_operation():
    json_input = json.dumps({"a": 5, "b": "^(unknown 2 3)"})
    with pytest.raises(ValueError, match="Неизвестная операция: unknown"):
        translate(json_input)


def test_translate_undefined_variable():
    json_input = json.dumps({"a": "^(+ b 3)"})
    with pytest.raises(ValueError, match="Необъявленный идентификатор 'b'"):
        translate(json_input)


# --- Тесты для некорректного JSON ---

def test_translate_invalid_json():
    invalid_json = "{invalid_json}"
    with pytest.raises(SystemExit):
        translate(invalid_json)


def test_translate_non_dict_input():
    non_dict_json = json.dumps(["not", "a", "dict"])
    with pytest.raises(ValueError, match="Входной JSON должен быть объектом"):
        translate(non_dict_json)


def test_translate_invalid_value():
    invalid_value_json = json.dumps({"a": ["invalid", "value"]})
    with pytest.raises(ValueError, match="Недопустимое значение для a"):
        translate(invalid_value_json)
```
