import pygame

DINO_WIDTH = 40
DINO_HEIGHT = 50
DINO_COLOR = (53, 53, 53)

class Dino:
    __slots__ = ["x", "y", "width", "height"]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = DINO_WIDTH
        self.height = DINO_HEIGHT

    def draw(self, screen):
        pygame.draw.rect(screen, DINO_COLOR, (self.x, self.y, self.width, self.height))