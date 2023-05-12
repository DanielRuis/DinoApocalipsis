import pygame
import random
from network import Network
from meteorito import Meteorito



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
# titulo del juego
pygame.display.set_caption("Dino run for life")

# posicion del jugador ubicado ala altura del piso
jugador_posicion_x = 0
jugador_posicion_y = 470

# Definir la posición y el tamaño del piso
piso_posicion_x = 0
piso_posicion_y = 550
piso_ancho = 800
piso_alto = 50

# Definir el número de vidas
vidas = 3

# inicio del puntaje
score = -5
fuente_vidas = pygame.font.SysFont('comicsans', 30)

# imagenes de los dinosaurios 
DV_image = pygame.image.load("../assets/DV.png")
DM_image = pygame.image.load("../assets/DM.png")

# tiempo de espera para inicial la caida de meteroritos
TIEMPO_ESPERA = 5000
caida_meteoritos = False
     # Dibujar la puntacion de vida

vidas_text = fuente_vidas.render('Vidas: ' + str(vidas), True, (255, 255, 255))

# Función para verificar si ha pasado suficiente tiempo y comenzar a hacer caer los meteoritos


def verificar_tiempo():
    global caida_meteoritos
    tiempo_actual = pygame.time.get_ticks()
    # Verificar si ha pasado suficiente tiempo desde el inicio del juego
    if tiempo_actual >= TIEMPO_ESPERA:
        caida_meteoritos = True

# Definir la función para mostrar el mensaje de "Perdiste"
def mostrar_perdiste():
    font = pygame.font.Font(None, 36)  # Crear una fuente
    texto = font.render("Perdiste", True, (255, 0, 0))  # Crear el objeto de texto
    texto_rect = texto.get_rect(center=(width/2, height/2))  # Obtener el rectángulo del objeto de texto
    win.blit(texto, texto_rect)  # Dibujar el objeto de texto en el centro de la pantalla



# Función para dibujar el piso en la pantalla
def dibujar_piso(x, y):
    win.blit(suelo_image, (x, y))

meteoros = pygame.sprite.Group()
for _ in range(5):
    meteoros.add(Meteorito())

# Clase para manejar los jugadores
class Player():
    def __init__(self, x, y, width, height, color, image, text):
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

        # tiempo restante
        self.start_time = pygame.time.get_ticks()
        self.time_remaining = TIEMPO_ESPERA

    def draw(self, win):
        
        vidas_text = fuente_vidas.render('Vidas: ' + str(vidas), True, (255, 255, 255))
        win.blit(vidas_text, (width - vidas_text.get_width() - 150, -150))
        win.blit(vidas_text, (10, 10))

        if vidas == 0:
            mostrar_perdiste()
    # Dibujar el puntaje en la pantalla
            score_text = fuente_vidas.render('Puntaje: ' + str(score), True, (255, 255, 255))
            win.blit(score_text, (width - score_text.get_width() - 350, 250))

        else:
    # Dibujar el puntaje en la pantalla
            score_text = fuente_vidas.render('Puntaje: ' + str(score), True, (255, 255, 255))
            win.blit(score_text, (width - score_text.get_width() - 10, 10))


        # dibujar el texto de inicia en
        current_time = pygame.time.get_ticks()
        time_elapsed = current_time - self.start_time
        time_remaining = max(0, int((TIEMPO_ESPERA - time_elapsed) / 1000))
        instructions = fuente_vidas.render(
            '->Derecha   <-Izquierda', True, (255, 255, 255))
        time_text = fuente_vidas.render(
            'Inicia en : ' + str(time_remaining), True, (255, 255, 255))
        
# llama la verificacion del tiempo
        verificar_tiempo()
        if caida_meteoritos:
            meteoros.update()
            meteoros.draw(win)
        else:
            win.blit(instructions, (width - time_text.get_width() - 390, 10))
            win.blit(time_text, (width - time_text.get_width() - 350, 50))

        # dibuja el piso
        dibujar_piso(piso_posicion_x, piso_posicion_y)

        # Dibujar el texto en la pantalla
        win.blit(self.text, (self.x + 10, self.y - 30))

        if self.facing_left:
            win.blit(pygame.transform.flip(
                self.image, True, False), (self.x, self.y))
        else:
            win.blit(self.image, (self.x, self.y))
    #mover el personaje
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
                #baja la vida del jugador 
                vidas -= 1
                meteorito.rect.x = random.randrange(
                    0, width - meteorito.rect.width)
                meteorito.rect.y = -meteorito.rect.height
                meteorito.velocidad = random.randint(1, 5)
               
            elif meteorito.rect.bottom < self.rect.top and not meteorito.avoided:
                #aumenta la puntuacion cuando sobrepasa el limite del jugador
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
    
    if vidas == 0:
 # Establecer la posición del jugador fuera de la pantalla
        player.x = -800
        player.y = -800

    pygame.display.update()


# Función principal del programa
def main():

    run = True
    n = Network()

    DV_text = pygame.font.SysFont('comicsans', 20).render('TU', True, (255, 255, 255))
    DM_text = pygame.font.SysFont('comicsans', 20).render('OTRO', True, (255, 255, 255))
    # posicion del player
    DV_image = pygame.image.load("../assets/DV.png")
    DM_image = pygame.image.load("../assets/DM.png")

    pygame.mixer.music.load("../assets/Rip _ Tear(MP3_70K).mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(loops=-1)
    # obstaculos.generar_obstaculos(num_obstaculos=2,pantalla_ancho=piso_ancho,pantalla_alto=600)
#    obstaculos.dibujar_obstaculos(win)
    

    p = Player(jugador_posicion_x, jugador_posicion_y, 50,100, (180, 255, 255), DV_image, DV_text)
    p2 = Player(jugador_posicion_x, jugador_posicion_y,50, 100, (0, 0, 0), DM_image, DM_text)

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

        # Mover al jugador local
        p.move()

        # Dibujar los elementos en pantalla
        redrawWindow(win, p, p2)
 

pygame.mixer.init()
main()
