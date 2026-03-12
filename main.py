import pygame
import sys
from game.dino import Dino, DINO_HEIGHT
from game.obstacle import Cactus, Bird
from neural.population import Population
import random

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 300
FPS = 60
BG_COLOR = (255, 255, 255)
GROUND_HEIGHT = 250
GROUND_COLOR = (53, 53, 53)
POPULATION_SIZE = 50

def get_inputs(dino, obstacles, speed):
    if obstacles:
        nearest = obstacles[0]
        dist = nearest.x - dino.x
        cactus_height = nearest.height
        nearest_y = nearest.y
    else:
        dist = SCREEN_WIDTH
        cactus_height = 0
        nearest_y = GROUND_HEIGHT

    return [
        dist / SCREEN_WIDTH,           # distance to next cactus (normalized)
        cactus_height / SCREEN_HEIGHT, # height of next cactus (normalized)
        nearest_y / SCREEN_HEIGHT,     # height of nearest obstacle (normalized)
        dino.y / SCREEN_HEIGHT,        # dino's current y position (normalized)
        dino.velocity_y / 20,          # dino's vertical velocity (normalized)
        speed / 20,                    # current game speed (normalized)
        1 if dino.is_jumping else 0    # 1 if dino is jumping, else 0
    ]

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Neuro Dino")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)

    population = Population(POPULATION_SIZE)
    generation = 1

    while True:
        # the setup for this generation
        dinos = [Dino(x=80, y=GROUND_HEIGHT - DINO_HEIGHT) for _ in range(POPULATION_SIZE)]
        alive = list(range(POPULATION_SIZE))  # indices of dinos still alive
        obstacles = []
        spawn_timer = 0
        spawn_interval = 90
        speed = 6
        score = 0

        running = True
        while running:
            # handling events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            # update
            score += 1
            speed += 0.005

            spawn_timer += 1
            if spawn_timer >= spawn_interval:
                if random.random() < 0.3: # 30% chance of bird, 70% cactus
                    obstacles.append(Bird(SCREEN_WIDTH, GROUND_HEIGHT))
                else:
                    obstacles.append(Cactus(SCREEN_WIDTH, GROUND_HEIGHT))
                obstacles[-1].speed = speed
                spawn_timer = 0
                spawn_interval = random.randint(60, 150)

            for obs in obstacles:
                obs.update()
            obstacles = [obs for obs in obstacles if not obs.is_off_screen()]

            # AI decisions
            for i in alive[:]:
                inputs = get_inputs(dinos[i], obstacles, speed)
                decision = population.genomes[i].decide(inputs)
                if decision == 0:
                    dinos[i].jump()
                    dinos[i].stop_duck()
                elif decision == 1:
                    dinos[i].duck()
                else:
                    dinos[i].stop_duck()
                dinos[i].update()
                population.genomes[i].fitness = score

                # check collision
                for obs in obstacles:
                    if dinos[i].get_rect().colliderect(obs.get_rect()):
                        alive.remove(i)
                        break

            # all dinos dead -> evolve
            if not alive:
                population.evolve()
                generation += 1
                running = False

            # draw
            screen.fill(BG_COLOR)
            pygame.draw.line(screen, GROUND_COLOR, (0, GROUND_HEIGHT), (SCREEN_WIDTH, GROUND_HEIGHT), 2)

            for i in alive:
                dinos[i].draw(screen)
            for obs in obstacles:
                obs.draw(screen)

            score_text = font.render(f"Score: {int(score)}", True, (53, 53, 53))
            gen_text = font.render(f"Generation: {generation}", True, (53, 53, 53))
            alive_text = font.render(f"Alive: {len(alive)}/{POPULATION_SIZE}", True, (53, 53, 53))
            screen.blit(score_text, (20, 20))
            screen.blit(gen_text, (20, 45))
            screen.blit(alive_text, (20, 70))

            pygame.display.flip()
            clock.tick(FPS)

if __name__ == "__main__":
    main()