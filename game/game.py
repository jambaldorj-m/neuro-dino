import pygame
import sys

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 400
FPS = 60
BG_COLOR = (255, 255, 255)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Neuro Dino")
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill(BG_COLOR)
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()