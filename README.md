# Chat Punto a Punto Wi-Fi y Transferencia de Archivos (Equipo 6)

## Resumen y Objetivo
Este proyecto consiste en una aplicación de comunicación desarrollada en **Python** que permite el intercambio de mensajes en tiempo real y la transferencia segura de archivos entre laptops conectadas a una misma red Wi-Fi o mediante un Hotspot. 

El sistema utiliza **Sockets TCP** para garantizar la entrega de datos y **Threading (Multihilo)** para permitir conversaciones fluidas entre múltiples clientes y el servidor simultáneamente, superando la limitación de comunicación 1 a 1.

---

## Requisitos de Software
* **Python 3.8 o superior**
* **Bibliotecas estándar:** `socket`, `threading`, `hashlib`, `argparse`, `logging`, `os`.

---

## Estructura del Proyecto
```text
/
├── README.md              # Guía principal del proyecto
├── CHANGELOG.md           # Registro de cambios y aportes por integrante
├── requirements.txt       # Dependencias (estándar de Python)
├── /src                   # Código fuente
│   ├── server_chat.py     # Servidor multihilo principal
│   ├── client_chat.py     # Cliente de chat asíncrono
│   └── file_transfer.py   # Script de transferencia con SHA256
├── /docs                  # Documentación técnica
│   ├── THEORY.md          # Conceptos de redes y sockets
│   ├── DECISION.md        # Justificación de red y solución de problemas
│   └── LEARNED_PYTHON.md  # Resumen de aprendizaje técnico
├── /images/tests          # Evidencias (Capturas de pantalla)
└── /results               # Salidas de ejecución
    ├── logs/              # Registros históricos de conexión
    └── received/          # Archivos recibidos mediante file_transfer
```

---

##  Instrucciones de Uso

### 1. Configuración de Red
Asegúrese de que todas las computadoras estén en la misma red Wi-Fi o conectadas al Hotspot.
* **Obtener IP:** Ejecute `ipconfig` (Windows) o `ifconfig` (Mac) y anote la dirección IPv4 del servidor.

### 2. Ejecutar el Chat
**Servidor (Laptop Windows):**
```bash
py src/server_chat.py
```
**Clientes (Windows/Mac):**
```bash
# En Windows
py src/client_chat.py --host [IP_DEL_SERVIDOR]

# En Mac
python3 src/client_chat.py --host [IP_DEL_SERVIDOR]
```

### 3. Transferencia de Archivos
**Receptor:**
```bash
py src/file_transfer.py --mode receive --host 0.0.0.0
```
**Emisor:**
```bash
py src/file_transfer.py --mode send --host [IP_DEL_RECEPTOR] --file prueba.txt
```

---

##  Características Técnicas Implementadas
* **Concurrencia:** Uso de `threading` para manejar múltiples clientes sin bloquear el flujo del servidor.
* **Integridad de Datos:** Implementación de **SHA256** en la transferencia de archivos para verificar que el archivo recibido es idéntico al original.
* **Protocolo Estructurado:** Envío de metadatos (Nombre|Tamaño|Hash) mediante un encabezado previo a la transmisión de bytes.
* **Logging:** Registro automático de eventos en la carpeta `results/logs/`.
* **Multiplataforma:** Interoperabilidad probada exitosamente entre **Windows 10/11 y macOS**.

---

## Equipo E6 - Integrantes
| Nombre del Integrante | Contacto (Matrícula y Correo) |
| :--- | :--- |
| **Azael Pérez González** | Matrícula: zs24013146 - [zs24013146@estudiantes.uv.mx](mailto:zs24013146@estudiantes.uv.mx) |
| **José Santiago Alegría Ponce** | Matrícula: zs24013141 - [zs24013141@estudiantes.uv.mx](mailto:zs24013141@estudiantes.uv.mx) |
| **Juan Carlos Hernández García** | Matrícula: zs24013178 - [zs24013178@estudiantes.uv.mx](mailto:zs24013178@estudiantes.uv.mx) |
| **Alfredo Cid García** | Matrícula: zs24013120 - [zs24013120@estudiantes.uv.mx](mailto:zs24013120@estudiantes.uv.mx) |
| **Antonio De Jesus Portilla Durán** | Matrícula: zs24013166 - [zs24013166@estudiantes.uv.mx](mailto:zs24013166@estudiantes.uv.mx) |
| **Jimmy Loucioss Alarcon Galván** | Matrícula: zs24013200 - [zs24013200@estudiantes.uv.mx](mailto:zs24013200@estudiantes.uv.mx) |
---

## Seguridad
Este software fue diseñado para fines académicos. Se recomienda usar solo en redes privadas y cerrar los puertos/hotspot tras finalizar las pruebas.
