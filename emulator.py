# emulator.py

import argparse
import sys
from gui import ShellEmulatorGUI

def main():
    parser = argparse.ArgumentParser(description='Shell Emulator')
    parser.add_argument('--username', required=True, help='Имя пользователя для приглашения')
    parser.add_argument('--filesystem', required=True, help='Путь к архиву виртуальной файловой системы')
    parser.add_argument('--log', required=True, help='Путь к лог-файлу')

    args = parser.parse_args()

    gui = ShellEmulatorGUI(args.username, args.filesystem, args.log)
    gui.run()

if __name__ == '__main__':
    main()
