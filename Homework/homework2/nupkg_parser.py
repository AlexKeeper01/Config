import zipfile
import xml.etree.ElementTree as ET
import os


def parse_dependencies(package_name, path_to_package):
    package_path = f"{path_to_package}{package_name}"

    if not os.path.exists(package_path):
        raise FileNotFoundError(f"{package_name}")

    dependencies = {}

    # Открываем nupkg файл как архив
    with zipfile.ZipFile(package_path, 'r') as z:
        # Проходим по файлам внутри архива
        for file in z.namelist():
            # Ищем .nuspec файл
            if file.endswith(".nuspec"):
                with z.open(file) as nuspec:
                    # Парсим .nuspec файл
                    tree = ET.parse(nuspec)
                    root = tree.getroot()

                    # Ищем все зависимости внутри тега <dependencies>
                    for group in root.findall(".//ns0:metadata/ns0:dependencies/ns0:group", namespaces={
                        'ns0': 'http://schemas.microsoft.com/packaging/2013/05/nuspec.xsd'}):
                        # Внутри группы ищем зависимости
                        for dep in group.findall(".//ns0:dependency", namespaces={
                            'ns0': 'http://schemas.microsoft.com/packaging/2013/05/nuspec.xsd'}):
                            dep_name = dep.attrib.get("id")
                            dep_version = dep.attrib.get("version")

                            # Добавляем зависимость с версией, если её ещё нет
                            if dep_name:
                                dep_info = {"name": dep_name, "version": dep_version}

                                # Используем set для исключения дубликатов
                                dependencies.setdefault(package_name, set()).add(f"{dep_name}_{dep_version}")

    # Преобразуем set обратно в список для дальнейшего использования
    for package, deps in dependencies.items():
        dependencies[package] = [{"name": dep.split("_")[0], "version": dep.split("_")[1]} for dep in deps]

    return dependencies
