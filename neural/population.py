"""
Represents the entire group of dinos, and the evolution logic.

@author: Jambaldorj Munkhsoyol
"""

import numpy as np
from neural.genome import Genome

class Population:
    """
    Holds all genomes (dino brains) and manages evolution between generations.
    """

    __slots__ = ["size", "genomes"]

    def __init__(self, size):
        """
        Create a fresh population of randomly initialized genomes.

        @param size: how many dinos to run per generation (e.g. 50)
        """
        self.size = size                               # total number of dinos
        self.genomes = [Genome() for _ in range(size)] # the list of Genome objects, one per dino

    def evolve(self):
        """
        Breed a new generation from the current one.
        """
        # sort genomes by fitness, best first
        self.genomes.sort(key=lambda g: g.fitness, reverse=True)

        # keep the top 20% as parents
        cutoff = max(1, self.size // 5)
        parents = self.genomes[:cutoff]

        # list for next generation
        next_generation = []

        # keep top 10% unchanged (elites)
        elite_count = max(1, self.size // 10)
        for i in range(elite_count):
            next_generation.append(self._copy(parents[i]))

        # fill the rest with mutated copies of parents
        while len(next_generation) < self.size:
            parent = parents[np.random.randint(0, len(parents))]
            child = self._copy(parent)
            child.mutate()
            next_generation.append(child)

        # replace the old generation
        self.genomes = next_generation

        # reset fitness scores
        for g in self.genomes:
            g.fitness = 0

    def _copy(self, genome):
        """
        Return a new Genome whose network weights are independent copies
        of the given genome's weights.

        @param genome: the Genome to copy
        @returns: a new Genome with identical but independent weights
        """
        child = Genome()
        child.network.weights_input_hidden = genome.network.weights_input_hidden.copy()
        child.network.weights_hidden_output = genome.network.weights_hidden_output.copy()
        child.network.bias_hidden           = genome.network.bias_hidden.copy()
        child.network.bias_output           = genome.network.bias_output.copy()
        return child

    def best_fitness(self):
        """
        Return the highest fitness score in the current generation.
        Useful for tracking progress.
        """
        return max(g.fitness for g in self.genomes)