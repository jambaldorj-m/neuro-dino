"""
Contains the Dino class that represents a dino in the game.

@author: Jambaldorj Munkhsoyol
"""

import pygame

# standing dino size
DINO_WIDTH  = 40
DINO_HEIGHT = 50

# ducking dino size (wider and shorter)
DINO_DUCK_WIDTH  = 60
DINO_DUCK_HEIGHT = 25

DINO_COLOR = (53, 53, 53)

# added to velocity_y every frame, so the dino accelerates downward over time
GRAVITY = 1.2

# The upward velocity applied when the dino jumps.
# Negative because in pygame, y=0 is the top of the screen so moving up
# means decreasing y, which means a negative velocity.
JUMP_VELOCITY = -18

class Dino:
    """
    Represents a single dino in the game.

    Handles its own physics (jumping, gravity, ducking) and drawing.
    Does NOT make AI decisions — that happens in main.py.
    The AI calls jump(), duck(), or stop_duck() based on its decision,
    then update() is called every frame to apply physics.
    """

    __slots__ = ["x", "y", "width", "height", "ground_y", "velocity_y", "is_jumping", "is_ducking"]

    def __init__(self, x, y):
        """
        Create a new dino at position (x, y).

        y should be passed as GROUND_HEIGHT - DINO_HEIGHT so the dino
        sits on top of the ground line rather than below it.
        """
        self.x = x                      # horizontal position of dino (fixed, never moves left or right)
        self.y = y                      # vertical position of dino (top-left corner of the rectangle)
        self.width = DINO_WIDTH         # width of dino
        self.height = DINO_HEIGHT       # heigth of dino
        self.ground_y = y + DINO_HEIGHT # the y coordinate of the ground line, never changes
        self.velocity_y = 0             # current vertical speed, positive = moving down
        self.is_jumping = False         # True while the dino is in the air
        self.is_ducking = False         # True while the dino is ducking

    def jump(self):
        """
        Make the dino jump by giving it an upward velocity.

        The is_jumping guard prevents double-jumping — once in the air,
        calling jump() again does nothing until the dino lands.
        """
        if not self.is_jumping:
            self.velocity_y = JUMP_VELOCITY
            self.is_jumping = True

    def duck(self):
        """
        Make the dino crouch.

        Two things happen depending on whether the dino is in the air:
            - On the ground: shrink the hitbox and snap y down so it stays grounded
            - In the air:    push velocity_y to 10 (fast drop) so it falls quickly

        This method is called every frame the AI decides to duck, not just once,
        so the fast-drop velocity keeps applying during a mid-air duck.
        """
        self.is_ducking = True
        self.width = DINO_DUCK_WIDTH
        self.height = DINO_DUCK_HEIGHT
        if self.is_jumping:
            self.velocity_y = 10
        else:
            self.y = self.ground_y - self.height

    def stop_duck(self):
        """
        Return the dino to its standing size.

        Only does anything if the dino is currently ducking, avoids
        redundantly resetting values every frame when already standing.
        """
        if self.is_ducking:
            self.is_ducking = False
            self.width = DINO_WIDTH
            self.height = DINO_HEIGHT
            self.y = self.ground_y - self.height

    def update(self):
        """
        Apply physics and advance the dino by one frame.

        Called every frame regardless of what the AI decided.
        Gravity always pulls the dino down. If it reaches the ground,
        we stop it there and reset the jump state.
        """
        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        if self.y >= self.ground_y - self.height:
            self.y = self.ground_y - self.height
            self.velocity_y = 0
            self.is_jumping = False

    def draw(self, screen):
        """
        Draw the dino as a filled rectangle on the given pygame surface.
        """
        pygame.draw.rect(screen, DINO_COLOR, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        """
        Return a pygame.Rect representing the dino's current hitbox.
        Used for collision detection against obstacles in main.py.
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)