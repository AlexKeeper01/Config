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
