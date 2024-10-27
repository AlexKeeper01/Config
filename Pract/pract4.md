# Практическое задание №4. Системы автоматизации сборки

Работа с утилитой Make.

## Задача 1

Написать программу на Питоне, которая транслирует граф зависимостей civgraph в makefile в духе примера выше.

```
import re

with open("civgraph.txt", "r") as file:
    content = file.read()

dependency_pattern = re.compile(r"(\w+)\s*->\s*(\w+)")

dependencies = {}
all_targets = set()

for source, target in dependency_pattern.findall(content):
    source = source.lower()
    target = target.lower()
    all_targets.add(source)
    all_targets.add(target)
    
    if target in dependencies:
        dependencies[target].append(source)
    else:
        dependencies[target] = [source]

with open("Makefile", "w") as makefile:
    for target in all_targets:
        sources = dependencies.get(target, [])
        makefile.write(f"{target}: {' '.join(sources)}\n")
        makefile.write(f"\t@echo \"{target}\"\n")
    
    makefile.write("\nall: " + " ".join(all_targets) + "\n")

print("Makefile успешно создан.")
```

![image](https://github.com/user-attachments/assets/e2032348-fcf6-4db3-8092-a93e69403d7e)
