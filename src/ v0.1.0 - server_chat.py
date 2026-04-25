import socket
# Autor: Alarcón Galván Jimmy Loucioss
# Version: v0.2.0

import socket

HOST = '127.0.0.1'
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"[*] Servidor escuchando en {HOST}:{PORT}")
conn, addr = server_socket.accept()
print(f"[+] Conectado a {addr}")

while True:
   
    data = conn.recv(1024)
    if not data:
        break
    
    print(f"Cliente: {data.decode('utf-8')}")
    
    respuesta = input("Tú (Servidor): ")
    conn.sendall(respuesta.encode('utf-8'))

conn.close()
server_socket.close()
