# Практическое занятие №2. Менеджеры пакетов

Разобраться, что представляет собой менеджер пакетов, как устроен пакет, как читать версии стандарта semver. Привести примеры программ, в которых имеется встроенный пакетный менеджер.

## Задача 1

Вывести служебную информацию о пакете matplotlib (Python). Разобрать основные элементы содержимого файла со служебной информацией из пакета. Как получить пакет без менеджера пакетов, прямо из репозитория?

### C менеджером пакетов

```
pip show matplotlib
```

![image](https://github.com/user-attachments/assets/b3792aa5-750a-4633-9c8c-9bc25980987c)

### Без менеджера пакетов

```
git clone https://github.com/matplotlib/matplotlib.git
```
```
cd matplotlib
```
```
pip install -r requirements.txt
```
```
python setup.py install
```

## Задача 2

Вывести служебную информацию о пакете express (JavaScript). Разобрать основные элементы содержимого файла со служебной информацией из пакета. Как получить пакет без менеджера пакетов, прямо из репозитория?

### C менеджером пакетов

```
npm show express
```

![image](https://github.com/user-attachments/assets/3cd2ed73-0495-4b50-af14-4991c7cbcc20)


### Без менеджера пакетов

```
git clone https://github.com/expressjs/express.git
```
```
cd express
```
```
npm install
```
```
npm link
```

## Задача 3

Сформировать graphviz-код и получить изображения зависимостей matplotlib и express.

### Зависимости для matplotlib (Python)

```
digraph G {
    "matplotlib" -> "numpy";
    "matplotlib" -> "pyparsing";
    "matplotlib" -> "cycler";
    "matplotlib" -> "pillow";
    "matplotlib" -> "kiwisolver";
    "matplotlib" -> "python-dateutil";

    "cycler" -> "six";
    "python-dateutil" -> "six";
}
```

![graph](https://github.com/user-attachments/assets/9a4919df-eb9f-4296-81a0-479ff4ab2ba9)

### Зависимости для express (JavaScript)

```
digraph G {
    "express" -> "accepts";
    "express" -> "array-flatten";
    "express" -> "body-parser";
    "express" -> "content-disposition";
    "express" -> "content-type";
    "express" -> "cookie";
    "express" -> "cookie-signature";
    "express" -> "debug";
    "express" -> "depd";
    "express" -> "encodeurl";
    "express" -> "escape-html";
    "express" -> "etag";
    "express" -> "finalhandler";
    "express" -> "fresh";
    "express" -> "merge-descriptors";
    "express" -> "methods";
    "express" -> "on-finished";
    "express" -> "parseurl";
    "express" -> "path-to-regexp";
    "express" -> "proxy-addr";
    "express" -> "qs";
    "express" -> "range-parser";
    "express" -> "safe-buffer";
    "express" -> "send";
    "express" -> "serve-static";
    "express" -> "setprototypeof";
    "express" -> "statuses";
    "express" -> "type-is";
    "express" -> "utils-merge";
    "express" -> "vary";

    "accepts" -> "mime-types";
    "accepts" -> "negotiator";
    "body-parser" -> "bytes";
    "body-parser" -> "http-errors";
    "body-parser" -> "iconv-lite";
    "body-parser" -> "on-finished";
    "body-parser" -> "qs";
    "body-parser" -> "raw-body";
}
```

![graph (1)](https://github.com/user-attachments/assets/f64a0da3-f60d-48eb-b97c-d188973059cd)

## Задача 4

Изучить основы программирования в ограничениях. Установить MiniZinc, разобраться с основами его синтаксиса и работы в IDE.

Решить на MiniZinc задачу о счастливых билетах. Добавить ограничение на то, что все цифры билета должны быть различными (подсказка: используйте all_different). Найти минимальное решение для суммы 3 цифр.

```
include "globals.mzn";

var 0..9: d1;
var 0..9: d2;
var 0..9: d3;
var 0..9: d4;
var 0..9: d5;
var 0..9: d6;

constraint all_different([d1, d2, d3, d4, d5, d6]);
constraint d1 + d2 + d3 = d4 + d5 + d6;
solve minimize (d1 + d2 + d3);
output ["Digits: \(d1), \(d2), \(d3), \(d4), \(d5), \(d6)\n"];
```

## Задача 5

Решить на MiniZinc задачу о зависимостях пакетов для рисунка, приведенного ниже.

![pubgrub](https://github.com/user-attachments/assets/99f96aca-9308-4396-967f-2d2416c47663)

```
set of int: MenuVersion = {100, 110, 120, 130, 150};
set of int: DropdownVersion = {180, 200, 210, 220, 230};
set of int: IconsVersion = {100, 200};

var MenuVersion: menu;
var DropdownVersion: dropdown;
var IconsVersion: icons;

constraint if menu >= 110 then dropdown >= 200 else dropdown = 180 endif;
constraint if dropdown <= 200 /\ dropdown > 180 then icons = 200 else icons = 100 endif;
solve satisfy;
output ["Выбранные версии пакетов: ", show(menu), ", ", show(dropdown), ", ", show(icons), "\n"];
```

![image](https://github.com/user-attachments/assets/f0ac3457-b322-42db-819b-2754164d0dcc)

## Задача 6

Решить на MiniZinc задачу о зависимостях пакетов для следующих данных:

```
root 1.0.0 зависит от foo ^1.0.0 и target ^2.0.0.
foo 1.1.0 зависит от left ^1.0.0 и right ^1.0.0.
foo 1.0.0 не имеет зависимостей.
left 1.0.0 зависит от shared >=1.0.0.
right 1.0.0 зависит от shared <2.0.0.
shared 2.0.0 не имеет зависимостей.
shared 1.0.0 зависит от target ^1.0.0.
target 2.0.0 и 1.0.0 не имеют зависимостей.
```

```
set of int: PackageVersionRoot = {100};   % root 1.0.0
set of int: PackageVersionFoo = {110, 100}; % foo 1.1.0, foo 1.0.0
set of int: PackageVersionLeft = {000, 100};    % left 1.0.0
set of int: PackageVersionRight = {000, 100};   % right 1.0.0
set of int: PackageVersionShared = {000, 100, 200}; % shared 1.0.0, shared 2.0.0
set of int: PackageVersionTarget = {200, 100}; % target 2.0.0, target 1.0.0

var PackageVersionRoot: root;
var PackageVersionFoo: foo;
var PackageVersionLeft: left;
var PackageVersionRight: right;
var PackageVersionShared: shared;
var PackageVersionTarget: target;

constraint
    (foo >= 100) /\ (target >= 200) /\
    (if foo = 110 then left >= 100 /\ right >= 100 else true endif) /\
    (if foo = 100 then left = 000 /\ right = 000 else true endif) /\
    (if left = 100 then shared >= 100 else true endif) /\
    (if right = 100 then shared < 200 else true endif) /\
    (if shared = 100 then target >= 100 else true endif);

solve satisfy;
output [
    "root: ", show(root), "\n",
    "foo: ", show(foo), "\n",
    "left: ", show(left), "\n",
    "right: ", show(right), "\n",
    "shared: ", show(shared), "\n",
    "target: ", show(target), "\n"
];
```

![image](https://github.com/user-attachments/assets/cc6ee6dc-d2f5-4237-815b-edc99338dc5d)
