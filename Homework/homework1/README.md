# Задание №1

Разработать эмулятор для языка оболочки ОС. Необходимо сделать работу
эмулятора как можно более похожей на сеанс shell в UNIX-подобной ОС.
Эмулятор должен запускаться из реальной командной строки, а файл с
виртуальной файловой системой не нужно распаковывать у пользователя.
Эмулятор принимает образ виртуальной файловой системы в виде файла формата
tar. Эмулятор должен работать в режиме GUI.

**Ключами командной строки задаются:**

• Имя пользователя для показа в приглашении к вводу.

• Имя компьютера для показа в приглашении к вводу.

• Путь к архиву виртуальной файловой системы.

• Путь к стартовому скрипту.

Стартовый скрипт служит для начального выполнения заданного списка
команд из файла.

**Необходимо поддержать в эмуляторе команды ls, cd и exit, а также
следующие команды:**

1. wc.

2. history.

3. du.
   
Все функции эмулятора должны быть покрыты тестами, а для каждой из
поддерживаемых команд необходимо написать 3 теста.

## 1. Запуск программы

```
//start <URL репозитория>\shell.exe aleks ELBRUS <URL репозитория>\Virtual_File_System.tar <URL репозитория>\script.txt
```

## 2. Структура проекта

```
shell.cpp                 # Основной код
script.txt                # Файл со скриптом
Virtual_File_System.tar   # Архив с виртуальной фаловой системой
```

## Результаты тестирования

![image](https://github.com/user-attachments/assets/101b3125-5122-426d-b152-c56b66cae669)

![image](https://github.com/user-attachments/assets/b092044d-72f3-4759-9aba-46b2a0ea21ba)

![image](https://github.com/user-attachments/assets/ce628f4b-52af-406c-a8d2-aa4ba4dff202)

![image](https://github.com/user-attachments/assets/05b1984d-9608-4b65-bfea-98091ce4c395)

## Виртуальная вайловая система

![image](https://github.com/user-attachments/assets/b29a991f-3d83-46f6-bb31-897504273a19)

## Скрипт

![image](https://github.com/user-attachments/assets/37f9a15a-6b08-4c83-94fa-6fcae98c22c7)
