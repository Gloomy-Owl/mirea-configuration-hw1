# commands.py

import csv
from datetime import datetime

class CommandHandler:
    def __init__(self, vfs, username, log_file):
        self.vfs = vfs
        self.username = username
        self.log_file = log_file

    def log_action(self, action):
        with open(self.log_file, 'a', newline='') as csvfile:
            logwriter = csv.writer(csvfile)
            logwriter.writerow([datetime.now().isoformat(), self.username, action])

    def execute(self, command_line):
        parts = command_line.strip().split()
        if not parts:
            return ''
        command = parts[0]
        args = parts[1:]

        if command == 'ls':
            output = self.ls(args)
        elif command == 'cd':
            output = self.cd(args)
        elif command == 'rm':
            output = self.rm(args)
        elif command == 'find':
            output = self.find(args)
        elif command == 'exit':
            output = 'exit'
        else:
            output = f"Command not found: {command}"

        self.log_action(command_line)
        return output

    def ls(self, args):
        dirs, files = self.vfs.list_dir()
        return '\n'.join(dirs + files)

    def cd(self, args):
        if not args:
            return 'cd: missing operand'
        try:
            self.vfs.change_dir(args[0])
        except FileNotFoundError as e:
            return str(e)
        return ''

    def rm(self, args):
        if not args:
            return 'rm: missing operand'
        try:
            self.vfs.remove(args[0])
        except FileNotFoundError as e:
            return str(e)
        return f"Removed {args[0]}"

    def find(self, args):
        if not args:
            return 'find: missing operand'
        matches = self.vfs.find(args[0])
        if matches:
            return '\n'.join(matches)
        else:
            return 'No matches found'
