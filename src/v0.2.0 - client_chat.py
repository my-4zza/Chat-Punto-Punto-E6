# Autor: Hernández García Juan Carlos
# v0.2.0

import socket

HOST = '127.0.0.1'
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print("[*] Conectado. Escribe un mensaje.")

while True:
    mensaje = input("Tú (Cliente): ")
    client_socket.sendall(mensaje.encode('utf-8'))    

    data = client_socket.recv(1024)
    print(f"Servidor: {data.decode('utf-8')}")

client_socket.close()
