# Autor: Hernández García Juan Carlos
# v0.3.0

import socket
import argparse
import logging

logging.basicConfig(filename='../results/logs/client_test1.log', level=logging.INFO)

def start_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    logging.info(f"Conectado a {host}:{port}")

    while True:
        mensaje = input("Cliente: ")
        client_socket.sendall(mensaje.encode('utf-8'))
        
        data = client_socket.recv(1024)
        print(f"Servidor: {data.decode('utf-8')}")

if _name_ == "_main_":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', required=True)
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()
    start_client(args.host, args.port)
