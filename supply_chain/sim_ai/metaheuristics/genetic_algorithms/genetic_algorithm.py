from chromosome import *


class GeneticAlgorithm:
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

    def best_chromosome(
        self,
        chromosome1: Chromosome,
        chromosome2: Chromosome,
    ) -> Chromosome:
        """Returns the best chromosome"""
        cmp = lambda x, y: x > y if self.maximization_problem else x < y
        if cmp(chromosome1.calculate_fitness(), chromosome2.calculate_fitness()):
            return chromosome1
        return chromosome2

    def get_best_solution(self, population: list[Chromosome]) -> Chromosome:
        """Returns the best chromosome in a population"""
        if population is None or len(population) == 0:
            raise Exception(f"The population passed is None or Empty")
        best = population[0]
        # cmp = lambda x, y: x > y if self.maximization_problem else x < y
        # TODO: Make the comparison more effective by storing the fitness once and not calculating it every time
        for i in range(1, len(population)):
            actual = population[i]
            best = self.best_chromosome(actual, best)
        return best

    def mate_population(self, population: list[Chromosome]) -> list[Chromosome]:
        """This method generate a new population of individuals from a population.
        This method calls internally the selection and the cross_over method"""
        new_population: list[Chromosome] = []
        parents: list[tuple[Chromosome, Chromosome]] = self.selection(population)
        for parent1, parent2 in parents:
            child: Chromosome = parent1.mate(parent2)
            new_population.append(child)
        return new_population

    def solve(
        self,
        population_size: int,
        max_iterations: int,
        stop_criteria: Callable[
            [float], bool
        ],  # Stop criteria takes as parameter the fitness
        mutation_rate: float = 0.3,
    ) -> Chromosome:
        """This returns the population whose fitness was the best"""
        population: list[Chromosome] = [
            self.sample_chromosome.clone(True) for _ in range(population_size)
        ]
        best_solution = self.sample_chromosome.clone(True)
        for _ in range(max_iterations):
            for individual in population:
                individual.calculate_fitness()
            # Updating the best solution so far
            best_solution = self.best_chromosome(
                best_solution, self.get_best_solution(population)
            )
            # Generate new population
            new_population = self.mate_population(population)
            # Apply mutation
            for offspring in new_population:
                offspring.mutate(mutation_rate)
            # Check for stopping criteria
            if stop_criteria(best_solution.calculate_fitness()):
                return best_solution
        return best_solution
