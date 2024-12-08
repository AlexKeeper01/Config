def generate_mermaid_graph(package_name, dependencies):
    mermaid_graph = "graph TD\n"
    for dep_info in dependencies.get(package_name, []):
        dep_name = dep_info["name"]
        dep_version = dep_info["version"]

        dep_string = f"    {package_name} --> {dep_name}_{dep_version}"
        mermaid_graph += dep_string + "\n"

    return mermaid_graph
