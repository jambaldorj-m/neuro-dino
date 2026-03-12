"""
Can be used to play as a normal player.

@author: Jambaldorj Munkhsoyol
"""

import pygame
import sys
import random
from dino import Dino, DINO_HEIGHT
from obstacle import Cactus, Bird

SCREEN_WIDTH  = 900
SCREEN_HEIGHT = 300
FPS           = 60
BG_COLOR      = (255, 255, 255)
GROUND_HEIGHT = 250
GROUND_COLOR  = (53, 53, 53)

# How much speed increases every frame.
SPEED_INCREMENT = 0.005

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Neuro Dino")
    clock = pygame.time.Clock()
    font  = pygame.font.Font(None, 30)

    # place the dino so its feet sit exactly on the ground line
    dino = Dino(x=80, y=GROUND_HEIGHT - DINO_HEIGHT)

    obstacles      = []
    spawn_timer    = 0
    score          = 0
    spawn_interval = 90 # frames between obstacle spawns (randomized after first)

    # Single source of truth for speed.
    # Every obstacle reads from this variable each frame so they all
    # move at the same rate, no obstacle ever drifts ahead or behind.
    speed   = 6.0
    running = True

    while running:
        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        running = False
                    case pygame.K_SPACE | pygame.K_UP:
                        dino.jump()
                    case pygame.K_DOWN:
                        dino.duck()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    dino.stop_duck()

        # UPDATING
        speed += SPEED_INCREMENT
        score += 1

        # spawn a new obstacle when the timer expires
        spawn_timer += 1
        if spawn_timer >= spawn_interval:
            if random.random() < 0.3:
                obstacles.append(Bird(SCREEN_WIDTH, GROUND_HEIGHT))
            else:
                obstacles.append(Cactus(SCREEN_WIDTH, GROUND_HEIGHT))

            # give the newly spawned obstacle the current speed immediately
            obstacles[-1].speed = speed

            spawn_timer    = 0
            spawn_interval = random.randint(60, 150) # randomize gap until next spawn

        # update the dino's physics (gravity, position)
        dino.update()

        # Sync every obstacle to the global speed, then advance their position.
        # Setting obs.speed every frame (rather than just at spawn) ensures
        # all obstacles accelerate together as speed increases.
        for obs in obstacles:
            obs.speed = speed
            obs.update()

        # remove obstacles that have fully passed the left edge
        obstacles = [obs for obs in obstacles if not obs.is_off_screen()]

        # collision detection
        for obs in obstacles:
            if dino.get_rect().colliderect(obs.get_rect()):
                running = False

        # DRAWING
        screen.fill(BG_COLOR)

        # ground line
        pygame.draw.line(screen, GROUND_COLOR, (0, GROUND_HEIGHT), (SCREEN_WIDTH, GROUND_HEIGHT), 2)

        dino.draw(screen)

        for obs in obstacles:
            obs.draw(screen)

        # score displayed in top-left corner
        score_text = font.render(f"Score: {int(score)}", True, (53, 53, 53))
        screen.blit(score_text, (20, 20))

        # Flip pushes everything drawn this frame onto the actual display.
        # Without this, nothing would appear on screen.
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()