import random
import pygame

CACTUS_COLOR = (53, 53, 53)
CACTUS_WIDTH = 20
CACTUS_HEIGHT = 50

class Cactus:
    __slots__ = ["width", "height", "x", "y", "speed"]

    def __init__(self, screen_width, ground_y):
        self.width = CACTUS_WIDTH
        self.height = CACTUS_HEIGHT
        self.x = screen_width
        self.y = ground_y - self.height
        self.speed = 6

    def update(self):
        self.x -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, CACTUS_COLOR, (self.x, self.y, self.width, self.height))

    def is_off_screen(self):
        return self.x + self.width < 0