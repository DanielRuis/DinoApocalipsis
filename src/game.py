import pygame
import socket

# Clase para manejar la conexión de red
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.56.1"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.pos = self.connect()

    def getPos(self):
        return self.pos

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

# Definir la pantalla
width = 500
height = 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

# Clase para manejar los jugadores
class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.vel = 3

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel
        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        # Limitar la posición del jugador a la pantalla
        if self.x < 0:
            self.x = 0
        elif self.x > width - self.width:
            self.x = width - self.width

        self.update()

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
#Clase para la pantalla de carga
class LoadingScreen():
    def __init__(self, text, font_size, x, y):
        self.text = text
        self.font_size = font_size
        self.x = x
        self.y = y
        self.font = pygame.font.SysFont(None, self.font_size)
        self.surface = self.font.render(self.text, True, (255, 255, 255))

    def draw(self, win):
        win.blit(self.surface, (self.x, self.y))

# Funciones para convertir las posiciones de texto a tuplas y viceversa
def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

# Función para dibujar los elementos en pantalla
def redrawWindow(win, player, player2):
    win.fill((128, 128, 128))
    player.draw(win)
    player2.draw(win)
    pygame.display.update()  

# Función principal del programa
def main():
    run = True
    n = Network()

    # Crear la pantalla de carga
    loading_text = LoadingScreen("Esperando a que se conecte el otro jugador...", 30, 100, 200)

    # Mostrar la pantalla de carga mientras se espera a que los dos jugadores se conecten
    connected = False
    while not connected:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        # Verificar si se ha recibido un mensaje del otro jugador
        data = n.client.recv(2048).decode()
        if data == 'Connected':
            connected = True

        # Dibujar la pantalla de carga
        loading_text.draw(win)
        pygame.display.update()

    # Iniciar el juego cuando ambos jugadores estén conectados
    p = Player(0, 500, 50, 100, (180, 255, 255))
    p2 = Player(200, 500, 50, 100, (0, 0, 0))

    clock = pygame.time.Clock()

    while run:
        clock.tick(60)

        # Actualizar la posición del jugador remoto
        p2Pos = read_pos(n.send(make_pos((p.x, p.y))))
        p2.x = p2Pos[0]
        p2.y = p2Pos[1]
        p2.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        # Mover al jugador local
        p.move()

        # Dibujar los elementos en pantalla
        redrawWindow(win, p, p2)

    pygame.quit()

main()
