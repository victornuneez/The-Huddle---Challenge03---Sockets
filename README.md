# 💬 Proyecto: Chat Multiusuario en Tiempo Real (Sockets & Threading)

Este proyecto es un sistema de comunicación **cliente-servidor distribuido** diseñado para el intercambio de mensajes entre múltiples usuarios de forma simultánea. Utiliza protocolos de red estándar de la industria y una gestión avanzada de hilos para garantizar una experiencia fluida.



## 📖 Descripción

El sistema se basa en una arquitectura de **servidor centralizado** que gestiona conexiones concurrentes. El servidor actúa como un "hub" inteligente encargado de:

* **Gestión de Conexiones:** Registro y control de entrada/salida de nodos.
* **Retransmisión:** Procesamiento y distribución de mensajes en milisegundos.
* **Persistencia de Estado:** Mantenimiento de una lista activa de usuarios de forma sincronizada.

---

## 🛠️ Tecnologías y Conceptos Implementados

* **Sockets (TCP/IP):** Uso de la familia `AF_INET` y protocolo `SOCK_STREAM` para garantizar una comunicación orientada a conexión, asegurando que los mensajes lleguen íntegros y en el orden correcto.
* **Multithreading (Hilos):** Implementación de hilos independientes mediante la librería `threading`, permitiendo que cada cliente sea procesado en paralelo sin bloquear el hilo principal del servidor.
* **Sincronización (Locks):** Uso de `threading.Lock` para proteger las estructuras de datos compartidas, evitando condiciones de carrera (*race conditions*) al modificar la lista de usuarios.
* **Broadcast Dinámico:** Algoritmo de transmisión masiva que notifica eventos del sistema y mensajes de usuario a todos los nodos conectados simultáneamente.

---

## 🧠 Desafíos Técnicos Superados

### 1. Concurrencia Real y No Bloqueante
Gracias a la arquitectura multihilo, el servidor puede realizar el *handshake* con nuevas conexiones mientras procesa de forma ininterrumpida el tráfico de datos de los clientes ya conectados.

### 2. Robustez ante Desconexiones Abruptas
El sistema implementa un manejo de excepciones avanzado mediante bloques `try-except-finally`. Esto garantiza que, si un cliente pierde la conexión o el programa se cierra inesperadamente, el servidor libere los recursos, cierre el socket y limpie la lista de usuarios de forma segura.

### 3. Interfaz de Usuario Dual en Consola
El cliente utiliza un **hilo dedicado a la recepción** (`daemon=True`). Esto resuelve el problema clásico de las aplicaciones de consola donde la entrada de texto del usuario se bloquea al esperar datos de la red.

### 4. Reutilización de Puertos
Configuración de la opción `SO_REUSEADDR` a nivel de socket. Esto permite que el servidor se reinicie instantáneamente en el mismo puerto, evitando el estado de espera (*TIME_WAIT*) del sistema operativo.

---

## 🚀 Guía de Ejecución

Para desplegar el sistema en un entorno local, sigue estos pasos:

### 1. Iniciar el Servidor
Abre una terminal y ejecuta el script principal del servidor:
```
python servidor.py

```

### 2. Iniciar los Clientes

Abre múltiples terminales (una por cada usuario que quieras simular) y ejecuta en cada una:
```
python cliente.py
```
