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

        if cmd == "ls":
            return "\n".join(self.vfs.list_directory(*args))
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
