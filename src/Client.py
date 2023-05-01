import pygame
import socket
import random
import time

suelo_image = pygame.image.load("../assets/suelo.png")
fondo_image = pygame.image.load("../assets/fondo.png")
pygame.init()

# Clase para manejar los objetos que caen
class Objeto():
    def __init__(self, x, y, width, height, color, speed):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.color = color
            self.rect = pygame.Rect(x, y, width, height)
            self.speed = speed

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

    def update(self):
        self.y += self.speed
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

# Función para generar nuevos objetos aleatorios
def generar_objetos(objetos, cantidad):
    for i in range(cantidad):
        x = random.randint(0, width-50)
        y = random.randint(-200, -50)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        speed = random.randint(1, 5)
        objeto = Objeto(x, y, 50, 50, color, speed)
        objetos.append(objeto)




# Clase para manejar la conexión de red
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
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
width = 800
height = 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

# Definir la lista de objetos y el temporizador de velocidad
objetos = []
velocidad = 1
temporizador = time.time()

jugador_posicion_x = 0
jugador_posicion_y = 470

# Definir la posición y el tamaño del piso
piso_posicion_x = 0
piso_posicion_y = 550
piso_ancho = 800
piso_alto = 50

ROJO = (255, 0, 0)

# Función para dibujar el piso en la pantalla
def dibujar_piso(x, y):
   win.blit(suelo_image, (x, y))


# Clase para manejar los jugadores
class Player():
    def __init__(self, x, y, width, height, color, image,text):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.color = color
            self.image = image
            self.rect = pygame.Rect(x, y, width, height)
            self.vel = 3
            self.facing_left = False
            self.text = text



    def draw(self, win):
        dibujar_piso(piso_posicion_x, piso_posicion_y)
        win.blit(self.text, (self.x + 10, self.y - 30))  # Dibujar el texto en la pantalla
        if self.facing_left:
            win.blit(pygame.transform.flip(self.image, True, False), (self.x, self.y))
        else:
            win.blit(self.image, (self.x, self.y))

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel
            self.facing_left = True
        if keys[pygame.K_RIGHT]:
            self.x += self.vel
            self.facing_left = False

        # Limitar la posición del jugador a la pantalla
        if self.x < 0:
            self.x = 0
        elif self.x > width - self.width:
            self.x = width - self.width

        self.update()

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

# Funciones para convertir las posiciones de texto a tuplas y viceversa
def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

# Función para dibujar los elementos en pantalla
def redrawWindow(win, player, player2):
    generar_objetos(objetos, 5)

    # Dibujar la imagen de fondo
    #win.blit(fondo_image, (0, 0))

    player.draw(win)
    player2.draw(win)
    
    dibujar_piso(piso_posicion_x, piso_posicion_y)
    #win.blit(suelo_image, (0,0))
    pygame.display.update()

# Función principal del programa
def main():

    run = True
    n = Network()
    startPos = read_pos(n.getPos())   
    # p = Player(startPos[0], startPos[1], 100, 100, (180, 255, 0))
    DV_text = pygame.font.SysFont('comicsans', 20).render('TU', True, (255, 255, 255))
    DM_text = pygame.font.SysFont('comicsans', 20).render('OTRO', True, (255, 255, 255))
    # posicion del player
    DV_image = pygame.image.load("../assets/DV.png")
    DM_image = pygame.image.load("../assets/DM.png")

    p = Player(jugador_posicion_x, jugador_posicion_y, 50, 100, (180, 255, 255), DV_image, "yo")
    p2 = Player(jugador_posicion_x, jugador_posicion_y, 50, 100, (0, 0, 0), DM_image,"rival")
    #pygame.mixer.music.load("../assets/Rip _ Tear(MP3_70K).mp3")
    #pygame.mixer.music.play(loops=-1)


    p = Player(jugador_posicion_x, jugador_posicion_y, 50, 100, (180, 255, 255), DV_image, DV_text)
    p2 = Player(jugador_posicion_x, jugador_posicion_y, 50, 100, (0, 0, 0), DM_image, DM_text)
    objeto = Objeto(x=100, y=50, width=30, height=30, color=(255, 0, 0), speed=3)
    
    clock = pygame.time.Clock()


    while run:
        clock.tick(60)

        # Actualizar la posición del jugador remoto
        p2Pos = read_pos(n.send(make_pos((p.x, p.y))))
        p2.x = p2Pos[0]
        p2.y = p2Pos[1]
        p2.update()
        objeto.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()


        objeto.draw(win)

        # Mover al jugador local
        p.move()
        # Enviar la posición del jugador local al servidor
        n.send(make_pos((p.x, p.y)))
        # Recibir la posición del jugador remoto del servidor
        p2.x = p2Pos[0]
        p2.y = p2Pos[1]
        p2.update()

        # Dibujar los elementos en pantalla
        redrawWindow(win, p, p2)

pygame.mixer.init()
main()
