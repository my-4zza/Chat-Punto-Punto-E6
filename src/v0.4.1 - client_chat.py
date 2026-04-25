# Autor: Hernández García Juan Carlos
# v0.4.1

import socket
import argparse
import logging
import os
import threading

os.makedirs('../results/logs', exist_ok=True)
logging.basicConfig(filename='../results/logs/client_test1.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def recibir_mensajes(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print("\n[*] El servidor ha cerrado la conexión.")
                os._exit(0)
            print(f"\n{data.decode('utf-8')}")
        except Exception:
            break

def start_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        print(f"[*] Conectado a la sala del servidor {host}:{port}")

        hilo = threading.Thread(target=recibir_mensajes, args=(client_socket,))
        hilo.daemon = True
        hilo.start()

        # FALTA: Falta el comando 'salir' y el bloque finally con client_socket.close()
        while True:
            mensaje = input("")
            if not mensaje.strip():
                continue
            client_socket.sendall(mensaje.encode('utf-8'))
    except Exception as e:
        print(f"[!] Error de conexión: {e}")

if _name_ == "_main_":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', required=True)
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()
    start_client(args.host, args.port)
