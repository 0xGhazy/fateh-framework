import os
from termcolor import colored
from getpass import getuser
from tool_data import CommandModes, generator_help
from autocompleter import CommandCompleter
from pathlib import Path
import json
from validation.agent_generator_validation import read_agent_port, \
            read_agent_host, read_agent_name, read_agent_source


# TODO: make this in config file
cwd = Path(__file__).parent
agents_source = cwd / "agents"
extract_path = cwd.parent / "dist"
if not os.path.isdir(extract_path):
    os.mkdir(extract_path)

class AgentGenerator:

    def __init__(self) -> None:
        os.chdir(os.path.dirname(__file__))
        self.name = "fateh_http.pyw"
        self.host = "127.0.0.1"
        self.port = 8080
        self.agents_source = agents_source
        self.agent = None
        self.agent_dist = None
        self.auto_completer_prompt = colored("fateh/generator", "red") + " ~ "
        self.commands_list = CommandModes.generator_commands + os.listdir(agents_source)
        self.is_generated = False
        self.extract_path = extract_path

    def show_options(self):
        print(json.dumps(
            {
                "name": f"{self.name}",
                "host": f"{self.host}",
                "port": self.port,
                "agent-type": self.agent,
                "state": self.is_generated
            },
            indent=4))

    def get_agent_source(self, name: str):
        agents = os.listdir(self.agents_source)
        if name in agents:
            agent_path = self.agents_source / name
            with open(agent_path, "r") as file_obj:
                return file_obj.read()
        else:
            print(colored("[-] Invalid agent name", "red"))

    def fill_agent_data(self, source: str) -> str:
        source = source.replace("XIP", self.host)
        source = source.replace("XPORT", str(self.port))
        source = source.replace("XNAME", self.name)
        source = source.replace("XTYPE", self.agent)
        return source

    def write_agent(self, content: str) -> None:
        agent_dist = self.extract_path / self.name
        with open(agent_dist, "w") as file_obj:
            file_obj.write(content)
        if os.path.isfile(agent_dist):
            self.agent_dist = agent_dist
            self.is_generated = True
        else:
            print(colored(f"[-] Failed to generate <{self.name}> at {colored(self.agent_dist, 'yellow')}", "red"))

    def generate(self):
        if self.agent is None:
            print(colored("[!] Can't generate unspecified agent source, use 'set_agent'"))
            return
        try:
            # read agent source code with it's new data
            agent_source = self.get_agent_source(self.agent)
            filled_agent = self.fill_agent_data(agent_source)
            self.write_agent(filled_agent)
            print(colored(f"[+] <{self.name}> is generated at {colored(self.agent_dist, 'yellow')}", "green"))
        except Exception as error_message:
            print(colored(f"[!] An error was occurred while generating <{self.name}>","red"))
            print(colored(f"[!] {error_message}", "red"))

    def start(self):
        completer = CommandCompleter(self.commands_list)

        while True:
            command = completer.read_input(self.auto_completer_prompt + colored(os.getcwd(), "yellow"))

            if "set_name" in command.lower():
                self.name = read_agent_name(command)
            elif "set_host" in command.lower():
                self.host = read_agent_host(command)
            elif "set_port" in command.lower():
                self.port = read_agent_port(command)
            elif "set_agent" in command.lower():
                self.agent = read_agent_source(command, self.agents_source)
            elif "show" in command.lower():
                self.show_options()
            elif "generate" in command.lower():
                self.generate()
            elif "exit" in command.lower():
                break
            elif "_help" in command.lower():
                generator_help(self.command_flag)
            elif command.startswith("cd "):
                _, dist = command.split(" ")
                os.chdir(dist)
            else:
                os.system(command)


if __name__ == "__main__":
    x = AgentGenerator()
    x.start()
