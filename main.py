#!/usr/bin/env python3

import socket as sock
import paramiko
import threading

class SSHServer(paramiko.ServerInterface):
    def check_auth_password(self, username: str, password: str) -> int:
        print(f"{username}:{password}")
        return paramiko.AUTH_FAILED

def handle_connection(client):
    transport = paramiko.Transport(client)
    server_key = paramiko.RSAKey.generate(2048)
    # server_key = paramiko.RSAKey.from_private_key_file('key') 
    transport.add_server_key(server_key)
    ssh = SSHServer()
    transport.start_server(server=ssh)

def main():
    server = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    server.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
    server.bind(('', 2222))
    server.listen(223)

    while True:
        client, client_addr = server.accept()
        print(f"Connection from {client_addr[0]}:{client_addr[1]}")
        t = threading.Thread(target=handle_connection, args=(client, ))
        t.start()

if __name__ == "__main__":
    main()