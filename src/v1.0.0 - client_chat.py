# Autor: Hernández García Juan Carlos
# v1.0.0

import socket
import argparse
import logging
import os
import threading

os.makedirs('../results/logs', exist_ok=True)

logging.basicConfig(
    filename='../results/logs/client_test1.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def recibir_mensajes(client_socket):
    """Hilo independiente para escuchar mensajes del servidor en todo momento"""
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print("\n[*] El servidor ha cerrado la conexión.")
                os._exit(0) # Termina el programa abruptamente si el servidor cae
            
            respuesta = data.decode('utf-8')
            print(f"\n{respuesta}")
            logging.info(f"Mensaje recibido: {respuesta}")
        except Exception:
            break

def start_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))
        print(f"[*] Conectado exitosamente a la sala del servidor {host}:{port}")
        logging.info(f"Conectado a {host}:{port}")

        # Iniciar hilo de recepción
        hilo_recepcion = threading.Thread(target=recibir_mensajes, args=(client_socket,))
        hilo_recepcion.daemon = True
        hilo_recepcion.start()

        # Bucle principal para enviar mensajes
        while True:
            mensaje = input("")
            if not mensaje.strip():
                continue
            if mensaje.lower() == 'salir':
                break
                
            client_socket.sendall(mensaje.encode('utf-8'))
            logging.info(f"Mensaje enviado: {mensaje}")

    except Exception as e:
        print(f"[!] Error de conexión: {e}")
        logging.error(f"Error: {e}")
    finally:
        client_socket.close()
        print("[*] Desconectado.")

if _name_ == "_main_":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', required=True, help='IP del servidor')
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()
    start_client(args.host, args.port)
