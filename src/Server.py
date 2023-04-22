import socket
#import threading
#import json

# Configuración del servidor
host = 'localhost'
port = 8200
max_conexiones = 3

# Crea el socket del servidor
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((host, port))

# Espera conexiones de los clientes
servidor.listen(max_conexiones)
print('Servidor esperando conexiones...')

# Lista de clientes conectados
clientes = []

# Espera conexiones de los clientes
while True:
    # Acepta la conexión del cliente
    cliente, direccion = servidor.accept()
    print(f'Jugador {direccion}, dentro')

    #Le envaimos al cliente un mensaje de conexion establecida
    mensaje = "Estas dentro!"
    cliente.send(mensaje.encode())
    
    # Agrega el cliente a la lista de clientes conectados
    clientes.append(cliente)
    
    # Verifica que se hayan conectado todos los clientes
    if len(clientes) == max_conexiones:
        break

print('Todos los clientes se han conectado. Iniciando el juego...')

