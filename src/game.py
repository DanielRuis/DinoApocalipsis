import pygame
import random

# Inicializar Pygame
pygame.init()

# Definir los colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)

# Definir la pantalla
pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Juego de plataforma")

# Definir el reloj para controlar la velocidad de los fotogramas
reloj = pygame.time.Clock()

# Definir la posición y la velocidad del jugador
jugador_ancho = 50
jugador_alto = 50
jugador_posicion_x = 375
jugador_posicion_y = 525
jugador_velocidad = 0

# Definir la posición y el tamaño del piso
piso_ancho = 800
piso_alto = 50
piso_posicion_x = 0
piso_posicion_y = 575

# Definir la posición, el tamaño y la velocidad de los meteoritos
meteorito_ancho = 50
meteorito_alto = 50
meteorito_posiciones_x = []
meteorito_posiciones_y = []
meteorito_velocidades = []
num_meteoritos = 10
velocidad_meteoritos = 2
for i in range(num_meteoritos):
    meteorito_posiciones_x.append(random.randint(0, 750))
    meteorito_posiciones_y.append(random.randint(-200, -50))
    meteorito_velocidades.append(velocidad_meteoritos)

# Definir el contador de vidas
vidas = 3

# Definir el nivel de dificultad
nivel = "Fácil"

# Función para dibujar el jugador en la pantalla
def dibujar_jugador(x, y):
    pygame.draw.rect(pantalla, BLANCO, [x, y, jugador_ancho, jugador_alto])

# Función para dibujar el piso en la pantalla
def dibujar_piso(x, y):
    pygame.draw.rect(pantalla, BLANCO, [x, y, piso_ancho, piso_alto])

# Función para dibujar los meteoritos en la pantalla
def dibujar_meteoritos():
    for i in range(num_meteoritos):
        pygame.draw.rect(pantalla, ROJO, [meteorito_posiciones_x[i], meteorito_posiciones_y[i], meteorito_ancho, meteorito_alto])
        
# Bucle principal del juego
terminado = False
while not terminado:
    # Manejar eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            terminado = True
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_velocidad = -5
            elif evento.key == pygame.K_RIGHT:
                jugador_velocidad = 5
        elif evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_velocidad = 0

    # Mover el jugador
    jugador_posicion_x += jugador_velocidad

    # Mover los meteoritos y comprobar si colisionan
    for i in range(num_meteoritos):
        meteorito_posiciones_y[i] += meteorito_velocidades[i]
        if meteorito_posiciones_y[i] > 600:
            meteorito_posiciones_x[i] = random.randint(0, 750)
            meteorito_posiciones_y[i] = random.randint(-200, -50)
            meteorito_velocidades[i] = velocidad_meteoritos
        if jugador_posicion_x < meteorito_posiciones_x[i] + meteorito_ancho and \
           jugador_posicion_x + jugador_ancho > meteorito_posiciones_x[i] and \
           jugador_posicion_y < meteorito_posiciones_y[i] + meteorito_alto and \
           jugador_posicion_y + jugador_alto > meteorito_posiciones_y[i]:
            vidas -= 1
            meteorito_posiciones_x[i] = random.randint(0, 750)
            meteorito_posiciones_y[i] = random.randint(-200, -50)
            meteorito_velocidades[i] = velocidad_meteoritos
        if nivel == "Medio":
            velocidad_meteoritos = 3
            if vidas < 3:
                vidas += 1
        elif nivel == "Difícil":
            velocidad_meteoritos = 4
            if vidas < 3:
                vidas += 1
        if meteorito_posiciones_y[i] > 525:
            meteorito_posiciones_x[i] = random.randint(0, 750)
            meteorito_posiciones_y[i] = random.randint(-200, -50)
            meteorito_velocidades[i] = velocidad_meteoritos
            vidas -= 1

    # Dibujar el fondo
    pantalla.fill(NEGRO)

    # Dibujar el piso, el jugador, los meteoritos y el contador de vidas
    dibujar_piso(piso_posicion_x, piso_posicion_y)
    dibujar_jugador(jugador_posicion_x, jugador_posicion_y)
    dibujar_meteoritos()
    fuente = pygame.font.SysFont("arial", 20)
    texto_vidas = fuente.render("Vidas: " + str(vidas), True, BLANCO)
    pantalla.blit(texto_vidas, (10, 10))

    # Actualizar el nivel de dificultad
    if vidas == 0:
        nivel = "Fácil"
        vidas = 3
        velocidad_meteoritos = 2
    elif vidas == 1 or vidas == 2:
        nivel = "Medio"
    elif vidas == 3:
        nivel = "Difícil"

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad de los fotogramas
    reloj.tick(60)

# Salir de Pygame
pygame.quit()
