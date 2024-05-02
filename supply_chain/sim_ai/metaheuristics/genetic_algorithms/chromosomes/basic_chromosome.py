from ..chromosome import *
import random as rnd


class BasicChromosome(Chromosome):
    """This chromosome mates with the single point strategy"""

    def __init__(
        self,
        genes: list[Gene],
        generate_solution: Callable[[list[Gene]], Any],
        fitness_function: Callable[[Any], float],
        maximization_problem: bool,
    ) -> None:
        super().__init__(genes, maximization_problem)
        self.generate_solution: Callable[[list[Gene]],] = generate_solution
        """This function represents how to convert the genes to a solution in the domain problem"""
        self.fitness_function: Callable[[list], float] = fitness_function
        """The fitness function"""
        self.fitness: float = None
        """The fitness of this chromosome"""
        self.dirty: bool = True

    def get_solution(self):
        return self.generate_solution(self.genes)

    def calculate_fitness(self) -> float:
        if self.fitness is not None and not self.dirty:
            return self.fitness
        solution = self.get_solution()
        self.fitness = self.fitness_function(solution)
        self.dirty = False
        return self.fitness

    def mate(self, other: Self) -> Self:
        if not self.equal(other):
            raise Exception("The chromosomes for mating are not compatibles")
        pivot_point = rnd.randrange(0, len(self.genes))
        clone = lambda genes: [gene.clone() for gene in genes]
        first1, last1 = (
            clone(self.genes[:pivot_point]),
            clone(self.genes[pivot_point:]),
        )
        first2, last2 = (
            clone(other.genes[:pivot_point]),
            clone(other.genes[pivot_point:]),
        )
        child1, child2 = (
            BasicChromosome(
                first1 + last2,
                self.generate_solution,
                self.fitness_function,
                self.maximization_problem,
            ),
            BasicChromosome(
                first2 + last1,
                self.generate_solution,
                self.fitness_function,
                self.maximization_problem,
            ),
        )
        cmp = lambda x, y: x > y if self.maximization_problem else x < y
        best = (
            child1
            if cmp(child1.calculate_fitness(), child2.calculate_fitness())
            else child2
        )
        return best

    def clone(self, with_mutation: bool) -> Self:
        cloned_genes = [gene.clone(with_mutation) for gene in self.genes]
        return BasicChromosome(
            cloned_genes,
            self.generate_solution,
            self.fitness_function,
            self.maximization_problem,
        )

    def mutate(self, mutation_rate: float = 0.3):
        for i in range(len(self.genes)):
            if rnd.random() < mutation_rate:
                self.genes[i].mutate()
        self.dirty = True
        self.calculate_fitness()
