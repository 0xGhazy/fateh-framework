import os
import readline
from termcolor import colored
from typing import List

cwd = os.getcwd()
current_directories_list = os.listdir(cwd)

class CommandCompleter:

    def __init__(self, options: List[str]):
        self.options = sorted(options)

    def complete(self, text: str, state: int):
        options_with_files = sorted(self.options + current_directories_list)
        if text.startswith('cd '):
            # If the text starts with 'cd ', auto-complete directory names
            text = text[3:]
            # dirs = [d for d in options_with_files if os.path.isdir(d) and d.startswith(text)]
        else:
            if state == 0:
                if text:
                    # cache matches (entries that start with entered text)
                    self.matches = [s for s in options_with_files if s and s.startswith(text)]
                else:
                    # no text entered, all matches possible
                    self.matches = options_with_files[::]

        try:
            return self.matches[state]
        except IndexError:
            return None

    def read_input(self, flag: str):
        self.completer = CommandCompleter(self.options)
        readline.set_completer(self.completer.complete)
        readline.parse_and_bind('tab: complete')
        command = input(f"Fateh({colored(flag, 'yellow')} ~ {colored(cwd, 'red')})>> ")
        if command != "back":
            return command


if __name__ == '__main__':
    commands = ["cd ", "ifconfig", "dir", "session"]
    cwd = os.getcwd()
    auto_completer = CommandCompleter(commands)
    while True:
        try:
            result = auto_completer.read_input("fateh/generator")
            if result.startswith("cd "):
                dist = f"{result.split(' ')[1]}"
                os.chdir(dist)
                cwd = os.getcwd()
                current_directories_list = os.listdir(cwd)
            else:
                os.system(result)
        except Exception as e:
            print(colored("[+] auto-completer session ended successfully", "red"))
