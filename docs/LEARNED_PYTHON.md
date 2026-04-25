
# Aprendizajes de Python (LEARNED_PYTHON.md)
### En este documento se resumen los principales conceptos, módulos y funciones de la biblioteca estándar de Python que investigamos y aplicamos para el desarrollo de nuestro Chat Punto a Punto y el sistema de Transferencia de Archivos.

# 1. Sockets y funciones clave
### El módulo socket es la base de nuestra aplicación. Nos permitió crear la conexión de red a nivel de sistema operativo.

## socket(): Crea el objeto socket. En nuestro caso, usamos AF_INET (para IPv4) y SOCK_STREAM (para el protocolo TCP).

## bind(): Asocia el socket del servidor a una dirección IP y un puerto específicos (ej. 0.0.0.0:5000).

## listen(): Pone al servidor en modo "escucha", esperando a que un cliente toque a la puerta.

## accept(): Acepta la conexión entrante. Devuelve un nuevo socket dedicado exclusivamente a hablar con ese cliente y la tupla con su dirección IP.

## connect(): Utilizado por el cliente para iniciar la conexión hacia la IP y puerto del servidor.

## sendall(): A diferencia de send(), esta función garantiza que todos los bytes especificados se envíen por la red, manejando internamente los reintentos si la red está saturada.

## recv(): Lee los bytes que llegan desde la red. Nosotros usamos un búfer de 1024 o 4096 bytes.

# 2. Manejo de archivos (Bloques y Chunks)
### Para la transferencia de archivos, aprendimos que cargar un archivo gigante en la memoria RAM de golpe es una mala práctica que puede congelar la computadora.

## open(): Usamos el gestor de contexto (with open(...)) en modo rb (lectura binaria) y wb (escritura binaria) para garantizar que los archivos se cierren automáticamente al terminar o si ocurre un error.

## Envío por chunks: Implementamos un bucle while que lee el archivo en bloques (chunks) de 4096 bytes usando f.read(4096) y los envía por el socket. El servidor hace lo mismo a la inversa: recibe de 4096 en 4096 y va escribiendo en el disco duro poco a poco.

# 3. Hashing y verificación (SHA256)
### Para asegurar que los archivos no se corrompieran durante el viaje por el Wi-Fi, utilizamos el módulo hashlib.

### Creamos una función que lee el archivo original en bloques y calcula su SHA256 (hashlib.sha256().hexdigest()).

### El cliente envía esta "huella digital" antes que el archivo.

### Cuando el servidor termina de descargar, calcula el SHA256 del archivo nuevo. Si ambas huellas coinciden, confirmamos al 100% la integridad de los datos.

# 4. Logging: Registro de eventos
### En aplicaciones de servidor, usar solo print() no es suficiente porque la consola se cierra y se pierde la historia. Usamos el módulo logging para crear archivos .log.

## Configuramos logging.basicConfig() para guardar los eventos en results/logs/.

## Aprendimos a registrar eventos según su gravedad: logging.info() para conexiones y mensajes, y logging.error() para capturar excepciones del sistema (try/except).

### 5. Argumentos de terminal (Argparse)
### Para no tener que modificar el código fuente cada vez que cambiábamos de red o de computadora, usamos argparse.

### Esto nos permitió ejecutar nuestros scripts de forma dinámica desde la terminal.

## Implementamos banderas (flags) como --host para la IP, --port para cambiar de puerto (5000 para chat, 5001 para archivos), --mode (send/receive) y --file para especificar el archivo a transferir.

# 6. Concurrencia básica
### Para lograr que nuestro servidor pudiera hablar con varios clientes al mismo tiempo (y que no se congelara esperando a que alguien escribiera), investigamos métodos de concurrencia:

### threading (El método que elegimos): Permite ejecutar múltiples "hilos" en el mismo proceso. Creamos un hilo independiente para la recepción de mensajes de cada cliente. Es ideal para tareas "I/O bound" (limitadas por entrada/salida) como los sockets, donde el programa pasa mucho tiempo esperando respuestas de la red.

### select: Una forma de multiplexar I/O en un solo hilo. Permite a un programa monitorear múltiples sockets a la vez para ver cuál está listo para leer o escribir. Es muy eficiente a nivel de sistema operativo.

### asyncio: Es la concurrencia moderna de Python basada en un bucle de eventos (Event Loop) y funciones async/await. Es excelente para manejar miles de conexiones simultáneas en un solo hilo, aunque requiere reestructurar el código de manera asíncrona.

# 7. Utilidades del sistema operativo
### os: Lo usamos intensamente en nuestro proyecto para manejar rutas multiplataforma (ej. os.path.join), obtener el tamaño de un archivo en bytes (os.path.getsize) y crear carpetas automáticamente (os.makedirs).

### pathlib: Una alternativa orientada a objetos para manejar rutas, más moderna y legible que os.path.

### subprocess: Permite a Python ejecutar comandos directamente en la terminal del sistema operativo (como si escribiéramos netsh o ipconfig a mano) y capturar su salida.

# 8. Buenas prácticas implementadas
### Metadatos antes de datos: En nuestro protocolo de transferencia (file_transfer.py), el cliente siempre envía una cabecera (FILENAME|SIZE|SHA256) y espera un READY. Esto previene que el servidor reciba bytes a ciegas.

### Manejo de errores: Todo el código de red está envuelto en bloques try/except/finally para evitar que el programa se cierre de golpe (crash) si el Wi-Fi falla y para asegurar que el socket.close() siempre se ejecute.

### Commits semánticos: Llevamos un registro limpio en Git usando prefijos claros (feat:, docs:, test:) para que la contribución de cada integrante sea fácilmente rastreable.
