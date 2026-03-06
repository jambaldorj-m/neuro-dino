import pygame
import sys
from dino import Dino, DINO_HEIGHT

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 300
FPS = 60
BG_COLOR = (255, 255, 255)
GROUND_HEIGHT = 250
GROUND_COLOR = (53, 53, 53)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Neuro Dino")
    clock = pygame.time.Clock()
    
    dino = Dino(x=80, y=GROUND_HEIGHT - DINO_HEIGHT)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill(BG_COLOR)
        pygame.draw.line(screen, GROUND_COLOR, (0, GROUND_HEIGHT), (SCREEN_WIDTH, GROUND_HEIGHT), 2)
        dino.draw(screen)
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()