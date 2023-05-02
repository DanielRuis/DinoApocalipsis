# import random
# import pygame

# class Obstaculos(pygame.sprite.Sprite):
#     VELOCIDAD_INICIAL = 5

#     def __init__(self, x, y):
#         super().__init__()
#         self.image = pygame.Surface((50, 50))
#         self.image.fill((255, 0, 0))
#         self.rect = self.image.get_rect()
#         self.rect.x = x
#         self.rect.y = y
#         self.velocidad = Obstaculos.VELOCIDAD_INICIAL

#     def mover(self):
#         self.rect.y += self.velocidad

# class Juego:

#     FPS = 60
#     ANCHO = 800
#     ALTO = 600
#     INCREMENTO_VELOCIDAD = 1

#     def __init__(self):
#         pygame.init()
#         self.pantalla = pygame.display.set_mode((Juego.ANCHO, Juego.ALTO))
#         self.reloj = pygame.time.Clock()
#         self.obstaculos = pygame.sprite.Group()
#         self.tiempo_transcurrido = 0
#         self.puntuacion = 0
#         self.obstaculos = Obstaculos()

#     def generar_obstaculos(self, num_obstaculos):
#         for i in range(num_obstaculos):
#             x = random.randint(0, Juego.ANCHO - 50)
#             y = random.randint(-Juego.ALTO, -50)
#             obstaculo = Obstaculos(x, y)
#             self.obstaculos.add(obstaculo)

#     def dibujar_obstaculos(self):
#         self.obstaculos.draw(self.pantalla)
#         self.tiempo_transcurrido += self.reloj.tick(Juego.FPS) / 1000.0
#         if self.tiempo_transcurrido >= 10:
#             for obstaculo in self.obstaculos:
#                 obstaculo.velocidad += Juego.INCREMENTO_VELOCIDAD
#             self.tiempo_transcurrido = 0

#     def actualizar_obstaculos(self):
#         for obstaculo in self.obstaculos:
#             obstaculo.mover()
#             if obstaculo.rect.top > Juego.ALTO:
#                 self.obstaculos.remove(obstaculo)
#                 self.puntuacion += 1
#         while len(self.obstaculos) < 5:
#             self.generar_obstaculos(1)

#     def bucle_principal(self):
#         game_over = False
#         while not game_over:
#             for evento in pygame.event.get():
#                 if evento.type == pygame.QUIT:
#                     game_over = True
#             self.pantalla.fill((255, 255, 255))
#             self.dibujar_obstaculos()



import random
import pygame


class Obstaculos(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 10, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad_y = 0.1  # velocidad vertical inicial
    
    def update(self):
        self.rect.y += self.velocidad_y  # actualizar posición vertical
        self.velocidad_y += 0.1  # aumentar velocidad vertical

def generar_obstaculos(num_obstaculos, pantalla_ancho, pantalla_alto):
    obstaculos = pygame.sprite.Group()
    for i in range(num_obstaculos):
        x = random.randint(0, pantalla_ancho - 10)
        y = random.randint(0, pantalla_alto - 10)
        obstaculo = Obstaculos(x, y)
        obstaculos.add(obstaculo)
    return obstaculos

def dibujar_obstaculos(win):
    obstaculos = generar_obstaculos(5, win.get_width(), win.get_height())
    for obstaculo in obstaculos:
        obstaculo.update()
    obstaculos.draw(win)
    return obstaculos



    

# import random
# import pygame

# def juego_de_objetos_que_caen(frecuencia_creación_objetos=60, intervalo_tiempo=10):
#     # Definir colores
#     ROJO = (255, 0, 0)

#     # Definir velocidad inicial de caída de los objetos
#     velocidad_caída = 1

#     # Definir clase para los objetos que caen
#     class ObjetoQueCae(pygame.sprite.Sprite):
#         def __init__(self):
#             super().__init__()
#             self.image = pygame.Surface([50, 50])
#             self.image.fill(ROJO)
#             self.rect = self.image.get_rect()
#             self.rect.x = random.randint(0, 600 - self.rect.width)
#             self.rect.y = -self.rect.height

#         def update(self):
#             self.rect.y += velocidad_caída

#     # Crear grupo de sprites para los objetos que caen
#     grupo_objetos_que_caen = pygame.sprite.Group()

#     # Definir variables para controlar la creación de objetos que caen
#     contador_creación_objetos = 0

#     # Definir variables para controlar el aumento de velocidad
#     tiempo_transcurrido = 0

#     while True:
#         # Crear nuevos objetos que caen
#         contador_creación_objetos += 1
#         if contador_creación_objetos == frecuencia_creación_objetos:
#             nuevo_objeto_que_cae = ObjetoQueCae()
#             grupo_objetos_que_caen.add(nuevo_objeto_que_cae)
#             contador_creación_objetos = 0

#         # Actualizar objetos que caen
#         grupo_objetos_que_caen.update()

#         # Actualizar el tiempo transcurrido
#         tiempo_transcurrido += 1

#         # Aumentar velocidad de caída de los objetos después de cierto intervalo de tiempo
#         if tiempo_transcurrido >= intervalo_tiempo:
#             velocidad_caída += 1
#             tiempo_transcurrido = 0

#         # Devolver los objetos que caen como una lista
#         obstaculos = [objeto_que_cae.rect for objeto_que_cae in grupo_objetos_que_caen]

#         # Salir del bucle si no quedan objetos que caen
#         if not obstaculos:
#             break

#     # Devolver la lista de obstáculos
#     return obstaculos
