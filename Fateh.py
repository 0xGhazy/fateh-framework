from os import system
from termcolor import colored
from cores.tool_data import banner, CommandModes, main_help
from cores.shell_generator import ShellGenerator
from cores.autocompleter import CommandCompleter
from cores.functions import checking_requirements, ip_lookup
from cores.connection_handler import Handler
import os

class Fateh:

    def __init__(self):
        checking_requirements()
        self.tool_banner = banner()
        self.cwd = colored(os.getcwd(), "red")
        self.available_mode_commands = CommandModes.server_commands
        self.shell_gen = ShellGenerator()

    def start(self):

        completer = CommandCompleter(self.available_mode_commands)
        while True:
            command = completer.read_input(colored(f"server ~ {colored(os.getcwd(), 'green')}", "red"))
            
            try:
                if len(command) < 1:
                    print(colored("[-] Dont't play with me bro ~_~", "red"))

                elif command == "generator":
                    self.shell_gen.command_prompot()

                elif "geo_ip" in command:
                    _, ip = command.split()
                    ip_lookup(ip)

                elif command == "exit" or command == "0":
                    exit(0)

                elif "start_listener" in command:
                    command = command.replace("start_listener", "").strip().split()
                    if len(command) == 3:
                        s_type, host, port = command
                        Handler(s_type, host, int(port))
                    else:
                        print(colored("""
                        [-] You must enter 3 values ex:
                        start_listener tcp 127.0.0.1 8080
                        """, "red"))

                elif "cd" in command:
                    _, directory = command.split(" ")
                    os.chdir(directory)

                elif "_help" in command:
                    main_help("Server")

                else:
                    system(command)

            except Exception as error_message:
                print(colored(f"[-] {error_message}", "red"))

if __name__ == '__main__':
    my_server = Fateh()
    my_server.start()
