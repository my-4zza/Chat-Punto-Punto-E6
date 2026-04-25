# Version: v0.3.0
# Autor: Alarcón Galván Jimmy Loucioss

import socket
import argparse
import logging

logging.basicConfig(filename='../results/logs/server_test1.log', level=logging.INFO)

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    
    print(f"[*] Servidor iniciado en {host}:{port}")
    conn, addr = server_socket.accept()
    logging.info(f"Conectado a {addr}")

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            print(f"Cliente: {data.decode('utf-8')}")
            
            respuesta = input("Servidor: ")
            conn.sendall(respuesta.encode('utf-8'))
        except Exception as e:
            logging.error(f"Error: {e}")
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()
    start_server(args.host, args.port)
