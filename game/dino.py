import pygame

DINO_WIDTH = 40
DINO_HEIGHT = 50
DINO_COLOR = (53, 53, 53)

GRAVITY = 1.2
JUMP_VELOCITY = -18

class Dino:
    __slots__ = ["x", "y", "width", "height", "ground_y", "velocity_y", "is_jumping"]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = DINO_WIDTH
        self.height = DINO_HEIGHT
        self.ground_y = y
        self.velocity_y = 0
        self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = JUMP_VELOCITY
            self.is_jumping = True

    def update(self):
        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        if self.y >= self.ground_y:
            self.y = self.ground_y
            self.velocity_y = 0
            self.is_jumping = False

    def draw(self, screen):
        pygame.draw.rect(screen, DINO_COLOR, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)