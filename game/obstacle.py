"""
Contains the Cactus and Bird classes.

@author: Jambaldorj Munkhsoyol
"""

import random
import pygame

CACTUS_COLOR  = (53, 53, 53)
CACTUS_WIDTH  = 20
CACTUS_HEIGHT = 50

BIRD_COLOR  = (53, 53, 53)
BIRD_WIDTH  = 40
BIRD_HEIGHT = 20

# The three possible heights a bird can fly at.
# Each one requires a different response from the dino.
BIRD_LOW  = 0 # ground level — dino must jump over it
BIRD_MID  = 1 # mid height   — dino must duck or jump
BIRD_HIGH = 2 # high up      — dino can safely run underneath

class Cactus:
    """
    A cactus obstacle that slides in from the right side of the screen.

    The dino must jump over it. Cacti always sit on the ground.
    """

    __slots__ = ["width", "height", "x", "y", "speed"]

    def __init__(self, screen_width, ground_y):
        """
        Spawn a cactus just off the right edge of the screen.

        @param screen_width: the total width of the game window — spawns just beyond it
        @param ground_y: the y coordinate of the ground line
        """
        self.width = CACTUS_WIDTH       # rectangle width
        self.height = CACTUS_HEIGHT     # rectangle height
        self.x = screen_width           # horizontal position (moves left each frame)
        self.y = ground_y - self.height # vertical position (fixed, always on the ground)
        self.speed = 6                  # how many pixels it moves left per frame

    def update(self):
        """
        Move the cactus left by its current speed.
        Called every frame by main.py.
        """
        self.x -= self.speed

    def draw(self, screen):
        """
        Draw the cactus as a filled rectangle on the given pygame surface.
        """
        pygame.draw.rect(screen, CACTUS_COLOR, (self.x, self.y, self.width, self.height))

    def is_off_screen(self):
        """
        Return True once the cactus has fully passed the left edge of the screen.
        main.py uses this to remove obstacles that no longer need to exist.
        """
        return self.x + self.width < 0
    
    def get_rect(self):
        """
        Return a pygame.Rect representing the cactus hitbox.
        Used for collision detection against the dino in main.py.
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
class Bird:
    """
    A bird obstacle that flies in from the right at one of three heights.

    Unlike the cactus, the bird's y position is random, it's chosen at spawn time.
    Each height level requires a different response from the dino:
        - BIRD_LOW:  must jump over it (same as a cactus)
        - BIRD_MID:  must duck under it, or jump over it
        - BIRD_HIGH: safe to run under, no action needed

    The AI receives the bird's y position as one of its inputs so it can
    learn to distinguish which response is appropriate.
    """

    __slots__ = ["x", "y", "width", "height", "speed"]

    def __init__(self, screen_width, ground_y):
        """
        Spawn a bird just off the right edge of the screen at a random height.

        @param screen_width: the total width of the game window
        @param ground_y: the y coordinate of the ground line
        """
        self.width = BIRD_WIDTH   # rectangle width
        self.height = BIRD_HEIGHT # rectangle height
        self.speed = 6            # how many pixels it moves left per frame

        level = random.randint(0, 2)
        if level == BIRD_LOW:
            self.y = ground_y - BIRD_HEIGHT
        elif level == BIRD_MID:
            self.y = ground_y - 60
        else:
            self.y = ground_y - 120

        self.x = screen_width

    def update(self):
        """
        Move the bird left by its current speed.
        Called every frame by main.py.
        """
        self.x -= self.speed

    def draw(self, screen):
        """
        Draw the bird as a filled rectangle on the given pygame surface.
        """
        pygame.draw.rect(screen, BIRD_COLOR, (self.x, self.y, self.width, self.height))

    def is_off_screen(self):
        """
        Return True once the bird has fully passed the left edge of the screen.
        main.py uses this to remove obstacles that no longer need to exist.
        """
        return self.x + self.width < 0

    def get_rect(self):
        """
        Return a pygame.Rect representing the bird's hitbox.
        Used for collision detection against the dino in main.py.
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)