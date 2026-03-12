"""
The dino game for the AI to be played.

@author: Jambaldorj Munkhsoyol
"""

import pygame
import sys
from game.dino import Dino, DINO_HEIGHT
from game.obstacle import Cactus, Bird
from neural.population import Population
import random

SCREEN_WIDTH    = 900
SCREEN_HEIGHT   = 300
FPS             = 60
BG_COLOR        = (255, 255, 255)
GROUND_HEIGHT   = 250
GROUND_COLOR    = (53, 53, 53)
POPULATION_SIZE = 50

def get_inputs(dino, obstacles, speed):
    """
    Build the 7-value input list that gets fed into a dino's neural network.

    All values are normalized.

    @param dino: the Dino object for this specific dino
    @param obstacles: the current list of active obstacles (already sorted left-to-right)
    @param speed: the current global game speed
    @returns: list of 7 floats, all roughly in the 0–1 range
    """
    if obstacles:
        nearest = obstacles[0]
        dist = nearest.x - dino.x
        obstacle_height = nearest.height
        obstacle_y = nearest.y
    else:
        dist = SCREEN_WIDTH
        obstacle_height = 0
        obstacle_y = GROUND_HEIGHT

    return [
        dist / SCREEN_WIDTH,             # distance to nearest obstacle
        obstacle_height / SCREEN_HEIGHT, # height of nearest obstacle
        obstacle_y / SCREEN_HEIGHT,      # y position of nearest obstacle
        dino.y / SCREEN_HEIGHT,          # dino's current y position
        dino.velocity_y / 20,            # dino's vertical velocity
        speed / 20,                      # current game speed
        1 if dino.is_jumping else 0      # is dino jumping?
    ]

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Neuro Dino")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)

    # Create the population once, it persists across all generations.
    # evolve() updates it in place, so we never recreate it.
    population = Population(POPULATION_SIZE)
    generation = 1

    while True:
        dinos = [Dino(x=80, y=GROUND_HEIGHT - DINO_HEIGHT) for _ in range(POPULATION_SIZE)]
        alive = list(range(POPULATION_SIZE))
        passed_obstacles = [set() for _ in range(POPULATION_SIZE)]

        obstacles      = []
        spawn_timer    = 0
        spawn_interval = 90 # frames until first obstacle
        speed          = 6.0
        score          = 0

        running = True
        while running:
            # EVENTS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            # UPDATE
            score += 1
            speed += 0.005

            # spawn a new obstacle when the timer expires
            spawn_timer += 1
            if spawn_timer >= spawn_interval:
                if random.random() < 0.3:
                    obstacles.append(Bird(SCREEN_WIDTH, GROUND_HEIGHT))
                else:
                    obstacles.append(Cactus(SCREEN_WIDTH, GROUND_HEIGHT))

                # immediately give the new obstacle the current speed
                obstacles[-1].speed = speed
                spawn_timer    = 0
                spawn_interval = random.randint(40, 150)

            # sync all obstacles to global speed, then advance their position
            for obs in obstacles:
                obs.speed = speed
                obs.update()

            # remove obstacles that have fully left the screen
            obstacles = [obs for obs in obstacles if not obs.is_off_screen()]

            # AI DECISIONS
            for i in alive[:]:
                inputs   = get_inputs(dinos[i], obstacles, speed)
                decision = population.genomes[i].decide(inputs)

                if decision == 0:
                    # jump
                    dinos[i].stop_duck()
                    dinos[i].jump()
                elif decision == 1:
                    # duck
                    dinos[i].duck()
                else:
                    # do nothing or release duck if it was being held
                    dinos[i].stop_duck()

                dinos[i].update()

                population.genomes[i].fitness += 1

                for obs in obstacles:
                    obs_id = id(obs)
                    if obs.x + obs.width < dinos[i].x and obs_id not in passed_obstacles[i]:
                        passed_obstacles[i].add(obs_id)

                        if isinstance(obs, Bird) and obs.y < GROUND_HEIGHT - 40:
                            if dinos[i].is_ducking:
                                population.genomes[i].fitness += 100 # reward correct duck
                            elif dinos[i].is_jumping:
                                population.genomes[i].fitness -= 30 # penalize unnecessary jump
                        else:
                            population.genomes[i].fitness += 50

                # collision check
                for obs in obstacles:
                    if dinos[i].get_rect().colliderect(obs.get_rect()):
                        alive.remove(i)
                        break

            # END OF GENERATION
            if not alive:
                population.evolve()
                generation += 1
                running = False

            # DRAW
            screen.fill(BG_COLOR)

            # ground line
            pygame.draw.line(screen, GROUND_COLOR, (0, GROUND_HEIGHT), (SCREEN_WIDTH, GROUND_HEIGHT), 2)

            for i in alive:
                dinos[i].draw(screen)

            for obs in obstacles:
                obs.draw(screen)

            score_text = font.render(f"Score: {int(score)}", True, GROUND_COLOR)
            gen_text = font.render(f"Generation: {generation}", True, GROUND_COLOR)
            alive_text = font.render(f"Alive: {len(alive)}/{POPULATION_SIZE}", True, GROUND_COLOR)
            screen.blit(score_text, (20, 20))
            screen.blit(gen_text, (20, 45))
            screen.blit(alive_text, (20, 70))

            pygame.display.flip()
            clock.tick(FPS)

if __name__ == "__main__":
    main()