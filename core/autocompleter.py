import readline
from termcolor import colored


class CommandCompleter(object):

    def __init__(self, options):
        # list of commands to be auto completed
        self.options = sorted(options)


    def complete(self, text: str, state: int):
        if state == 0:  # on first trigger, build possible matches
            if text:
                # cache matches (entries that start with entered text)
                self.matches = [s for s in self.options if s and s.startswith(text)]
            else: 
                # no text entered, all matches possible
                self.matches = self.options[:]
        try: 
            return self.matches[state]
        except IndexError:
            return None
    

    def read_input(self, command_flag):
        # read commands from tha attacker instead of built-in input function.
        self.completer = CommandCompleter(self.options)
        readline.set_completer(self.completer.complete)
        readline.parse_and_bind('tab: complete')
        u_command = input(f"Fateh({colored(command_flag, 'red')})>> ")
        if u_command != "back":
            return u_command
        else:
            pass


if __name__ == '__main__':
    # test our auto completer
    test_commands = ["cd", "dir", "sysinfo"]
    x = CommandCompleter(test_commands)
