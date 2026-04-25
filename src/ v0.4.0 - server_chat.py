# Version: v0.4.0
# Autor: Alarcón Galván Jimmy Loucioss

import socket
import argparse
import logging
import os
import threading

os.makedirs('../results/logs', exist_ok=True)
logging.basicConfig(filename='../results/logs/server_test1.log', level=logging.INFO)

clientes = []

def manejar_cliente(conn, addr):
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(f"[{addr[0]}]: {data.decode()}")
        
        for c in clientes:
            if c != conn:
                c.sendall(f"[{addr[0]}]: {data.decode()}".encode())

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    
    print(f"[*] Servidor MULTIHILO en {host}:{port}")

    def aceptar():
        while True:
            conn, addr = server_socket.accept()
            clientes.append(conn)
            threading.Thread(target=manejar_cliente, args=(conn, addr)).start()

    threading.Thread(target=aceptar).start()

    while True:
        msg = input("")
        for c in clientes:
            c.sendall(f"Servidor: {msg}".encode())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()
    start_server(args.host, args.port)
