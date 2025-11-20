# ===========================================================================================================================================================================#
#=============================================== (BLOQUE DE IMPORTACIONES DE MODULOS Y CONFIGURACION GLOBAL) ================================================================#
# ===========================================================================================================================================================================#

# Modulo para crear conexiones de red(cliente servidor)
import socket

# Modulo pra crear hilos(threads) y ejeutar codigo en paralelo.
import threading

# Definimos en donde escuchara el servidor, direccion IP local(localhost) y en que puerto deben conectarse los clientes.
direccion_IP = "127.0.0.1"
Puerto = 8000

# ===========================================================================================================================================================================#
#============================================== (BLOQUE DE ESTRUCUTURA DE DATOS COMPARTIDAS) ================================================================================#
# ===========================================================================================================================================================================#

# Lista de todos los sockets activos
clientes = []

# Diccionario que contendra los nombres de cada socket de los clientes conectados, (agenda telefonica) Ej: socket del cliente numero de telefono, nombre de usuario es el contacto.
nombres = {}

# Su proposito es controlar el acceso a clientes y nombres.
candado = threading.Lock()

# ===========================================================================================================================================================================#
#================================================== (BLOQUE FUNCION BROADCAST(TRANSMISION)) =================================================================================#
# ===========================================================================================================================================================================#

# Es una funcion que envia un mensaje a todos los clientes conectados excepto al remitente.
def broadcast(mensaje, remitente=None):

    # Activa el lock antes de ejecutar este bloque y se desbloquea al salir de este bloque.(Evita que varios clientes traten de modificar el mismo recurso al mismo tiempo)
    with candado:

        # Este bloque envia el mensaje a todos los clientes menos al remitente.
        for cliente in clientes[:]:           
            if cliente != remitente:
                try:
                    cliente.send(mensaje.encode("utf-8"))
                
                # Limpia a los clientes que no recibieron el mensaje
                except:
                    clientes.remove(cliente) # Los saca de la lista de conexiones activas(clientes)
                    if cliente in nombres:  # Evitar el keyerror(borrar algo que no existe)
                        del nombres[cliente] # elimina su nombre del diccionario.

# ===========================================================================================================================================================================#
# ==================================================== (BLOQUE FUNCION HILO CLIENTE) ========================================================================================#
# ===========================================================================================================================================================================#

