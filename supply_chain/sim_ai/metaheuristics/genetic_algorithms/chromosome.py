from gene import *


class Chromosome:
    """Base class for all chromosomes"""

    def __init__(
        self,
        genes: list[Gene],
        maximization_problem: bool,
    ) -> None:
        if genes is None or len(genes) == 0:
            raise Exception(f"The genes parameter is None or is empty")
        self.genes: list[Gene] = genes
        """The list of all the genes"""
        self.maximization_problem: bool = maximization_problem
        """Represents if the problem is a maximization problem"""

    @abstractmethod
    def mate(self, other: Self) -> Self:
        """This method mates two chromosomes and generate a new chromosome child"""
        pass

    @abstractmethod
    def mutate(self, mutation_rate: float = 0.3):
        """Mutate this chromosome in place"""
        pass

    @abstractmethod
    def calculate_fitness(self) -> float:
        """A function for calculate the fitness of this chromosome"""
        pass

    def get_solution(self):
        """This method converts the genes in a solution of the domain problem"""
        pass

    @abstractmethod
    def clone(self, with_mutation: bool) -> Self:
        """Returns a clone of this chromosome"""
        pass

    def equal(self, other_chromosome: Self) -> bool:
        """Says if two chromosomes are equals, meaning that they could mate"""
        return len(self.genes) == len(other_chromosome.genes) and all(
            gene1 == gene2 for gene1, gene2 in zip(self.genes, other_chromosome.genes)
        )
