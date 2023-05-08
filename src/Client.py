import pygame
import random
from network import Network


meteorito_img = pygame.image.load("../assets/met.png")
suelo_image = pygame.image.load("../assets/suelo.png")
fondo_image = pygame.image.load("../assets/fondo.png")

pygame.init()
pygame.mixer.init()  # Inicializar el mezclador de audio de pygame

# Cargar el archivo de sonido de las pisadas
pisadas_sound = pygame.mixer.Sound("../assets/Pisadas.ogg")
pisadas_sound.set_volume(0.2)
# Definir la pantalla
width = 800
height = 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


jugador_posicion_x = 0
jugador_posicion_y = 470

# Definir la posición y el tamaño del piso
piso_posicion_x = 0
piso_posicion_y = 550
piso_ancho = 800
piso_alto = 50


ROJO = (255, 0, 0)

# Meteoritos
class Meteorito(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = meteorito_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, width - self.rect.width)
        self.rect.y = -self.rect.height
        self.velocidad = random.randint(1, 5)
        self.avoided = False  # Nueva variable para indicar si el meteorito se evadió
    
    def update(self):
        self.rect.y += self.velocidad
        if self.rect.y > height:
            self.rect.x = random.randrange(0, width - self.rect.width)
            self.rect.y = -self.rect.height
            self.velocidad = random.randint(1, 5)
            self.avoided = False  # Reiniciar la variable avoided cuando el meteorito vuelve a aparecer

    def check_collision(self):
        global vidas
        global score

        for meteorito in meteoros:
            if not meteorito.avoided and self.rect.colliderect(meteorito.rect):
                vidas -= 1
                meteorito.rect.x = random.randrange(0, width - meteorito.rect.width)
                meteorito.rect.y = -meteorito.rect.height
                meteorito.velocidad = random.randint(1, 5)
                meteorito.avoided = False
            elif not meteorito.avoided and meteorito.rect.bottom >= self.rect.top and meteorito.rect.left > self.rect.left and meteorito.rect.right < self.rect.right:
                score += 1
                meteorito.avoided = False
            elif meteorito.rect.bottom < self.rect.top and not meteorito.avoided:
                score += 1
                meteorito.avoided = True

            # if self.rect.colliderect(meteorito.rect):
            #     vidas -= 1
            #     meteorito.rect.x = random.randrange(0, width - meteorito.rect.width)
            #     meteorito.rect.y = -meteorito.rect.height
            #     meteorito.velocidad = random.randint(1, 5)
            #     meteorito.avoided = False  # Reiniciar la variable avoided cuando se produce una colisión
            # elif meteorito.rect.bottom >= self.rect.top and meteorito.rect.left > self.rect.left and meteorito.rect.right < self.rect.right:
            #     score += 1
            #     meteorito.avoided = False  # Reiniciar la variable avoided cuando se produce una colisión
            # elif meteorito.rect.bottom < self.rect.top and not meteorito.avoided:
            #     score += 1
            #     meteorito.avoided = True  # Establecer avoided en True cuando el meteorito se evadió

meteoros = pygame.sprite.Group()
for _ in range(5):
    meteoros.add(Meteorito())

    
# Función para dibujar el piso en la pantalla
def dibujar_piso(x, y):
   win.blit(suelo_image, (x, y))

# Definir el número de vidas
vidas = 3
score = 0
fuente_vidas = pygame.font.SysFont('comicsans', 30)


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
        #self.score = 0  # Variable de contador de puntos
        
    def draw(self, win):
        vidas_text = fuente_vidas.render('Vidas: ' + str(vidas), True, (255, 255, 255))
        win.blit(vidas_text, (10, 10))
        
        # Dibujar el puntaje en la pantalla
        score_text = fuente_vidas.render('Puntaje: ' + str(score), True, (255, 255, 255))
        win.blit(score_text, (width - score_text.get_width() - 10, 10))
        
        meteoros.update()
        meteoros.draw(win)

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
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            # Reproducir el sonido de las pisadas
            pisadas_sound.play()
        # Limitar la posición del jugador a la pantalla
        if self.x < 0:
            self.x = 0
        elif self.x > width - self.width:
            self.x = width - self.width
       
        self.update()
        self.check_collision()


    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def check_collision(self):
        global vidas
        global score
        
        for meteorito in meteoros:
            if self.rect.colliderect(meteorito.rect):
                vidas -= 1
                meteorito.rect.x = random.randrange(0, width - meteorito.rect.width)
                meteorito.rect.y = -meteorito.rect.height
                meteorito.velocidad = random.randint(1, 5)
            elif meteorito.rect.bottom < self.rect.top and not meteorito.avoided:
                score += 1
                meteorito.avoided = True  # Establecer avoided en True cuando el meteorito se evadió


# Funciones para convertir las posiciones de texto a tuplas y viceversa
def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

# Función para dibujar los elementos en pantalla
def redrawWindow(win, player, player2):
    
    # Dibujar la imagen de fondo
    win.blit(fondo_image, (0, 0))    

    player.draw(win)
    player2.draw(win)

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
    pygame.mixer.music.load("../assets/Rip _ Tear(MP3_70K).mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(loops=-1)
    # obstaculos.generar_obstaculos(num_obstaculos=2,pantalla_ancho=piso_ancho,pantalla_alto=600)
#    obstaculos.dibujar_obstaculos(win)
    



    p = Player(jugador_posicion_x, jugador_posicion_y, 50, 100, (180, 255, 255), DV_image, DV_text)
    p2 = Player(jugador_posicion_x, jugador_posicion_y, 50, 100, (0, 0, 0), DM_image, DM_text)
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         run = False
        #         pygame.quit()

        # Mover al jugador local
        p.move()

        # Dibujar los elementos en pantalla
        redrawWindow(win, p, p2)



pygame.mixer.init()
main()
