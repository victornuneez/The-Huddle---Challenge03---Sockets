# =================================================================================================================================================================================#
# ====================================================== (IMPORTACION DE LIBRERIAS Y CONFIGURACION INICIAL) =======================================================================#
# =================================================================================================================================================================================#


# Importamos  las herramientas para conexiones de red.
# Se usa para conectarse al servidor, enviar/recibir mensajes.
import socket

# Se usa hilos para realizar tareas paralelas como recibir mensajes mientras se envia mensajes.
import threading

# Herramientas relacionadas con el tiempo. Se usa para pausar segundos entr reintentos
import time

# Se define la direccion del servidor(localhost) y el puerto en donde esta esuchando el servidor.
# (Deben coincidir con el servidor para poder conectarse).
IP_clientes = "127.0.0.1"
puerto_cliente = 8000

# =================================================================================================================================================================================#
# ====================================================== (FUNCION QUE RECIBE MENSAJES EN UN HILO) =================================================================================#
# =================================================================================================================================================================================#


# Se define una funcion que solo va a recibir mensajes en un hilo separado.
def recibir_mensajes(cliente):

    #------------------------
    # OIDO Y BOCA DEL CLIENTE
    # -----------------------
    
    # Ejecuta un bloque de codigo que puede fallar 
    try:
        # Bucle que se ejecuta constantemente(espera mensajes) solo termina si hay un error o si el servidor se cierra.
        while True:

            # Es bloqueante se queda esperando aqui hasta que llegue un mensaje
            mensaje = cliente.recv(1024).decode("utf-8")

            # Se verifica si el mensaje esta vacio, significa que el servidor cerro la conexion.
            if not mensaje:
                # Se imprime un mensaje y se sale del bucle
                print("\n[DESCONECTADO] El servidor cerro la conexion.")
                break
            
            # Se imprime el mensaje recibido.
            print(f"\n{mensaje}")
            
            # Deja el cursor listo para escribir inmediatamnete, sin saltos de línea al recibir un mensaje.
            print(f"Tu mensaje: ", end="", flush=True)

    # -------------------------------------------------------
    # GESTIONA FALLOS INESPERADOS Y DESCONEXIONES DEL CLIENTE
    # -------------------------------------------------------

    # Captura los errores de desconexion abrupta(el servidor crasheo) y errores genericos del sitema operativo.
    except (ConnectionResetError, OSError):
        print("\n[ERROR] Conexion perdida con el servidor")

    # Captura cualquier otro error no esperado.
    except Exception as e:
        print(f"\n[ERROR]: {e}")


# =================================================================================================================================================================================#
# ====================================================== (FUNCION MAIN CLIENTE) ===================================================================================================#
# =================================================================================================================================================================================#


# Se define la funcion principal que va a ejecutar el socket del cliente.
def ejecutar_cliente():
    
    # Se define la IP, puerto y numero de intentos del cliente.
    IP_cliente = "127.0.0.1"
    puerto_cliente = 8000
    max_reintentos = 3

    # Bucle que controla los intentos de conexion al servidor.
    for intento in range(max_reintentos):
                
        try:

            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Proceso inicial de conexion y registro del nombre del cliente.
            cliente.connect((IP_cliente, puerto_cliente))
            print(f"Conectado a {IP_cliente}:{puerto_cliente}")

            # recibe la solicitud de nombre
            solicitud = cliente.recv(1024).decode("utf-8") # Es bloqueante.
            if solicitud == "NOMBRE":
                
                nombre = input("Ingresa tu nombre: ")
                cliente.send(nombre.encode("utf-8"))
                
                print("\nEscribe 'salir' para desconectarte.")

            # Se crea y arranca un hilo para que el cliente pueda recibir mensajes del servidor.            
            threading.Thread(target=recibir_mensajes, args=(cliente,), daemon=True).start()

            # Bucle principal del chat
            while True:
                mensaje = input("> ")
                
                if mensaje.lower() == "salir":
                    cliente.send(mensaje.encode("utf-8"))
                
                    print("Desconectando...")
                    cliente.close()
                    break  
                
                cliente.send(mensaje.encode("utf-8"))
            
            # Salir del bucle de intentos si se conecto correctamnete al servidor.
            break

        # Captura el error cuando el cliente se quiere conectar a un servidor apagado.
        except ConnectionRefusedError:
            print(f"No se pudo conectar (intento {intento+1}/{max_reintentos})")
            time.sleep(1)

        # Captura cualquier error general del sistema operativo..
        except OSError as e:
            print(f"[ERROR SOCKET]: {e}")
            break
    
    # Se ejecuta si el bucle termina sin un break. Se agoto los 3 intentos
    else:
        print(f"No se pudo conectar despues de {max_reintentos} intentos")

    # Mensaje final antes de que el programa termine. Se ejecuta siempre con o sin conexion exitosa
    print(f"Cliente cerrado")


if __name__ == "__main__":
    ejecutar_cliente()






