# Autor: Hernández García Juan Carlos
# v0.4.0

import socket
import argparse
import logging
import os
import threading

os.makedirs('../results/logs', exist_ok=True)
logging.basicConfig(filename='../results/logs/client_test1.log', level=logging.INFO)

def recibir(sock):
    while True:
        data = sock.recv(1024)
        print(f"\n{data.decode()}")

def start_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    # BUG/FALTA: Los hilos no son daemon. Si haces Ctrl+C, el programa se queda colgado en segundo plano.
    threading.Thread(target=recibir, args=(client_socket,)).start()

    while True:
        msg = input("")
        client_socket.sendall(msg.encode())

if _name_ == "_main_":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', required=True)
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()
    start_client(args.host, args.port)
