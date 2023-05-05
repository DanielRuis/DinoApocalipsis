import pygame
import random

    # Definir el tamaño de la pantalla
width = 800
height = 600


meteorito_img = pygame.image.load("../assets/met.png")
# clase meteorito
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
