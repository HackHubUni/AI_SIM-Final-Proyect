from ..chromosome import *
import random as rnd


class SimpleChromosome(Chromosome):
    """This chromosome performs random single point crossover and random simple mutation"""

    def __init__(
        self,
        genes: list[Gene],
        fitness_function: Callable[[list], float],
        maximization_problem: bool,
    ) -> None:
        super().__init__(genes, maximization_problem)
        self.fitness_function: Callable[[list], float] = fitness_function
        """The function used to calculate the fitness of a chromosome"""
        self.fitness_value: float = None
        """The fitness of this chromosome"""

    def random_instance(self) -> Self:
        new_genes = [gene.mutate() for gene in self.genes]
        return SimpleChromosome(
            new_genes, self.fitness_function, self.maximization_problem
        )

    def compatible(self, other: Self) -> bool:
        return len(self.genes) == len(other.genes) and all(
            type(gene1) == type(gene2) and gene1 == gene2
            for gene1, gene2 in zip(self.genes, other.genes)
        )

    def get_fitness(self) -> float:
        if self.fitness_value is not None:
            return self.fitness_value
        solution_values = self.get_solution_values()
        self.fitness_value = self.fitness_function(solution_values)
        return self.fitness_value

    def improve(self, n_iterations: int = 10) -> Self:
        best_chromosome = self
        for _ in range(n_iterations):
            new_chromosome = self.mutate()
            best_chromosome = best_chromosome.get_best(new_chromosome)
        return best_chromosome

    def mutate(self) -> Self:
        index = rnd.randrange(0, len(self.genes))
        old_gene = self.genes[index]
        mutated = old_gene.mutate()
        cloned_genes = [gene.clone() for gene in self.genes]
        cloned_genes[index] = mutated
        return SimpleChromosome(
            cloned_genes, self.fitness_function, self.maximization_problem
        )

    def get_solution(self) -> Any:
        return self.get_solution_values()

    def cloned_genes(self) -> list[Gene]:
        """This method returns a copy of all the genes of this chromosome"""
        return [gene.clone() for gene in self.genes]

    def mate(self, other: Self) -> Self:
        if not self.compatible(other):
            raise Exception(
                "The chromosomes are not compatible. Check the length of it's genes and the type of each one"
            )
        pivot_point = rnd.randrange(0, len(self.genes))
        my_genes, other_genes = (self.cloned_genes(), other.cloned_genes())
        first1, last1 = (my_genes[:pivot_point], my_genes[pivot_point:])
        first2, last2 = (other_genes[:pivot_point], other_genes[pivot_point:])
        child1 = SimpleChromosome(
            first1 + last2, self.fitness_function, self.maximization_problem
        )
        child2 = SimpleChromosome(
            first2 + last1, self.fitness_function, self.maximization_problem
        )
        return child1.get_best(child2)
