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