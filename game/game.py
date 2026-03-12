import pygame
import sys
import random
from game.dino import Dino, DINO_HEIGHT
from game.obstacle import Cactus, Bird

SCREEN_WIDTH   = 900
SCREEN_HEIGHT  = 300
FPS            = 60
BG_COLOR       = (255, 255, 255)
GROUND_HEIGHT  = 250
GROUND_COLOR   = (53, 53, 53)
SPEED_INCREMENT = 0.005

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Neuro Dino")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)

    dino = Dino(x=80, y=GROUND_HEIGHT - DINO_HEIGHT)

    obstacles = []
    spawn_timer = 0
    score = 0
    spawn_interval = 90
    # single source of truth for speed - obstacles read from this
    speed = 6.0
    running = True

    while running:
        # handling events
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

        # updating part
        speed += SPEED_INCREMENT
        score += 1

        spawn_timer += 1
        if spawn_timer >= spawn_interval:
            if random.random() < 0.3:
                obstacles.append(Bird(SCREEN_WIDTH, GROUND_HEIGHT))
            else:
                obstacles.append(Cactus(SCREEN_WIDTH, GROUND_HEIGHT))
            obstacles[-1].speed = speed
            spawn_timer = 0
            spawn_interval = random.randint(60, 150)

        dino.update()

        for obs in obstacles:
            # keep all obstacles in sync with the global speed
            obs.speed = speed
            obs.update()

        obstacles = [obs for obs in obstacles if not obs.is_off_screen()]

        for obs in obstacles:
            if dino.get_rect().colliderect(obs.get_rect()):
                running = False

        # drawing part
        screen.fill(BG_COLOR)
        pygame.draw.line(screen, GROUND_COLOR, (0, GROUND_HEIGHT), (SCREEN_WIDTH, GROUND_HEIGHT), 2)
        dino.draw(screen)
        for obs in obstacles:
            obs.draw(screen)

        score_text = font.render(f"Score: {int(score)}", True, (53, 53, 53))
        screen.blit(score_text, (20, 20))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()