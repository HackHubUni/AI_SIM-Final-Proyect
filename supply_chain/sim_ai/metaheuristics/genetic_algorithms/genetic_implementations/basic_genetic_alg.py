from ..genetic_algorithm import *
import random as rnd


class BasicGeneticAlgorithm(GeneticAlgorithm):
    """This class implements the genetic algorithm by using single point crossover"""

    def __init__(self, sample_chromosome: Chromosome) -> None:
        super().__init__(sample_chromosome)

    def selection(
        self, population: list[Chromosome]
    ) -> list[tuple[Chromosome, Chromosome]]:
        progenitor_list: list[tuple[Chromosome, Chromosome]] = []
        for _ in range(len(population)):
            idx, idy = rnd.sample(range(len(population)), 2)
            progenitor_list.append((population[idx], population[idy]))
        return progenitor_list
