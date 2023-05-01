import socket
import threading
import json
import random

# configuración del cliente
host = 'localhost'
port = 8200

# crea el socket del cliente
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((host, port))
mensaje = "Hola desde el cliente"
cliente.send(mensaje.encode())
respuesta=cliente.recv(1024)
print(respuesta)
print(respuesta)
print(respuesta)
print(respuesta)
cliente.close()
