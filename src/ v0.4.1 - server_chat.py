# Version: v0.4.0
# Autor: Alarcón Galván Jimmy Loucioss

import socket
import argparse
import logging
import os
import threading

os.makedirs('../results/logs', exist_ok=True)
logging.basicConfig(filename='../results/logs/server_test1.log', level=logging.INFO, format='%(asctime)s - %(message)s')

clientes_conectados = []

def manejar_cliente(conn, addr):
    with conn:
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                mensaje = data.decode('utf-8')
                print(f"\n[Cliente {addr[0]}]: {mensaje}")
                
                # CORRECCIÓN: Ya tiene try/except individual para cada cliente
                for c in clientes_conectados:
                    if c != conn:
                        try:
                            c.sendall(f"[Cliente {addr[0]}]: {mensaje}".encode('utf-8'))
                        except:
                            pass
            except Exception:
                break
    clientes_conectados.remove(conn)

def aceptar_conexiones(server_socket):
    while True:
        conn, addr = server_socket.accept()
        clientes_conectados.append(conn)
        h = threading.Thread(target=manejar_cliente, args=(conn, addr))
        h.daemon = True
        h.start()

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # CORRECCIÓN: Se añade REUSEADDR para mitigar problemas de puertos ocupados
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"[*] Servidor MULTIHILO escuchando en {host}:{port}")

    h_con = threading.Thread(target=aceptar_conexiones, args=(server_socket,))
    h_con.daemon = True
    h_con.start()

    # FALTA: No hay manera de romper este bucle limpiamente con una palabra clave.
    while True:
        mensaje = input("")
        if not mensaje.strip():
            continue
        for c in clientes_conectados:
            try:
                c.sendall(f"Servidor: {mensaje}".encode('utf-8'))
            except:
                pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()
    start_server(args.host, args.port)
