import pygame
import random

# Definir el tamaño de la pantalla
width = 800
height = 600

# Inicializar pygame
pygame.init()

# Crear la ventana
screen = pygame.display.set_mode((width, height))

# Cargar la imagen del meteorito
meteorito_img = pygame.image.load("../assets/met.png")

# Definir la clase Meteorito
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

# Variables globales
tiempo_anterior = pygame.time.get_ticks()  # Tiempo en milisegundos desde que se inició el juego
tiempo_aumento_velocidad = 10000  # 10 segundos en milisegundos
velocidad_inicial = 1
incremento_velocidad = 1

# Crear un grupo para los meteoritos
meteoritos_group = pygame.sprite.Group()

# Crear meteoritos y agregarlos al grupo
for i in range(1):
    meteorito = Meteorito()
    meteoritos_group.add(meteorito)

# Bucle principal del juego
while True:
    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Actualizar meteoritos
    meteoritos_group.update()

    # Verificar si ha pasado el tiempo necesario para aumentar la velocidad
    tiempo_actual = pygame.time.get_ticks()
    if tiempo_actual - tiempo_anterior >= tiempo_aumento_velocidad:
        tiempo_anterior = tiempo_actual  # Actualizar el tiempo anterior
        for meteorito in meteoritos_group:
            meteorito.velocidad += incremento_velocidad  # Aumentar la velocidad de cada meteorito

    # Dibujar los meteoritos en la pantalla
    screen.fill((0, 0, 0))
    meteoritos_group.draw(screen)

    # Actualizar la pantalla
    pygame.display.flip()
