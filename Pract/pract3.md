# Практическое занятие №3. Конфигурационные языки

Разобраться, что собой представляют программируемые конфигурационные языки (Jsonnet, Dhall, CUE).

## Задача 1

Реализовать на Jsonnet приведенный ниже пример в формате JSON. Использовать в реализации свойство программируемости и принцип DRY.

```Jsonnet
local groupPrefix = "ИКБО-";
local groupSuffix = "-20";

local generateGroups(start, end) = [
  groupPrefix + std.toString(i) + groupSuffix
  for i in std.range(start, end)
];

{
  groups: generateGroups(1, 24),
  students: [
    {
      age: 19,
      group: "ИКБО-4-20",
      name: "Иванов И.И."
    },
    {
      age: 18,
      group: "ИКБО-5-20",
      name: "Петров П.П."
    },
    {
      age: 18,
      group: "ИКБО-5-20",
      name: "Сидоров С.С."
    },
    {
      age: 18,
      group: "ИКБО-23-20",
      name: "Попов А.В."
    }
  ],
  subject: "Конфигурационное управление"
}
```

Вывод:

```JSON
{
   "groups": [
      "ИКБО-1-20",
      "ИКБО-2-20",
      "ИКБО-3-20",
      "ИКБО-4-20",
      "ИКБО-5-20",
      "ИКБО-6-20",
      "ИКБО-7-20",
      "ИКБО-8-20",
      "ИКБО-9-20",
      "ИКБО-10-20",
      "ИКБО-11-20",
      "ИКБО-12-20",
      "ИКБО-13-20",
      "ИКБО-14-20",
      "ИКБО-15-20",
      "ИКБО-16-20",
      "ИКБО-17-20",
      "ИКБО-18-20",
      "ИКБО-19-20",
      "ИКБО-20-20",
      "ИКБО-21-20",
      "ИКБО-22-20",
      "ИКБО-23-20",
      "ИКБО-24-20"
   ],
   "students": [
      {
         "age": 19,
         "group": "ИКБО-4-20",
         "name": "Иванов И.И."
      },
      {
         "age": 18,
         "group": "ИКБО-5-20",
         "name": "Петров П.П."
      },
      {
         "age": 18,
         "group": "ИКБО-5-20",
         "name": "Сидоров С.С."
      },
      {
         "age": 18,
         "group": "ИКБО-23-20",
         "name": "Попов А.В."
      }
   ],
   "subject": "Конфигурационное управление"
}
```

## Задача 2

Реализовать на Dhall приведенный ниже пример в формате JSON. Использовать в реализации свойство программируемости и принцип DRY.

```Dhall
let generateGroup : Natural → Text
= λ(i : Natural) → "ИКБО-" ++ Text/show i ++ "-20"

let groups : List Text
= List/generate 24 generateGroup

let Student
    : Type
= { age : Natural, group : Text, name : Text }

let students : List Student
= [ { age = 19, group = "ИКБО-4-20", name = "Иванов И.И." }
  , { age = 18, group = "ИКБО-5-20", name = "Петров П.П." }
  , { age = 18, group = "ИКБО-5-20", name = "Сидоров С.С." }
  , { age = 20, group = "ИКБО-6-20", name = "Новиков Н.Н." }
  ]

let config
    : { groups : List Text, students : List Student, subject : Text }
= { groups = groups
  , students = students
  , subject = "Конфигурационное управление"
  }

in  config
```

## Задача 3

Для решения дальнейших задач потребуется программа на Питоне, представленная ниже. Разбираться в самом языке Питон при этом необязательно.

> Код пришлось изменить, так как он не работал должным образом.

```Python
import random

def parse_bnf(text):
    grammar = {}
    # Разделяем входной текст на строки и обрабатываем каждую строку
    rules = [line.strip() for line in text.strip().split('\n') if line.strip()]
    for rule in rules:
        # Разделяем правило на имя и тело
        name, body = rule.split('=')
        name = name.strip()  # Убираем лишние пробелы в имени
        # Разделяем тело на альтернативы, убирая пробелы
        alternatives = [alt.strip().split() for alt in body.split('|')]
        grammar[name] = alternatives  # Записываем в словарь

    return grammar

def generate_phrase(grammar, start, depth=0, max_depth=3):
    if depth > max_depth:
        return ''  # Возвращаем пустую строку, если превышена максимальная глубина

    if start in grammar:
        # Выбираем случайное правило для данного нетерминала
        seq = random.choice(grammar[start])
        # Рекурсивно генерируем строку для каждого элемента последовательности без пробелов
        return ''.join([generate_phrase(grammar, name, depth + 1, max_depth) for name in seq])
    
    return str(start)  # Если это терминал, просто возвращаем его

# Обновленная БНФ для укороченных выражений алгебры логики
bnf_text = '''

'''

# Преобразуем БНФ в словарь
grammar_dict = parse_bnf(bnf_text)

# Генерация нескольких коротких фраз
num_phrases = 10  # Количество строк для генерации
for i in range(num_phrases):
    print(generate_phrase(grammar_dict, 'E', max_depth=10))  # Вызываем с ограничением глубины


```

Реализовать грамматики, описывающие следующие языки (для каждого решения привести БНФ). Код решения должен содержаться в переменной bnf_text.

Язык нулей и единиц.

```
10
100
11
101101
000
```

```Python
bnf_text = '''
E = 0 E | 1 E | 1 | 0
'''
```

Пример вывода:

```
110
0
11
11101
011
010
00
01
0
001
```

## Задача 4

Язык правильно расставленных скобок двух видов.

```
(({((()))}))
{}
{()}
()
{}
```

```Python
bnf_text = '''
E = ε | ( E ) | { E }
'''
```

> ε - пустая строка

Пример вывода:

```
ε
({{ε}})
ε
ε
{(((ε)))}
{{ε}}
{ε}
{ε}
({({(ε)})})
ε
```

## Задача 5

Язык выражений алгебры логики.

```
((~(y & x)) | (y) & ~x | ~x) & x
y & ~(y)
(~(y) & y & ~y)
~x
~((x) & y | (y) | (x)) & x | x | (y & ~y)
```

```Python
bnf_text = '''
E = L
L = A / ~ A / S / A T L / A T S
S = ( L )
T = | / &
A = x / y
'''
```

Пример вывода:

```
x|(x|(y&x))
~x
y&y
x&(y|(x))
(y|x|((~y)))
(~x)
x
x|(y)
~x
x|(x&x|(x))
```
