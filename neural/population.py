import numpy as np
from neural.genome import Genome

class Population:
    __slots__ = ["size", "genomes"]

    def __init__(self, size):
        self.size = size
        self.genomes = [Genome() for _ in range(size)]

    def evolve(self):
        # sort genomes by fitness, best first
        self.genomes.sort(key=lambda g: g.fitness, reverse=True)

        # keep the top 20% as parents
        cutoff = max(1, self.size // 5)
        parents = self.genomes[:cutoff]

        # list for next generation
        next_generation = []

        # keep top 10% unchanged (elites) — uses _copy so they're independent objects
        elite_count = max(1, self.size // 10)
        for i in range(elite_count):
            next_generation.append(self._copy(parents[i]))

        # fill the rest with mutated copies of parents
        while len(next_generation) < self.size:
            parent = parents[np.random.randint(0, len(parents))]
            child = self._copy(parent)
            child.mutate()
            next_generation.append(child)

        self.genomes = next_generation

    def _copy(self, genome):
        child = Genome()
        child.network.weights_input_hidden = genome.network.weights_input_hidden.copy()
        child.network.weights_hidden_output = genome.network.weights_hidden_output.copy()
        child.network.bias_hidden = genome.network.bias_hidden.copy()
        child.network.bias_output = genome.network.bias_output.copy()
        return child

    def best_fitness(self):
        return max(g.fitness for g in self.genomes)