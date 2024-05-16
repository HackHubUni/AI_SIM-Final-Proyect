from ..genetic_algorithm import *
import random as rnd


class TournamentGeneticAlgorithm(GeneticAlgorithm):
    def __init__(
        self,
        sample_chromosome: Chromosome,
        tournament_percentage: float,
    ) -> None:
        super().__init__(sample_chromosome)
        if not 0 < tournament_percentage <= 1:
            raise Exception(
                "The tournament percentage must be between 0 (exclusive) and 1 (inclusive)"
            )
        self.tournament_percentage = tournament_percentage
        """The percentage of the population to take as participants in a tournament"""

    def generate_population(self, population_size: int) -> list[Chromosome]:
        """This method generates a new population"""
        population = [
            self.sample_chromosome.random_instance() for _ in range(population_size)
        ]
        return population

    def get_best(
        self,
        population_sample: list[Chromosome],
    ) -> Chromosome:
        best = population_sample[0]
        for i in range(1, len(population_sample)):
            best = best.get_best(population_sample[i])
        return best

    def select_next_parent_with_tournament(
        self,
        population: list[Chromosome],
        tournament_size: int,
    ) -> Chromosome:
        """This method returns a parent by the tournament selection method"""
        if tournament_size > len(population):
            raise Exception("The tournament size is greater than the population")
        tournament_population = rnd.sample(population, tournament_size)
        best = self.get_best(tournament_population)
        return best

    def selection(
        self, population: list[Chromosome]
    ) -> list[tuple[Chromosome, Chromosome]]:
        tournament_size = max(1, int(len(population) * self.tournament_percentage))
        parents: list[tuple[Chromosome, Chromosome]] = []
        for _ in range(len(population)):
            parent1 = self.select_next_parent_with_tournament(
                population, tournament_size
            )
            parent2 = self.select_next_parent_with_tournament(
                population, tournament_size
            )
            parents.append((parent1, parent2))
        return parents

    def improve_population(self, population: list[Chromosome]) -> list[Chromosome]:
        """Improves a population"""
        improved_chromosomes: list[Chromosome] = []
        for chromosome in population:
            improved = chromosome.improve()
            improved_chromosomes.append(improved)
        return improved_chromosomes

    def solve(
        self,
        population_size: int,
        max_iterations: int,
        stop_criteria: Callable[[float], bool],
    ) -> Chromosome:
        if population_size <= 5:
            raise Exception(
                "The population size must be greater than 5 for the algorithm to work"
            )
        if max_iterations <= 5:
            raise Exception("The maximum number of iterations must be greater than 5")
        population = self.improve_population(self.generate_population(population_size))
        best = self.get_best(population)
        for i in range(max_iterations):
            if stop_criteria(best.get_fitness()):
                print(
                    f"The genetic algorithm stops in the iteration = {i} with the stop criteria"
                )
                return best
            childrens = self.mate_population(population)  # Mating
            mutated_childrens = [children.mutate() for children in childrens]
            improved_childrens = [children.improve(5) for children in mutated_childrens]
            population = improved_childrens
            best = self.get_best(population)
        print(
            f"The algorithm stops after all the {max_iterations} and could not achieve the stop criteria"
        )
        return best
