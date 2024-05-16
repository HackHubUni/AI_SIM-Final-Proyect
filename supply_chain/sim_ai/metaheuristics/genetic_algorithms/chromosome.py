from .gene import *


class Chromosome(ABC):
    """This is the base class for chromosomes"""

    def __init__(
        self,
        genes: list[Gene],
        maximization_problem: bool,
    ) -> None:
        self.genes: list[Gene] = genes
        """This are the genes of the chromosome"""
        self.maximization_problem: bool = maximization_problem
        """Says if this chromosome is part of a maximization problem"""

    @abstractmethod
    def mate(self, other: Self) -> Self:
        """This method mates a chromosome with another chromosome"""
        pass

    @abstractmethod
    def mutate(self) -> Self:
        """This method returns a copy of this chromosome but with mutated genes"""
        pass

    @abstractmethod
    def improve(self, n_iterations: int = 10) -> Self:
        """This method improve a chromosome"""
        pass

    def get_best(self, other: Self) -> Self:
        """This method returns the best of the 2 chromosomes"""
        my_fitness = self.get_fitness()
        other_fitness = other.get_fitness()

        def cmp(x: float, y: float):
            return x > y if self.maximization_problem else x < y

        better = self if cmp(my_fitness, other_fitness) else other
        return better

    def get_solution_values(self) -> list:
        """This method returns a list with the values of all the genes in the chromosome"""
        return [gene.value for gene in self.genes]

    @abstractmethod
    def get_fitness(self) -> float:
        """This method returns the fitness of this chromosome"""
        pass

    @abstractmethod
    def compatible(self, other: Self) -> bool:
        """This method says if the other Chromosome is compatible for mating"""
        pass

    @abstractmethod
    def random_instance(self) -> Self:
        """This method returns a random instance of the chromosome"""
        pass

    @abstractmethod
    def get_solution(self) -> Any:
        """This method construct a solution in the terms of the problem.
        If you want to use this function then you should create a chromosome that implements it
        """
        pass
