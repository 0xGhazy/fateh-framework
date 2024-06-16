from socket import gethostbyname, inet_aton
from termcolor import colored
from string import ascii_lowercase, ascii_uppercase
from typing import List
import os

def name_validation(name: str):
    if len(name) > 1:
        return f"{name}.pyw"
    else:
        print(colored(f"[-] Error with naming shell [{name}.pyw]", "red"))
        return f"fateh-http.pyw"


def host_validation(host: str) -> str:
    if host[0] in ascii_lowercase or host[0] in ascii_uppercase:
        try:
            host = gethostbyname(host)
            return host
        except Exception as error_message:
            print(colored(f"[-] Error message:\n{error_message}\n", "red"))
    else:
        try:
            if inet_aton(host):
                return host
        except Exception as error_message:
            print(colored(f"[-] Error message:\n{error_message}\n", "red"))


def port_validation(port: str) -> int:
    if len(port) < 1:
        return 8080
    try:
        if int(port) < 1 or int(port) > 65353:
            print(colored("[-] Invalid port number, it must be between (1-65353)", "red"))
        return int(port)
    except Exception as error_message:
        print(colored(f"[-] Error message:\n{error_message}\n", "red"))
        return


###

def read_agent_name(command: str):
    try:
        name = command.lower().replace("set_name", "").strip()
        return name_validation(name)
    except:
        return "fateh_http.pyw"


def read_agent_host(command: str):
    try:
        host = command.lower().replace("set_host", "").strip()
        return host_validation(host)
    except:
        return "127.0.0.1"


def read_agent_port(command: str):
    try:
        port = command.lower().replace("set_port", "").strip()
        return port_validation(port)
    except:
        return 8080

def read_agent_source(command: str, agent_source: List[str]):
    try:
        agent = command.lower().replace("set_agent", "").strip()
        if agent in os.listdir(agent_source):    
            return agent
    except:
        print(colored("[-] Agent source not found in the ./cores/agents directory", "red"))