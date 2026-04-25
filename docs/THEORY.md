# Teoría de Redes y Sockets

Este documento contiene la fundamentación teórica para el desarrollo del proyecto de chat punto a punto y transferencia de archivos.

## ¿Qué es un socket?
Un **socket** es el punto final de un enlace de comunicación bidireccional entre dos programas que se ejecutan en una red. Es la abstracción de programación que permite a las aplicaciones enviar y recibir datos. 
* **Ejemplo de uso:** Se puede comparar con una llamada telefónica. La dirección IP actúa como el número de teléfono principal de la empresa, y el puerto es la extensión directa a la oficina de la persona con la que quieres hablar. En nuestro proyecto, usamos `socket.socket(socket.AF_INET, socket.SOCK_STREAM)` para crear esta conexión.

## TCP vs UDP
Existen dos protocolos principales en la capa de transporte:
* **TCP (Transmission Control Protocol):** Es orientado a la conexión. Garantiza que los paquetes lleguen en orden y sin errores (si se pierde un paquete, lo vuelve a pedir). 
    * *Ventajas:* Alta fiabilidad e integridad de datos.
    * *Cuándo usarlo:* Transferencia de archivos, chats de texto, páginas web, correos electrónicos. (Por esto lo elegimos para el proyecto).
* **UDP (User Datagram Protocol):** Es sin conexión. Envía los datos lo más rápido posible sin importar si el receptor los recibe todos o en orden.
    * *Ventajas:* Alta velocidad y menor latencia.
    * *Cuándo usarlo:* Transmisiones en vivo (streaming), videojuegos en línea, videollamadas.

## Puertos y Direcciones IP
* **Dirección IP:** Es el identificador lógico y único de un dispositivo en la red (ej. `192.168.137.1`).
* **Puertos:** Son canales virtuales que permiten al sistema operativo dirigir el tráfico a la aplicación correcta.
    * **Puertos bien conocidos (0 - 1023):** Reservados para servicios del sistema y protocolos estándar (ej. 80 para HTTP, 443 para HTTPS, 22 para SSH).
    * **Puertos dinámicos/privados (49152 - 65535) y registrados (1024 - 49151):** Disponibles para que los usen aplicaciones de usuario. En nuestro chat utilizamos un puerto en este rango (como el `5050`) para evitar conflictos con el sistema.

## NAT y problemas de conectividad
**NAT (Network Address Translation)** es una técnica usada por los routers para traducir múltiples direcciones IP privadas de una red local a una sola IP pública para salir a Internet.
* **El problema P2P:** Si dos computadoras están en casas distintas (detrás de NATs diferentes), no pueden verse directamente porque sus IPs privadas no son enrutables en Internet. Esto requiere técnicas complejas como *Port Forwarding* o servidores *STUN/TURN*. Al estar en una red local o Hotspot, evitamos el NAT y permitimos la conexión directa.

## Firewalls y permisos de puerto
Un **Firewall** es un sistema de seguridad que monitorea y controla el tráfico de red entrante y saliente basado en reglas de seguridad. 
* **Permisos:** Por defecto, los sistemas operativos (como Windows Defender Firewall) bloquean conexiones TCP entrantes en puertos no estándar. Para que el servidor del chat pueda recibir la conexión del cliente, es estrictamente necesario habilitar el permiso de red pública/privada para el ejecutable de Python o abrir el puerto específico.

## Wi-Fi Direct vs Hotspot vs Misma Red
* **Misma Red (Infraestructura):** Ambos equipos se conectan a un router central (ej. el módem de casa). 
    * *Limitación:* Muchas redes públicas o escolares tienen "AP Isolation" (Aislamiento de AP), lo que impide que los dispositivos conectados se comuniquen entre sí por seguridad.
* **Hotspot (Soft AP):** Una computadora actúa como un enrutador virtual, emitiendo su propia red Wi-Fi y asignando direcciones IP. 
    * *Ventaja:* Ideal para saltar las restricciones de aislamiento de redes de infraestructura. 
* **Wi-Fi Direct:** Es un estándar que permite que dos dispositivos establezcan una conexión P2P sin necesidad de un punto de acceso intermedio. 
    * *Limitación:* Su implementación a nivel de programación en sistemas operativos de escritorio con Python puro es muy compleja y requiere APIs específicas del OS, por lo que el Hotspot es una alternativa más viable y universal.

## Seguridad básica: TLS/SSL y recomendaciones
Por defecto, los sockets TCP transmiten la información en **texto plano**. Esto significa que cualquiera conectado a la misma red usando un analizador de paquetes (como Wireshark) podría leer los mensajes del chat o interceptar los archivos.
* **TLS/SSL (Transport Layer Security):** Es el protocolo que cifra la información antes de enviarla por el socket. En Python, se implementaría envolviendo el socket original con la librería `ssl`.
* **Recomendaciones para pruebas de laboratorio:**
    1. No transmitir información personal, contraseñas o datos sensibles durante la ejecución de las pruebas.
    2. Utilizar el entorno de Hotspot cerrado con contraseña (WPA2) en lugar de una red LAN pública abierta.
    3. Apagar el Hotspot inmediatamente después de concluir las pruebas.
