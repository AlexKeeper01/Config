import subprocess


def save_graph_to_png(mermaid_graph, output_path, graph_tool_path):
    temp_file = "temp_graph.mmd"

    with open(temp_file, "w") as file:
        file.write(mermaid_graph)

    command = [graph_tool_path, "-i", temp_file, "-o", output_path, "--theme", "forest"]

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError("Ошибка при визуализации графа.")
