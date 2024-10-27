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
$ git commit -m "First program"
[master (root-commit) dea4dd0] First program
 1 file changed, 1 insertion(+)
 create mode 100644 prog.py
```

## Задача 3

Создать рядом с локальным репозиторием bare-репозиторий с именем server. Загрузить туда содержимое локального репозитория. Команда git remote -v должна выдать информацию о server! Синхронизировать coder1 с server.

Клонировать репозиторий server в отдельной папке. Задать для работы с ним произвольные данные пользователя и почты (далее – coder2). Добавить файл readme.md с описанием программы. Обновить сервер.

Coder1 получает актуальные данные с сервера. Добавляет в readme в раздел об авторах свою информацию и обновляет сервер.

Coder2 добавляет в readme в раздел об авторах свою информацию и решает вопрос с конфликтами.

Прислать список набранных команд и содержимое git log.

```
$ cd ..
$ git init --bare server.git
Initialized empty Git repository in /home/student/server.git/
$ cd my_project
$ git remote add server ../server.git
$ git remote -v
server	../server.git (fetch)
server	../server.git (push)
$ git push server master
Counting objects: 3, done.
Writing objects: 100% (3/3), 229 bytes | 0 bytes/s, done.
Total 3 (delta 0), reused 0 (delta 0)
To ../server.git
 * [new branch]      master -> master
$ cd ..
$ git clone server.git coder2_project
Cloning into 'coder2_project'...
done.
$ cd coder2_project
$ git config user.name "coder2"
$ git config user.email "coder2@google.com"
$ nano readme.md
```
> Just a new readme.
```
$ git add readme.md
$ git commit -m "Adding readme.md"
[master 3367a5f] Adding readme.md
 1 file changed, 1 insertion(+)
 create mode 100644 readme.md
$ git push origin master
Counting objects: 3, done.
Writing objects: 100% (3/3), 290 bytes | 0 bytes/s, done.
Total 3 (delta 0), reused 0 (delta 0)
To /home/student/server.git
 dea4dd0..3367a5f     master -> master
$ cd ../my_project
$ git pull server master
remote: Enumerating objects: 3, done.
remote: Counting objects: 100% (3/3), done.
remote: Total 3 (delta 0), reused 0 (delta 0)
Unpacking objects: 100% (3/3), done.
From ../server.git
 * branch            master     -> FETCH_HEAD
Updating dea4dd0..3367a5f
Fast-forward
 readme.md | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 readme.md
$ nano readme.md
```
> Author: coder1
```
$ git add readme.md
$ git commit -m "Adding new author"
[master e62fe91] Adding new author
 1 file changed, 1 insertion(+)
$ git push server master
Counting objects: 3, done.
Writing objects: 100% (3/3), 303 bytes | 0 bytes/s, done.
Total 3 (delta 0), reused 0 (delta 0)
To ../server.git
   3367a5f..e62fe91  master -> master
$ cd ../coder2_project
$ git pull origin master
Auto-merging readme.md
CONFLICT (content): Merge conflict in readme.md
Automatic merge failed; fix conflicts and then commit the result.
$ nano readme.md
```
> Author: coder2
```
$ git add readme.md
$ git commit -m "Resolve conflict and adding new author"
[master e62fe91] Resolve conflict and adding new author
$ git push origin master
Counting objects: 3, done.
Writing objects: 100% (3/3), 306 bytes | 0 bytes/s, done.
Total 3 (delta 0), reused 0 (delta 0)
To ../server.git
   e62fe91..a09244c  master -> master
$ git log
```

```
*   commit a457d748f0dab75b4c642e964172887de3ef4e3e
|\  Merge: 3367a5f  e62fe91
| | Author: Coder 2 <coder2@google.com>
| | Date:   Sun Oct 27 11:27:09 2024 +0300
| | 
| |     Resolve conflict and adding new author
| | 
| * commit d731ba84014d603384cc3287a8ea9062dbb92303
| | Author: Coder 1 <coder1@example.com>
| | Date:   Sun Oct 27 11:22:52 2024 +0300
| | 
| |     Adding new author
| | 
* | commit 48ce28336e6b3b983cbd6323500af8ec598626f1
|/  Author: Coder 2 <coder2@corp.com>
|   Date:   Sun Oct 27 11:24:00 2024 +0300
|   
|       Adding readme.md
| 
* commit ba9dfe9cb24316694808a347e8c36f8383d81bbe
| Author: Coder 1 <coder1@yandex.ru>
| Date:   Sun Oct 27 11:11:46 2024 +0300
| 
|     First program
```
