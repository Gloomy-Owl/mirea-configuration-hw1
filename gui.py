# gui.py

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from commands import CommandHandler
from filesystem import VirtualFileSystem


class ShellEmulatorGUI:
    def __init__(self, username, filesystem_path, log_file):
        self.username = username
        self.filesystem_path = filesystem_path
        self.log_file = log_file
        self.vfs = VirtualFileSystem(filesystem_path)
        self.command_handler = CommandHandler(self.vfs, username, log_file)
        self.root = tk.Tk()
        self.root.title('Shell Emulator')
        self.create_widgets()

    def create_widgets(self):
        self.text_area = ScrolledText(self.root, state='disabled', height=20, width=80)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        self.entry = tk.Entry(self.root)
        self.entry.bind('<Return>', self.on_enter)
        self.entry.pack(fill=tk.X)
        self.display_prompt()

    def display_prompt(self):
        prompt = f"{self.username}@emulator:{self.vfs.cwd}$ "
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, prompt)
        self.text_area.see(tk.END)
        self.text_area.config(state='disabled')

    def on_enter(self, event):
        command = self.entry.get()
        self.entry.delete(0, tk.END)
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, command + '\n')
        self.text_area.config(state='disabled')

        output = self.command_handler.execute(command)
        if output == 'exit':
            self.vfs.close()
            self.root.quit()
        else:
            if output:
                self.text_area.config(state='normal')
                self.text_area.insert(tk.END, output + '\n')
                self.text_area.config(state='disabled')
            self.display_prompt()

    def run(self):
        self.root.mainloop()
