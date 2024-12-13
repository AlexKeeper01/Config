def generate_mermaid_graph(dependencies):
    mermaid_graph = "graph TD\n"

    for package, deps in dependencies.items():
        for dep_info in deps:
            dep_name = dep_info["name"]
            dep_version = dep_info["version"]

            dep_string = f"    {package} --> {dep_name}_{dep_version}"
            mermaid_graph += dep_string + "\n"

    return mermaid_graph
