#Autor:Alfredo
#Modificador: Alfredo
#Fecha:24/04/26

import socket
import argparse
import os

def recibir_archivo(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    print(f"[*] Esperando archivo...")
    
    conn, addr = server.accept()
    with conn:
        print(f"[+] Recibiendo de {addr}")
        with open('archivo_recibido.txt', 'wb') as f:
            while True:
                chunk = conn.recv(4096)
                if not chunk: break
                f.write(chunk)
        print("[*] Transferencia finalizada.")
    server.close()

def enviar_archivo(host, port, ruta_archivo):
    if not os.path.exists(ruta_archivo):
        return print("[!] El archivo no existe.")

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((host, port))
    print(f"[*] Enviando {ruta_archivo}...")
    
    with open(ruta_archivo, 'rb') as f:
        while True:
            chunk = f.read(4096)
            if not chunk: break
            cliente.sendall(chunk)
    print("[*] Archivo enviado.")
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
