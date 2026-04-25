#Autor:Alfredo
#Modificador: Jose santiago
#Fecha:24/04/26

import socket
import argparse

def recibir_archivo(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    print(f"[*] Esperando archivo en {host}:{port}...")
    
    conn, addr = server.accept()
    with conn:
        print(f"[+] Conexión de {addr} para transferencia.")
        mensaje = conn.recv(1024).decode('utf-8')
        print(f"[*] Mensaje recibido: {mensaje}")
    server.close()

def enviar_archivo(host, port, ruta_archivo):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((host, port))
    cliente.sendall(b'Hola, estoy listo para enviar el archivo')
    print("[*] Conexion exitosa y mensaje enviado.")
    cliente.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['receive', 'send'], required=True)
    parser.add_argument('--host', required=True)
    parser.add_argument('--port', type=int, default=5001)
    parser.add_argument('--file')
    args = parser.parse_args()
    
    if args.mode == 'receive': recibir_archivo(args.host, args.port)
    elif args.mode == 'send': enviar_archivo(args.host, args.port, args.file)

#En el CMD se pone esto para que se ejecute:
#git add src/file_transfer.py
