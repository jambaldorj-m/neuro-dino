import random
import pygame

CACTUS_COLOR = (53, 53, 53)
CACTUS_WIDTH = 20
CACTUS_HEIGHT = 50

BIRD_COLOR = (53, 53, 53)
BIRD_WIDTH = 40
BIRD_HEIGHT = 20

BIRD_LOW = 0  # ground level, must jump
BIRD_MID = 1  # mid height, must duck or jump
BIRD_HIGH = 2 # high up, safe to run under

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
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
class Bird:
    __slots__ = ["x", "y", "width", "height", "speed"]

    def __init__(self, screen_width, ground_y):
        self.width = BIRD_WIDTH
        self.height = BIRD_HEIGHT
        self.speed = 6

        level = random.randint(0, 2)
        if level == BIRD_LOW:
            self.y = ground_y - BIRD_HEIGHT
        elif level == BIRD_MID:
            self.y = ground_y - 60
        else:
            self.y = ground_y - 120

        self.x = screen_width

    def update(self):
        self.x -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, BIRD_COLOR, (self.x, self.y, self.width, self.height))

    def is_off_screen(self):
        return self.x + self.width < 0

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)