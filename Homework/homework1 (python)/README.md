emulator.py

```
import argparse
from shell import Shell
from filesystem import VirtualFileSystem
from gui import ShellGUI


def parse_args():
    parser = argparse.ArgumentParser(description="Shell Emulator")
    parser.add_argument("--user", required=True, help="User name for shell prompt")
    parser.add_argument("--host", required=True, help="Host name for shell prompt")
    parser.add_argument("--fs", required=True, help="Path to virtual filesystem (zip)")
    parser.add_argument("--script", required=False, help="Path to startup script")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    vfs = VirtualFileSystem(args.fs)
    shell = Shell(args.user, args.host, vfs)

    if args.script:
        with open(args.script) as script:
            for line in script:
                shell.execute(line.strip())

    gui = ShellGUI(shell)
    gui.run()
```

filesystem.py

```
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
```

gui.py

```
import tkinter as tk

class ShellGUI:
    def __init__(self, shell):
        self.shell = shell

    def run(self):
        root = tk.Tk()
        root.title("Shell Emulator")

        text_output = tk.Text(root, wrap=tk.WORD)
        text_output.grid(row=0, column=0, sticky="nsew")

        input_field = tk.Entry(root)
        input_field.grid(row=1, column=0, sticky="ew")

        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=0)
        root.grid_columnconfigure(0, weight=1)

        def execute_command(event):
            command = input_field.get()
            input_field.delete(0, tk.END)
            text_output.insert(tk.END, f"{self.shell.prompt()}{command}\n")
            try:
                result = self.shell.execute(command)
                if result:
                    text_output.insert(tk.END, f"{result}\n")
            except Exception as e:
                text_output.insert(tk.END, f"Ошибка: {e}\n")
            if not self.shell.running:
                root.destroy()

        input_field.bind("<Return>", execute_command)
        root.mainloop()
```

shell.py

```
class Shell:
    def __init__(self, user, host, vfs):
        self.user = user
        self.host = host
        self.vfs = vfs
        self.running = True

    def prompt(self):
        return f"{self.user}@{self.host}:{self.vfs.current_path}$ "

    def execute(self, command):
        parts = command.split()
        if not parts:
            return ""
        cmd, *args = parts

        try:
            if cmd == "ls":
                return "\n".join(sorted(self.vfs.list_directory(*args)))
            elif cmd == "cd":
                self.vfs.change_directory(*args)
            elif cmd == "exit":
                self.running = False
            elif cmd == "whoami":
                return self.user
            elif cmd == "find":
                return self.vfs.find(*args)
            elif cmd == "wc":
                return self.vfs.wc(*args)
            else:
                return f"Неизвестная команда: {cmd}"
        except ValueError as e:
            return str(e)
```

test_commands.py

```
import pytest
from shell import Shell
from filesystem import VirtualFileSystem

@pytest.fixture
def shell():
    vfs = VirtualFileSystem("linux_filesystem.zip")
    return Shell("test_user", "test_host", vfs)


def test_ls(shell):
    result = shell.execute("ls")
    assert result == "bin\netc\nhome\nusr\nvar"


def test_cd(shell):
    shell.execute("cd /bin")
    assert shell.vfs.current_path == "~/bin"
    result = shell.execute("ls")
    assert result == "cat\nls"


def test_whoami(shell):
    result = shell.execute("whoami")
    assert result == "test_user"


def test_exit(shell):
    shell.execute("exit")
    assert not shell.running


def test_find(shell):
    result = shell.execute("find home")
    assert result == "~/home"


def test_wc(shell):
    shell.execute("cd /home/user")
    result = shell.execute("wc file1.txt")
    assert result == "1 5 28"


def test_unknown_command(shell):
    result = shell.execute("unknown_command")
    assert result == "Неизвестная команда: unknown_command"
```
