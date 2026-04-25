#Autor:Alfredo
#Modificador: Alfredo Cid Garcia
#Fecha:24/04/26

import socket
import os
import hashlib
import logging
import argparse

# Crear carpetas necesarias
os.makedirs('../results/logs', exist_ok=True)   
os.makedirs('../results/received', exist_ok=True)

# Configurar logging
logging.basicConfig(
    filename='../results/logs/file_transfer.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def calcular_sha256(ruta_archivo):
    """Calcula el checksum SHA256 leyendo el archivo en bloques."""
    sha256 = hashlib.sha256()
    try:
        with open(ruta_archivo, 'rb') as f:
            for bloque in iter(lambda: f.read(4096), b""):
                sha256.update(bloque)
        return sha256.hexdigest()
    except Exception as e:
        print(f"[!] Error al leer el archivo: {e}")
        return None

def recibir_archivo(host, port):
    """Servidor que espera recibir un archivo."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((host, port))
        server.listen(1)
        print(f"[*] Esperando archivo en {host}:{port}...")
        
        conn, addr = server.accept()
        with conn:
            print(f"[+] Conexión de {addr} para transferencia.")
            
            # 1. Recibir encabezado
            header = conn.recv(1024).decode('utf-8')
            if not header: return
            
            filename, size_str, client_sha256 = header.strip().split('|')
            filesize = int(size_str)
            print(f"[*] Entrante: {filename} ({filesize} bytes) | SHA256: {client_sha256}")
            logging.info(f"Recepción iniciada: {filename}, {filesize} bytes, SHA256: {client_sha256}")
            
            # 2. Responder READY
            conn.sendall(b'READY')
            
            # 3. Recibir el archivo en bloques
            ruta_guardado = os.path.join('../results/received', filename)
            bytes_recibidos = 0
            
            with open(ruta_guardado, 'wb') as f:
                while bytes_recibidos < filesize:
                    chunk = conn.recv(4096)
                    if not chunk: break
                    f.write(chunk)
                    bytes_recibidos += len(chunk)
            
            # 4. Calcular SHA256 local y comparar
            server_sha256 = calcular_sha256(ruta_guardado)
            if server_sha256 == client_sha256:
                print("[*] Transferencia exitosa. Checksum coincide.")
                logging.info("Transferencia exitosa y verificada.")
                conn.sendall(b'OK')
            else:
                print("[!] Error: El checksum no coincide. Archivo corrupto.")
                logging.error("Fallo de verificación SHA256.")
                conn.sendall(b'ERR')
                
    except Exception as e:
        print(f"[!] Error de red: {e}")
        logging.error(f"Error: {e}")
    finally:
        server.close()

def enviar_archivo(host, port, ruta_archivo):
    """Cliente que envía un archivo."""
    if not os.path.exists(ruta_archivo):
        print("[!] El archivo no existe.")
        return

    filename = os.path.basename(ruta_archivo)
    filesize = os.path.getsize(ruta_archivo)
    file_sha256 = calcular_sha256(ruta_archivo)
    
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente.connect((host, port))
        
        # 1. Enviar encabezado: FILENAME|SIZE|SHA256\n
        header = f"{filename}|{filesize}|{file_sha256}\n"
        cliente.sendall(header.encode('utf-8'))
        
        # 2. Esperar READY
        respuesta = cliente.recv(1024).decode('utf-8')
        if respuesta != 'READY':
            print("[!] El servidor no está listo.")
            return
            
        print(f"[*] Enviando {filename} ({filesize} bytes)...")
        
        # 3. Enviar contenido
        with open(ruta_archivo, 'rb') as f:
            while True:
                chunk = f.read(4096)
                if not chunk: break
                cliente.sendall(chunk)
                
        # 4. Esperar confirmación
        confirmacion = cliente.recv(1024).decode('utf-8')
        if confirmacion == 'OK':
            print("[*] Archivo recibido y verificado por el servidor.")
            logging.info(f"Archivo {filename} enviado con éxito.")
        else:
            print("[!] El servidor reportó un error al recibir el archivo.")
            logging.error("Error reportado por el servidor.")
            
    except Exception as e:
        print(f"[!] Error al enviar: {e}")
        logging.error(f"Error de envío: {e}")
    finally:
        cliente.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transferencia de Archivos")
    parser.add_argument('--mode', choices=['receive', 'send'], required=True, help="Modo: recibir o enviar")
    parser.add_argument('--host', required=True, help="IP (usa 0.0.0.0 para recibir)")
    parser.add_argument('--port', type=int, default=5001, help="Puerto")
    parser.add_argument('--file', help="Ruta del archivo a enviar (solo para modo send)")
    
    args = parser.parse_args()
    
    if args.mode == 'receive':
        recibir_archivo(args.host, args.port)
    elif args.mode == 'send':
        if not args.file:
            print("[!] Debes especificar el archivo con --file")
        else:
            enviar_archivo(args.host, args.port, args.file)


#En el cmd introducir este comando:
#git add src/file_transfer.py
