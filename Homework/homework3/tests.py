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
