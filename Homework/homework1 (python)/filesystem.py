import zipfile

class VirtualFileSystem:
    def __init__(self, zip_path):
        self.fs = {"~": {}}
        self.current_path = "~"
        self.load_zip(zip_path)

    def load_zip(self, zip_path):
        with zipfile.ZipFile(zip_path, "r") as archive:
            for item in archive.namelist():
                if item.endswith("/"):
                    self._create_path(f"~/{item}")
                else:
                    self._create_path(f"~/{item}")
                    content = archive.read(item).decode("utf-8")
                    self._write_file(f"~/{item}", content)
        print(self.fs)

    def _create_path(self, path):
        parts = path[1:].strip("/").split("/")
        current = self.fs["~"]
        for part in parts:
            if part not in current:
                current[part] = {}
            current = current[part]

    def _write_file(self, path, content):
        parts = path[1:].strip("/").split("/")
        filename = parts.pop()
        current = self.fs["~"]
        for part in parts:
            current = current[part]
        current[filename] = content

    def _resolve_path(self, path):
        if path == ".":
            path = self.current_path
        elif path.startswith("/"):
            path = f"{self.current_path}{path}"
        return path

    def change_directory(self, path):
        resolved_path = self._resolve_path(path)
        if resolved_path == "~":
            parts = [resolved_path]
            current = self.fs
        else:
            parts = resolved_path[2:].split("/")
            current = self.fs["~"]
        for part in parts:
            if part in current and isinstance(current[part], dict):
                current = current[part]
            else:
                raise ValueError(f"cd: {path}: Нет такого файла или каталога")
        self.current_path = resolved_path

    def list_directory(self, path="."):
        resolved_path = self._resolve_path(path)
        if resolved_path == "~":
            parts = [resolved_path]
            current = self.fs
        else:
            parts = resolved_path[2:].split("/")
            current = self.fs["~"]
        for part in parts:
            if part in current and isinstance(current[part], dict):
                current = current[part]
            else:
                raise ValueError(f"ls: {path}: Нет такого файла или каталога")
        return current.keys()

    def find(self, name, path="."):
        resolved_path = self._resolve_path(path)
        if resolved_path == "~":
            parts = [resolved_path]
            current = self.fs
        else:
            parts = resolved_path[2:].split("/")
            current = self.fs["~"]
        for part in parts:
            if part in current and isinstance(current[part], dict):
                current = current[part]
            else:
                raise ValueError(f"find: {path}: Нет такого файла или каталога")
        results = []

        def search(directory, current_path):
            for item, value in directory.items():
                if item == name:
                    results.append(f"{current_path}/{item}")
                if isinstance(value, dict):
                    search(value, f"{current_path}/{item}")

        search(current, resolved_path)
        return "\n".join(results)

    def wc(self, name):
        path = self.current_path + "/" + name
        parts = path[2:].split("/")
        current = self.fs["~"]
        for part in parts[:-1]:
            if part in current and isinstance(current[part], dict):
                current = current[part]
            else:
                raise ValueError(f"wc: {path}: Нет такого файла или каталога")
        file_name = name
        if file_name not in current or not isinstance(current[file_name], str):
            raise ValueError(f"wc: {path}: Нет такого файла")
        content = current[file_name]
        lines = (content.strip("\n")).count("\n") + 1
        words = len(content.split())
        bytes_ = len(content.encode("utf-8"))
        return f"{lines} {words} {bytes_}"
