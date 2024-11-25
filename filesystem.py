# filesystem.py
import os
import shutil
import tarfile
from datetime import datetime

class VirtualFileSystem:
    def __init__(self, archive_path):
        self.archive_path = archive_path
        self.tar = tarfile.open(archive_path, 'r')
        self.cwd = '.'  # Current Working Directory

    def list_dir(self, path=None):
        path = path or self.cwd
        dirs = set()
        files = set()
        for member in self.tar.getmembers():
            if member.name.startswith(path):
                relative_path = member.name[len(path):].lstrip('/')
                if '/' in relative_path:
                    dirs.add(relative_path.split('/')[0])
                elif relative_path:
                    files.add(relative_path)
        return sorted(dirs), sorted(files)

    def change_dir(self, path):
        if path == '..':
            if self.cwd != '.':
                self.cwd = '/'.join(self.cwd.rstrip('/').split('/')[:-1]) or '.'
        elif path == '.':
            pass
        else:
            new_path = self.cwd.rstrip('/') + '/' + path if self.cwd != '.' else path
            if any(member.name.startswith(new_path) for member in self.tar.getmembers()):
                self.cwd = new_path
            else:
                raise FileNotFoundError(f"No such directory: {path}")

    def remove(self, path):
        # Определяем абсолютный путь в архиве
        abs_path = self.cwd.rstrip('/') + '/' + path if self.cwd != '.' else path

        # Проверяем, есть ли такой файл или папка
        members_to_keep = []
        found = False
        for member in self.tar.getmembers():
            if not member.name.startswith(abs_path):
                members_to_keep.append(member)
            else:
                found = True

        if not found:
            raise FileNotFoundError(f"No such file or directory: {path}")

        # Создаём временный архив
        temp_path = self.archive_path + '.tmp'
        with tarfile.open(temp_path, 'w') as new_tar:
            for member in members_to_keep:
                fileobj = self.tar.extractfile(member) if member.isfile() else None
                new_tar.addfile(member, fileobj)

        # Заменяем старый архив на новый
        self.close()
        shutil.move(temp_path, self.archive_path)
        self.tar = tarfile.open(self.archive_path, 'r')

    def find(self, filename):
        found_paths = []
        for member in self.tar.getmembers():
            if member.name.endswith(filename):
                found_paths.append(member.name)
        return found_paths

    def close(self):
        self.tar.close()
