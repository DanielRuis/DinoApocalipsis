# juego DinoRunLife

para ejecutar el juego se necesita de

## Cambiar la ip en el Server.py y Network.py
- network.py
```
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "TU IP"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.pos = self.connect()
```
- Server.py
```
server = "TU IP"
port = 5555

```


 correr el servidor Server.py

```
python .\Server.py
```
## luego se ejecuta el archivo que contiene el juego en este caso es Client.py

```
python .\Client.py
```