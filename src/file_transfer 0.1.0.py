import argparse

def recibir_archivo(host, port):
    print(f"[*] Modo Servidor: Preparado para recibir en {host}:{port}")

def enviar_archivo(host, port, ruta_archivo):
    print(f"[*] Modo Cliente: Preparado para enviar '{ruta_archivo}' a {host}:{port}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transferencia de Archivos")
    parser.add_argument('--mode', choices=['receive', 'send'], required=True)
    parser.add_argument('--host', required=True)
    parser.add_argument('--port', type=int, default=5001)
    parser.add_argument('--file')
    
    args = parser.parse_args()
    
    if args.mode == 'receive':
        recibir_archivo(args.host, args.port)
    elif args.mode == 'send':
        if not args.file:
            print("[!] Debes especificar el archivo con --file")
        else:
            enviar_archivo(args.host, args.port, args.file)
