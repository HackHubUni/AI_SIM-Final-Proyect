from chromosome import *


class GeneticAlgorithm(ABC):
    """Base class for all implementations of Genetic Algorithms"""

    def __init__(self, sample_chromosome: Chromosome) -> None:
        self.sample_chromosome: Chromosome = sample_chromosome
        """The chromosome that represents a solution in the genetic algorithm"""
        self.maximization_problem: bool = self.sample_chromosome.maximization_problem
        """Tells if the problem to solve is a maximization problem"""

    @abstractmethod
    def selection(
        self,
        population: list[Chromosome],
    ) -> list[tuple[Chromosome, Chromosome]]:
        """This method returns a list of tuples where each tuple represents the parents to mate.
        Remember each chromosome has the fitness function inside"""
        pass

    def mate_population(self, population: list[Chromosome]) -> list[Chromosome]:
        """This method generate a new population of individuals from a population.
        This method calls internally the selection and the cross_over method"""
        new_population: list[Chromosome] = []
        parents: list[tuple[Chromosome, Chromosome]] = self.selection(population)
        for parent1, parent2 in parents:
            child: Chromosome = parent1.mate(parent2)
            new_population.append(child)
        return new_population

    @abstractmethod
    def solve(
        self,
        population_size: int,
        max_iterations: int,
        stop_criteria: Callable[[float], bool],
    ) -> Chromosome:
        """This method returns the best chromosome for the problem"""
        pass
