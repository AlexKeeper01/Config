# Практическое занятие №5. Вопросы виртуализации

## Задача 1

Исследование виртуальной стековой машины CPython.

Изучите возможности просмотра байткода ВМ CPython.

```
import dis

def foo(x):
    while x:
        x -= 1
    return x + 1

print(dis.dis(foo))
```

Этот код анализирует байткод функции foo и выводит его.

Байткод для функции `foo`:

```
  2           0 LOAD_FAST                0 (x)      # Загружаем значение x.
              2 POP_JUMP_IF_FALSE       18          # Если x == False (0), переходим на инструкцию 18.

  3     >>    4 LOAD_FAST                0 (x)      # Загружаем x.
              6 LOAD_CONST               1 (1)      # Загружаем константу 1.
              8 INPLACE_SUBTRACT                    # Выполняем x -= 1.
             10 STORE_FAST               0 (x)      # Сохраняем результат в x.
             12 JUMP_ABSOLUTE            0          # Возвращаемся на начало цикла.

  4     >>   18 LOAD_FAST                0 (x)      # Загружаем x.
             20 LOAD_CONST               1 (1)      # Загружаем константу 1.
             22 BINARY_ADD                          # Складываем x и 1.
             24 RETURN_VALUE                        # Возвращаем результат.
```

Опишите по шагам, что делает каждая из следующих команд (приведите эквивалентное выражение на Python):

```
 11           0 LOAD_FAST                0 (x)
              2 LOAD_CONST               1 (10)
              4 BINARY_MULTIPLY
              6 LOAD_CONST               2 (42)
              8 BINARY_ADD
             10 RETURN_VALUE
```

Эквивалентно

```
result = x * 10 + 42
return result
```

```
 11           0 LOAD_FAST                0 (x)      # Загружаем переменную `x` (локальную).
              2 LOAD_CONST               1 (10)     # Загружаем константу `10`.
              4 BINARY_MULTIPLY                     # Умножаем значение переменной `x` на `10`.
              6 LOAD_CONST               2 (42)     # Загружаем константу `42`.
              8 BINARY_ADD                          # Складываем результат умножения и `42`.
             10 RETURN_VALUE                        # Возвращаем результат вычислений.
```

## Задача 2

Что делает следующий байткод (опишите шаги его работы)? Это известная функция, назовите ее.

```
  5           0 LOAD_CONST               1 (1)
              2 STORE_FAST               1 (r)

  6     >>    4 LOAD_FAST                0 (n)
              6 LOAD_CONST               1 (1)
              8 COMPARE_OP               4 (>)
             10 POP_JUMP_IF_FALSE       30

  7          12 LOAD_FAST                1 (r)
             14 LOAD_FAST                0 (n)
             16 INPLACE_MULTIPLY
             18 STORE_FAST               1 (r)

  8          20 LOAD_FAST                0 (n)
             22 LOAD_CONST               1 (1)
             24 INPLACE_SUBTRACT
             26 STORE_FAST               0 (n)
             28 JUMP_ABSOLUTE            4

  9     >>   30 LOAD_FAST                1 (r)
             32 RETURN_VALUE
```

Это функция нахождения факториала числа `n`.

```
  5           0 LOAD_CONST               1 (1)       # Загружаем константу `1`.
              2 STORE_FAST               1 (r)       # Сохраняем ее в локальную переменную `r` (результат).

  6     >>    4 LOAD_FAST                0 (n)       # Загружаем значение `n`.
              6 LOAD_CONST               1 (1)       # Загружаем константу `1`.
              8 COMPARE_OP               4 (>)       # Проверяем, больше ли `n` 1.
             10 POP_JUMP_IF_FALSE       30           # Если нет, переходим к завершению цикла.

  7          12 LOAD_FAST                1 (r)       # Загружаем текущее значение `r`.
             14 LOAD_FAST                0 (n)       # Загружаем текущее значение `n`.
             16 INPLACE_MULTIPLY                     # Умножаем `r` на `n`.
             18 STORE_FAST               1 (r)       # Сохраняем результат обратно в `r`.

  8          20 LOAD_FAST                0 (n)       # Загружаем текущее значение `n`.
             22 LOAD_CONST               1 (1)       # Загружаем константу `1`.
             24 INPLACE_SUBTRACT                     # Вычитаем `1` из `n`.
             26 STORE_FAST               0 (n)       # Сохраняем результат обратно в `n`.
             28 JUMP_ABSOLUTE            4           # Переходим к началу цикла.

  9     >>   30 LOAD_FAST                1 (r)       # Загружаем результат `r`.
             32 RETURN_VALUE                         # Возвращаем результат.
```

## Задача 3

Приведите результаты из задач 1 и 2 для виртуальной машины JVM (Java) или .Net (C#).

```
 0: bipush        10         # Загружаем значение 10 (x).
 2: istore_1                  # Сохраняем его в локальную переменную `x`.
 3: iload_1                   # Загружаем значение `x`.
 4: bipush        10          # Загружаем значение 10.
 6: imul                      # Умножаем `x` на 10.
 7: bipush        42          # Загружаем значение 42.
 9: iadd                      # Складываем результат умножения и 42.
10: ireturn                   # Возвращаем результат.
```

```
  0: iconst_1                  # Загружаем константу `1`.
  1: istore_1                  # Сохраняем ее в локальной переменной `r`.

  2: iload_0                   # Загружаем значение `n`.
  3: iconst_1                  # Загружаем константу `1`.
  4: if_icmple     18          # Если `n <= 1`, переходим к завершению.

  5: iload_1                   # Загружаем текущее значение `r`.
  6: iload_0                   # Загружаем текущее значение `n`.
  7: imul                      # Умножаем `r` на `n`.
  8: istore_1                  # Сохраняем результат в `r`.

  9: iload_0                   # Загружаем текущее значение `n`.
 10: iconst_1                  # Загружаем константу `1`.
 11: isub                      # Вычитаем `1` из `n`.
 12: istore_0                  # Сохраняем результат в `n`.
 13: goto          2           # Переход к началу цикла.

 18: iload_1                   # Загружаем значение `r`.
 19: ireturn                   # Возвращаем результат.
```
