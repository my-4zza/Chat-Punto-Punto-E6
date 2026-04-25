# Version: v1.0.0
# Autor: Alarcón Galván Jimmy Loucioss

import socket
import argparse
import logging
import os
import threading

os.makedirs('../results/logs', exist_ok=True)

logging.basicConfig(
    filename='../results/logs/server_test1.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

clientes_conectados = []

def manejar_cliente(conn, addr):
    """Esta función corre en un hilo independiente para cada cliente"""
    with conn:
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                
                mensaje = data.decode('utf-8')
                print(f"\n[Cliente {addr[0]}]: {mensaje}")
                logging.info(f"Mensaje de {addr}: {mensaje}")
                
                for c in clientes_conectados:
                    if c != conn:
                        try:
                            c.sendall(f"[Cliente {addr[0]}]: {mensaje}".encode('utf-8'))
                        except:
                            pass
            except Exception:
                break
                
    print(f"\n[*] El cliente {addr[0]} se ha desconectado.")
    clientes_conectados.remove(conn)

def aceptar_conexiones(server_socket):
    """Esta función acepta clientes nuevos constantemente"""
    while True:
        conn, addr = server_socket.accept()
        print(f"\n[+] Nuevo cliente conectado: {addr}")
        logging.info(f"Conexión aceptada de {addr}")
        
        clientes_conectados.append(conn)
        
        hilo_cliente = threading.Thread(target=manejar_cliente, args=(conn, addr))
        hilo_cliente.daemon = True 
        hilo_cliente.start()

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((host, port))
        server_socket.listen(5) 
        print(f"[*] Servidor MULTIHILO escuchando en {host}:{port}")
        logging.info(f"Servidor iniciado en {host}:{port}")

        hilo_conexiones = threading.Thread(target=aceptar_conexiones, args=(server_socket,))
        hilo_conexiones.daemon = True
        hilo_conexiones.start()

        while True:
            mensaje = input("")
            if not mensaje.strip():
                continue
            if mensaje.lower() == 'salir':
                break
                
            for c in clientes_conectados:
                try:
                    c.sendall(f"Servidor: {mensaje}".encode('utf-8'))
                except:
                    pass
            logging.info(f"Servidor envió: {mensaje}")

    except Exception as e:
        print(f"[!] Error en el servidor: {e}")
        logging.error(f"Error: {e}")
    finally:
        server_socket.close()
        print("[*] Servidor apagado.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()
    start_server(args.host, args.port)
