from graph_generator import generate_mermaid_graph

def test_generate_mermaid_graph_single_dependency():
    # Тест с одной зависимостью
    package_name = "PackageA"
    dependencies = {
        "PackageA": [{"name": "Dependency1", "version": "1.0.0"}]
    }
    expected_output = "graph TD\n    PackageA --> Dependency1_1.0.0\n"
    assert generate_mermaid_graph(package_name, dependencies) == expected_output

def test_generate_mermaid_graph_multiple_dependencies():
    # Тест с несколькими зависимостями
    package_name = "PackageA"
    dependencies = {
        "PackageA": [
            {"name": "Dependency1", "version": "1.0.0"},
            {"name": "Dependency2", "version": "2.1.0"}
        ]
    }
    expected_output = (
        "graph TD\n"
        "    PackageA --> Dependency1_1.0.0\n"
        "    PackageA --> Dependency2_2.1.0\n"
    )
    assert generate_mermaid_graph(package_name, dependencies) == expected_output

def test_generate_mermaid_graph_no_dependencies():
    # Тест с пакетом без зависимостей
    package_name = "PackageA"
    dependencies = {
        "PackageA": []
    }
    expected_output = "graph TD\n"
    assert generate_mermaid_graph(package_name, dependencies) == expected_output

def test_generate_mermaid_graph_missing_package():
    # Тест, когда пакет отсутствует в списке зависимостей
    package_name = "MissingPackage"
    dependencies = {
        "PackageA": [{"name": "Dependency1", "version": "1.0.0"}]
    }
    expected_output = "graph TD\n"
    assert generate_mermaid_graph(package_name, dependencies) == expected_output

def test_generate_mermaid_graph_empty_dependencies():
    # Тест с пустым словарем зависимостей
    package_name = "PackageA"
    dependencies = {}
    expected_output = "graph TD\n"
    assert generate_mermaid_graph(package_name, dependencies) == expected_output
