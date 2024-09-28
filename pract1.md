# Практическое занятие №1. Введение, основы работы в командной строке

Научиться выполнять простые действия с файлами и каталогами в Linux из командной строки. Сравнить работу в командной строке Windows и Linux.

## Задача 1
Вывести отсортированный в алфавитном порядке список имен пользователей в файле passwd (вам понадобится grep).
```
cat /etc/passwd | cut -d ":" -f 1 | sort
```
![Результат выполнения программы 1](https://github.com/user-attachments/assets/b430df64-2154-4dd9-9ac8-7e566df01560)

## Задача 2
Вывести данные /etc/protocols в отформатированном и отсортированном порядке для 5 наибольших портов.
```
cat /etc/protocols | awk '{print $2, $1}' | sort -nr | head -n 5
```
![Результат выполнения программы 2](https://github.com/user-attachments/assets/48588bd1-1795-4e40-a34d-267ba9dcaa59)

## Задача 3
Написать программу banner средствами bash для вывода текстов, как в следующем примере (размер баннера должен меняться!)
```
#!/bin/bash
string="| "
string+=$1
string+=" |"
length=${#string}
str1="+"
for (( i=0; i < length - 2; i++ ))
do
str1+="-"
done
str1+="+"
echo $str1
echo "$string"
echo $str1
```
![Результат выполнения программы 3](https://github.com/user-attachments/assets/f7bd3d9b-e149-4590-a9d3-ac14d46ed96b)

## Задача 4
Написать программу для вывода всех идентификаторов (по правилам C/C++ или Java) в файле (без повторений).
```
#!/bin/bash
cat "$1" | tr -c "abcdefghijklmnopqrstuvwxyz" " " | xargs | tr " " "\n" | sort -u | xargs
```
![Результат выполнения программы 4](https://github.com/user-attachments/assets/dd0ef71b-7d90-483a-a584-a6e89456c6ff)

## Задача 5
Написать программу для регистрации пользовательской команды (правильные права доступа и копирование в /usr/local/bin). Например, пусть программа называется reg. В результате для banner задаются правильные права доступа и сам banner копируется в /usr/local/bin.
```
#!/bin/bash
touch "$1"
chmod +x "$1" 
cp "$1" /usr/local/bin
```
![Результат выполнения программы 5](https://github.com/user-attachments/assets/6a35d03c-4fde-45ee-9390-49bcfec3533f)


## Задача 6
Написать программу для проверки наличия комментария в первой строке файлов с расширением c, js и py.
```
#!/bin/bash
if [[ "$1" =~ \.c$|\.js$|\.py$ ]]; then
    first_line=$(head -n 1 "$1")
    if [[ "$1" =~ \.c$|\.js$ ]]; then
        if [[ "$first_line" =~ ^[[:space:]]*// ]] || [[ "$first_line" =~ ^[[:space:]]*/\* ]]; then
            echo "Комментарий найден в $1"
        else
            echo "Комментарий отсутствует в $1"
        fi
    elif [[ "$1" =~ \.py$ ]]; then
        if [[ "$first_line" =~ ^[[:space:]]*# ]]; then
            echo "Комментарий найден в $1"
        else
            echo "Комментарий отсутствует в $1"
        fi
    fi
else
    echo "Файл должен иметь расширение .c, .js или .py"
fi
```
![Результат выполнения программы 6](https://github.com/user-attachments/assets/26c07582-9dde-4169-a728-14277c0b87a3)


## Задача 7
Написать программу для нахождения файлов-дубликатов (имеющих 1 или более копий содержимого) по заданному пути (и подкаталогам).
```
#!/bin/bash
find "$1" -type f | while read -r file; do
    sha256sum "$file"
done | sort | uniq -w64 -d
```
![Результат выполнения программы 7](https://github.com/user-attachments/assets/ac01b522-cc5b-4df3-9007-858af1b5eead)


## Задача 8
Написать программу, которая находит все файлы в данном каталоге с расширением, указанным в качестве аргумента и архивирует все эти файлы в архив tar.
```
#!/bin/bash
dir="$1"
ext="$2"
archive="archive.tar"
find "$dir" -type f -name "*$ext" | tar -cf "$archive" -T -
```
![Результат выполнения программы 8](https://github.com/user-attachments/assets/ea82722a-37b2-47c2-a8d1-89d745faa5d5)

![Результат выполнения программы 8](https://github.com/user-attachments/assets/2e806201-d936-4111-8f9c-8cd7872a0a3f)

![Результат выполнения программы 8](https://github.com/user-attachments/assets/3715f57a-92f9-4f6b-a411-98c8fa675269)


## Задача 9
Написать программу, которая заменяет в файле последовательности из 4 пробелов на символ табуляции. Входной и выходной файлы задаются аргументами.
```
#!/bin/bash
sed 's/    /\t/g' "$1" > "$2"
```
![Результат выполнения программы 9](https://github.com/user-attachments/assets/e9f09d14-5f5a-432f-b684-d012a013646c)

![Результат выполнения программы 9](https://github.com/user-attachments/assets/45312c59-2613-4125-a758-6434df5e4345)

![Результат выполнения программы 9](https://github.com/user-attachments/assets/805c5f79-d50d-46a9-8d9f-cbeabd1aa535)

## Задача 10
Написать программу, которая выводит названия всех пустых текстовых файлов в указанной директории. Директория передается в программу параметром.
```
#!/bin/bash
find "$1" -type f -name "*.txt" -exec test ! -s {} \; -print
```
![Результат выполнения программы 10](https://github.com/user-attachments/assets/8e1cc87a-3184-442d-b550-b93cb2e21b4b)
