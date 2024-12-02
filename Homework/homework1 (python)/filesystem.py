import zipfile

class VirtualFileSystem:
    def __init__(self, zip_path):
        self.fs = {"~": {}}
        self.current_path = "~/"
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
