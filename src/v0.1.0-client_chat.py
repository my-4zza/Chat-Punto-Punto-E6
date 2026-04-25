# Autor: Hernández García Juan Carlos
# v0.1.0

import socket

HOST = '127.0.0.1'
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

client_socket.sendall(b"Hola servidor, soy el cliente 1")

data = client_socket.recv(1024)
print(f"Servidor dice: {data.decode('utf-8')}")

client_socket.close()
