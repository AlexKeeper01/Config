# Практическое задание №4. Системы контроля версий

Работа с Git.

## Задача 1

С помощью команд эмулятора git получить следующее состояние проекта. Прислать свою картинку.

```
git commit
git tag in
git branch first
git branch second
git commit
git checkout first
git commit
git checkout second
git commit
git commit
git checkout first
git commit
git checkout master
git commit
git merge first
git checkout second
git rebase master
git checkout master
git merge second
git checkout 0e7469f
```

![image](https://github.com/user-attachments/assets/7d579bc6-6c1c-4179-a7ea-a5fe35198ea9)

## Задача 2

Создать локальный git-репозиторий. Задать свои имя и почту (далее – coder1). Разместить файл prog.py с какими-нибудь данными. Прислать в текстовом виде диалог с git.

```
$ mkdir my_project
$ cd my_project
$ git init
Initialized empty Git repository in /home/student/my_project/.git/
$ git config user.name "coder1"
$ git config user.email "coder1@yandex.ru"
nano prog.py
```
> print("Hellow, world!")
```
$ git status
On branch master

Initial commit

Untracked files:
  (use "git add <file>..." to include in what will be committed)
    prog.py

nothing added to commit but untracked files present (use "git add" to track)
$ git add prog.py
$ git status
On branch master

Initial commit

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
    new file:   prog.py
$ git commit -m "First program."
[master (root-commit) dea4dd0] First program.
 1 file changed, 1 insertion(+)
 create mode 100644 prog.py
```
