# config.json

```
{
  "graph_tool_path": "C:/Users/aleks/AppData/Roaming/npm/mmdc.cmd",
  "package_url": "https://www.nuget.org/api/v2/package",
  "package_name": "Dapper",
  "output_path": "./graphs/dependency_graph.svg"
}
```

# graph_generator.py

```
def generate_mermaid_graph(dependencies):
    mermaid_graph = "graph TD\n"

    for package, deps in dependencies.items():
        for dep_info in deps:
            dep_name = dep_info["name"]
            dep_version = dep_info["version"]

            dep_string = f"    {package} --> {dep_name}_{dep_version}"
            mermaid_graph += dep_string + "\n"

    return mermaid_graph
```

# main.py

```
import json
from graph_generator import generate_mermaid_graph
from nupkg_parser import parse_dependencies
from visualizer import save_graph_to_png


def main(config_path="config.json"):
    with open(config_path, 'r') as file:
        config = json.load(file)

    dependencies = parse_dependencies(config["package_name"], config["package_url"], None, )
    mermaid_graph = generate_mermaid_graph(dependencies)
    save_graph_to_png(mermaid_graph, config["output_path"], config["graph_tool_path"])

    print("Граф зависимостей успешно сохранен в", config["output_path"])


if __name__ == "__main__":
    main()
```

# nupkg_parser.py

```
import requests
import zipfile
import io
import xml.etree.ElementTree as ET

def parse_dependencies(package_name, package_url, visited=None, package_version="unknown", temp=0):
    if visited is None:
        visited = set()

    if temp == 0:
        package_key = f"{package_name}"
    else:
        package_key = f"{package_name}_{package_version}"
    if package_key in visited:
        print(f"[DEBUG] Пакет {package_name} версии {package_version} уже обработан. Пропускаем.")
        return {}

    print(f"[DEBUG] Обрабатываем пакет: {package_name} версии {package_version}")
    visited.add(package_key)

    all_dependencies = {}

    try:
        print(f"[DEBUG] Загружаем пакет {package_name} с URL: {package_url}/{package_name}")
        response = requests.get(f"{package_url}/{package_name}")
        response.raise_for_status()

        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            print(f"[DEBUG] Успешно открыт архив пакета {package_name}")
            for file in z.namelist():
                if file.endswith(".nuspec"):
                    print(f"[DEBUG] Найден файл .nuspec: {file}")
                    with z.open(file) as nuspec:
                        tree = ET.parse(nuspec)
                        root = tree.getroot()

                        dependencies = []
                        for group in root.findall(".//ns0:metadata/ns0:dependencies/ns0:group", namespaces={
                            'ns0': 'http://schemas.microsoft.com/packaging/2013/05/nuspec.xsd'}):
                            for dep in group.findall(".//ns0:dependency", namespaces={
                                'ns0': 'http://schemas.microsoft.com/packaging/2013/05/nuspec.xsd'}):
                                dep_name = dep.attrib.get("id")
                                dep_version = dep.attrib.get("version", "unknown")

                                if dep_name:
                                    print(f"[DEBUG] Найдена зависимость: {dep_name}, версия: {dep_version}")
                                    dependency_info = {"name": dep_name, "version": dep_version}
                                    if dependency_info not in dependencies:
                                        dependencies.append(dependency_info)

                        all_dependencies[f"{package_key}"] = dependencies

                        for dep in dependencies:
                            dep_name = dep["name"]
                            dep_version = dep["version"]
                            transitive_dependencies = parse_dependencies(dep_name, package_url, visited, dep_version, 1)
                            for trans_package, trans_deps in transitive_dependencies.items():
                                if trans_package not in all_dependencies:
                                    all_dependencies[trans_package] = trans_deps
                                else:
                                    for trans_dep in trans_deps:
                                        if trans_dep not in all_dependencies[trans_package]:
                                            all_dependencies[trans_package].append(trans_dep)
    except requests.RequestException as e:
        print(f"Ошибка при загрузке пакета {package_name}: {e}")
    except zipfile.BadZipFile:
        print(f"Файл {package_name}.nupkg повреждён или не является архивом.")

    print(f"[DEBUG] Завершена обработка пакета: {package_name} версии {package_version}")
    print(all_dependencies)
    return all_dependencies
```

# visualizer.py

```
import subprocess


def save_graph_to_png(mermaid_graph, output_path, graph_tool_path):
    temp_file = "temp_graph.mmd"

    with open(temp_file, "w") as file:
        file.write(mermaid_graph)

    command = [graph_tool_path, "-i", temp_file, "-o", output_path, "--theme", "forest"]

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError("Ошибка при визуализации графа.")
```
