💬 Proyecto: Chat Multiusuario en Tiempo Real (Sockets & Threading)

Este proyecto es un sistema de comunicación cliente-servidor distribuido que permite el intercambio de mensajes entre múltiples usuarios de forma simultánea, utilizando protocolos de red estándar de la industria.

📖 Descripción

El sistema consta de un servidor centralizado que gestiona conexiones concurrentes y múltiples clientes que pueden unirse o salir de la sala de chat. El servidor actúa como un "hub" inteligente, retransmitiendo mensajes y gestionando el estado de los usuarios en tiempo real.

🛠️ Tecnologías y Conceptos Implementados

Sockets (TCP/IP): Uso de la familia AF_INET y protocolo SOCK_STREAM para garantizar que los mensajes lleguen íntegros y en orden.

Multithreading (Hilos): Implementación de hilos independientes para que cada cliente sea procesado en paralelo sin bloquear el servidor.

Sincronización (Locks): Uso de threading.Lock para proteger las estructuras de datos compartidas (listas de clientes) y evitar errores de concurrencia.

Broadcast dinámico: Algoritmo de transmisión masiva que notifica entradas, salidas y mensajes a todos los nodos conectados.

🧠 Desafíos Técnicos Superados

Concurrencia Real: Gracias al uso de hilos, el servidor puede "escuchar" a un Cliente A mientras el Cliente B está enviando un mensaje, permitiendo una experiencia fluida.

Robustez en Desconexiones: El código maneja activamente las desconexiones abruptas (crashes de cliente o pérdida de red) mediante bloques try-finally, asegurando que los recursos del sistema se liberen correctamente.

Interfaz de Usuario en Consola: El cliente implementa un hilo dedicado a la recepción (daemon=True) para que la escritura del usuario no se vea interrumpida por la llegada de nuevos mensajes.

Reutilización de Puertos: Configuración de SO_REUSEADDR para permitir reinicios rápidos del servidor sin esperar los tiempos de liberación del sistema operativo.

🚀 Guía de Ejecución

Para probar el sistema en una máquina local:

Lanzar el Servidor:

Bash

python servidor.py

Lanzar múltiples Clientes (en terminales separadas):

Bash

python cliente.py

Ingresa tu nombre y comienza a chatear.
