 Decisiones de Diseño y Arquitectura de Red

## 1. Método elegido
Para la implementación de este chat punto a punto, el método de conexión de red elegido fue la creación de un *Hotspot (Punto de acceso Wi-Fi local)* generado desde la laptop que actúa como servidor.

## 2. Justificación de la elección
Se seleccionó este método por encima de otras opciones por las siguientes razones técnicas:
* *Seguridad y Aislamiento*: Al crear una red propia, se cumple con la directriz de no utilizar redes públicas abiertas, evitando que el tráfico del chat sea visible para terceros.
* *Control de Direccionamiento*: El hotspot asigna automáticamente una dirección IP dentro de un segmento conocido (como el 192.168.137.x visto en las pruebas), lo que facilita la configuración del cliente.
* *Independencia de Infraestructura*: No se requiere de un router externo, permitiendo que el proyecto sea funcional en cualquier lugar solo con las dos laptops.
