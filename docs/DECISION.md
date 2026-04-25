 Decisiones de Diseño y Arquitectura de Red

## 1. Método elegido
Para la implementación de este chat punto a punto, el método de conexión de red elegido fue la creación de un *Hotspot (Punto de acceso Wi-Fi local)* generado desde la laptop que actúa como servidor.

## 2. Justificación de la elección
Se seleccionó este método por encima de otras opciones por las siguientes razones técnicas:
* *Seguridad y Aislamiento*: Al crear una red propia, se cumple con la directriz de no utilizar redes públicas abiertas, evitando que el tráfico del chat sea visible para terceros.
* *Control de Direccionamiento*: El hotspot asigna automáticamente una dirección IP dentro de un segmento conocido (como el 192.168.137.x visto en las pruebas), lo que facilita la configuración del cliente.
* *Independencia de Infraestructura*: No se requiere de un router externo, permitiendo que el proyecto sea funcional en cualquier lugar solo con las dos laptops.

## 3. Comandos usados
Para establecer la red y verificar la conectividad antes de iniciar los scripts de Python, se utilizaron los siguientes comandos:

* ipconfig: Ejecutado para identificar la dirección IPv4 del adaptador del hotspot en el servidor (192.168.137.1) y la dirección asignada al cliente.
* ping: Para validar que existiera respuesta entre ambas máquinas antes de abrir los sockets TCP.
* *Configuración de Windows*: Se utilizó la interfaz de "Punto de acceso móvil" para gestionar el SSID y la contraseña de la red privada.

## 4. Problemas encontrados y cómo se resolvieron

* *Bloqueo por Firewall*:
    * *Descripción*: Inicialmente, el cliente no podía conectar al servidor arrojando un error de tiempo de espera, a pesar de estar en la misma red.
    * *Solución*: Se identificó que el firewall de Windows bloqueaba las conexiones entrantes en el puerto 5000. Se añadieron reglas de exclusión para permitir el tráfico de Python en redes privadas.
* *Identificación del adaptador de red*:
    * *Descripción*: Al haber múltiples adaptadores activos (Wi-Fi, Ethernet, Virtual), era confuso determinar qué IP usar.
    * *Solución*: Mediante el uso de ipconfig se filtró específicamente por el adaptador de "Conexión de área local" relacionado al hotspot para obtener la IP correcta del gateway.
