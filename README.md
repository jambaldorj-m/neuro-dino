# Neuro Dino
A Python-based Chrome dinosaur game clone trained using a NEAT (NeuroEvolution of Augmenting Topologies) algorithm. A population of 50 dinosaurs runs simultaneously, each controlled by its own neural network brain. Over generations, the population evolves to avoid cacti and birds through survival of the fittest.

## How It Works
Each dino has a small neural network that takes in 7 inputs describing the current game state and outputs a decision: jump, duck, or do nothing. Dinos that survive longer pass their "genes" (network weights) to the next generation via mutation and selection. After enough generations, the population learns to play indefinitely.

## How to run project locally
  - Install the dependencies using "pip install pygame numpy)"
  - Run the program using "python main.py"
  - To play the game yourself, use "python game/game.py"

## Neural Network
  - Inputs (7): distance to obstacle, obstacle height, obstacle Y position, dino Y position, dino vertical velocity, game speed, is jumping
  - Hidden layer: 6 neurons with ReLU activation
  - Outputs (3): jump, duck, do nothing, highest score wins
 
## Evolution
  - Population size: 50
  - Top 20% become parents each generation
  - Top 10% survive unchanged (elites)
  - Remaining 90% are mutated copies of parents
  - Fitness score = frames survived + bonuses for passing obstacles correctly
