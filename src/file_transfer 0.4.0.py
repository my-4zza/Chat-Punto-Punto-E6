#Autor:Alfredo
#Modificador: José Santiago Alegría Ponce
#Fecha:24/04/26

import socket
import argparse
import os
import hashlib

def calcular_sha256(ruta_archivo):
    sha256 = hashlib.sha256()
    with open(ruta_archivo, 'rb') as f:
        for bloque in iter(lambda: f.read(4096), b""):
            sha256.update(bloque)
    return sha256.hexdigest()

def recibir_archivo(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    
    conn, addr = server.accept()
    with conn:
        header = conn.recv(1024).decode('utf-8')
        filename, size_str, client_sha256 = header.strip().split('|')
        print(f"[*] Entrante: {filename} | SHA256: {client_sha256}")
        
        conn.sendall(b'READY')
        
        with open(filename, 'wb') as f:
            bytes_recibidos = 0
            while bytes_recibidos < int(size_str):
                chunk = conn.recv(4096)
                if not chunk: break
                f.write(chunk)
                bytes_recibidos += len(chunk)
        
        if calcular_sha256(filename) == client_sha256:
            print("[*] Transferencia exitosa. Checksum coincide.")
        else:
            print("[!] Error: Archivo corrupto.")
    server.close()

def enviar_archivo(host, port, ruta_archivo):
    filename = os.path.basename(ruta_archivo)
    filesize = os.path.getsize(ruta_archivo)
    file_sha256 = calcular_sha256(ruta_archivo)
    
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((host, port))
    
    header = f"{filename}|{filesize}|{file_sha256}\n"
    cliente.sendall(header.encode('utf-8'))
    
    if cliente.recv(1024).decode('utf-8') == 'READY':
        with open(ruta_archivo, 'rb') as f:
            while True:
                chunk = f.read(4096)
                if not chunk: break
                cliente.sendall(chunk)
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


#En el cmd introducir este comando:
#git add src/file_transfer.py
