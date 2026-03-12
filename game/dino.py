import pygame

DINO_WIDTH = 40
DINO_HEIGHT = 50
DINO_DUCK_WIDTH = 60
DINO_DUCK_HEIGHT = 25
DINO_COLOR = (53, 53, 53)
GRAVITY = 1.2
JUMP_VELOCITY = -18

class Dino:
    __slots__ = ["x", "y", "width", "height", "ground_y", "velocity_y", "is_jumping", "is_ducking"]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = DINO_WIDTH
        self.height = DINO_HEIGHT
        self.ground_y = y + DINO_HEIGHT # store the raw ground line
        self.velocity_y = 0
        self.is_jumping = False
        self.is_ducking = False

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = JUMP_VELOCITY
            self.is_jumping = True

    def duck(self):
        self.is_ducking = True
        self.width = DINO_DUCK_WIDTH
        self.height = DINO_DUCK_HEIGHT
        if self.is_jumping:
            self.velocity_y = 10
        else:
            self.y = self.ground_y - self.height

    def stop_duck(self):
        if self.is_ducking:
            self.is_ducking = False
            self.width = DINO_WIDTH
            self.height = DINO_HEIGHT
            self.y = self.ground_y - self.height

    def update(self):
        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        if self.y >= self.ground_y - self.height:
            self.y = self.ground_y - self.height
            self.velocity_y = 0
            self.is_jumping = False

    def draw(self, screen):
        pygame.draw.rect(screen, DINO_COLOR, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)