# Esta funcion se encarga de ejecutar un hilo para cada cliente.
def hilo_cliente(socket_cliente, direccion):

    # ----------------------------------------
    # REGISTRO DEL CLIENTE Y AVISO AL SERVIDOR
    # ----------------------------------------

    # Variable que contedra los nombres de cada cliente.
    nombre = None 

    # El try indica que este bloque puede tener errores pero que lo puede manejar.
    try:
        # En este bloque se le pide al usuario que ingrese un nombre y tambien recibe el nombre que el cliente ingreso.
        socket_cliente.send("NOMBRE".encode("utf-8"))
        nombre = socket_cliente.recv(1024).decode("utf-8").strip() # Es bloqueante.

        # Este bloque filtra que los usuaios no envien nombres vacios o nombres muy largos.
        if not nombre or len(nombre) > 20:
            socket_cliente.close()
            return 

        # Se activa el candado para que dos clientes no puedan modificar "clientes y nombres" al mismo tiempo
        with candado:
            clientes.append(socket_cliente)  # Se agrega el socket del cliente a la lista activa de conexiones(clientes)
            nombres[socket_cliente] = nombre # Guarda en el diccionario "nombres" el nombre del usuario asociado a su socket.

        # Este print muestra un mensaje en pantalla en la consola del servidor.
        print(f"[+] {nombre} conectado desde {direccion}")
        broadcast(f"[SERVIDOR] {nombre} se unio al chat", socket_cliente)  # Se llama a la funcion broadcast para enviar un mensaje a todos los clientes conectados

        # ---------------------------------------------------------------
        #  BUCLE DE ESCUCHA Y REENVIO DE MENSAJES DEL CLIENTE AL SERVIDOR
        # ---------------------------------------------------------------

        # Bucle que mantiene al hilo escuhando mensajes constantemente.
        while True:

            # Puede haber errores en este bloque y try los maneja.(el recv puede tener algun error)
            try:
                # El hilo se detiene aca esperando los mensajes de los clientes.
                mensaje = socket_cliente.recv(1024).decode("utf-8")
                
                # Se verifica si el cliente sigue conectado o si hay un mensaje que sea para salir del servidor.
                if not mensaje or mensaje.lower() == "salir":
                    break

                # Se verifica si hay un mensaje, con strip() se verifica si despues de limpiar espacios hay un mensaje.
                if mensaje.strip():
                    # Se imprime en pantalla del servidor el mensaje del cliente.
                    print(f"[{nombre}]: {mensaje}")
                    
                    # Envia el mensaje a todos los clientes menos al remitente.
                    broadcast(f"[{nombre}]: {mensaje}", socket_cliente)

            # Esta exception captura los errores de desconexion abrupta.
            except ConnectionResetError:
                print(f"[!] {nombre} perdio la conexion abruptamente")
                break
            
            # Este except captura cualquier error inesperado.
            except Exception as e:
                print(f"[!] Error recibiendo mensaje de {nombre}: {e}")
                break
    
    # --------------------------------------------------------------------
    # BLOQUE DE MANEJO DE ERRORES Y LIMPIEZA DE LA DESCONEXION DEL CLIENTE
    # --------------------------------------------------------------------

    # Captura cualquier error que no sea una desconexion abrupta. "e" guarda el error para poder imprimirlo.
    except Exception as e:
        print(f"[!] Error del hilo del cliente: {e}")        
                
    # Este bloque siempre se va ejecutar no importa si hay un error o no.
    finally:
        # with activa el candado para que solo un hilo por vez modifique estos datos.
        with candado:
                # Este bloque se encarga de limpiar correctamente la información del cliente cuando termina su conexión.(propia o errores)
                    if socket_cliente in clientes:
                        clientes.remove(socket_cliente)

                    if socket_cliente in nombres:
                        del nombres[socket_cliente]

                    try: 
                        socket_cliente.close()
                    
                    # Ignora los errores del sistema operativo como cuando el socket ya esta cerrado.
                    except OSError:
                        pass
                    
                    # Este bloque de codigo avisa a todos cuando un cliente se desconecta.
                    # Se verifica si tiene un nombre, Si se desconecto  antes de dar su nombre, no hay nada que avisar.
                    if nombre:
                        print(f"[-] {nombre} desconectado")
                        broadcast(f"[SERVIDOR] {nombre} salio del chat")

#=====================================================================================================================================================#
#================================================== (BLOQUE PRINCIPAL) ===============================================================================#
#=====================================================================================================================================================#

# Se crea el objeto socket que usa a la familia de direcciones IPv4 con el protocolo TCP.
servidor = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)

# "setsockopt" sirve para cambiar las configuraciones internas que el sistema operativo usa para manejar los sockets.
# "socket.SOL_SOCKET" Le dice a python en que nivel del sistema operativo se quiere cambiar una opcion.
# "socket.SO_REUSEADDR" opcion especifica que se quiere activar, reutilizar la direccion,(se reusa el puerto sin tiempo de espera) 
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Asocia al servidor una direccion IP y un puerto en formato de tuplas.
servidor.bind((direccion_IP, Puerto))

# Pone al servidor en modo de escucha.
servidor.listen()
print(f"Servidor escuchando en {direccion_IP}: {Puerto}")
        
# Bucle principal: aceptar clientes y crear un hilo por cada uno
while True:
    cliente_socket, direccion = servidor.accept() # Es bloqueante.
    print(f"[+] Nueva conexión desde {direccion}")
    threading.Thread(target=hilo_cliente, args=(cliente_socket, direccion), daemon=True).start()



