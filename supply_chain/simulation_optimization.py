from uuid import uuid4

from . import CompanyConfidence
from .sim_ai.metaheuristics.genetic_algorithms.genetic_implementations.basic_genetic_alg import *
from .sim_ai.metaheuristics.genetic_algorithms.genes.choice_gene import *
from .sim_ai.metaheuristics.genetic_algorithms.chromosomes.basic_chromosome import *
from enum import Enum
from .company import TypeCompany


#class CompanyConfidence(Enum):
#    """The confidence level of a company"""
#
#    Fatal = "Fatal"
#    Mal = "Mal"
#    Regular = "Regular"
#    Bien = "Bien"
#    MuyBien = "Muy_bien"
#    Excelente = "Excelente"


class OptimizerParameter:
    def __init__(
        self,
        company_name: str,
        company_type: TypeCompany,
        confidence: CompanyConfidence,
    ) -> None:
        self.company_name: str = company_name
        """The name of the company"""
        self.company_type: TypeCompany = company_type
        """The type of the company"""
        self.confidence: CompanyConfidence = confidence
        """The confidence of this company"""


class OptimizerParameterGene(Gene):
    def __init__(
        self,
        value: OptimizerParameter,
    ) -> None:
        super().__init__(value, "Optimizer gene")

    def mutate(self) -> Self:
        actual_confidence = self.value.confidence
        available_options = [
            CompanyConfidence.Fatal,
            CompanyConfidence.Mal,
            CompanyConfidence.Regular,
            CompanyConfidence.Bien,
            CompanyConfidence.MuyBien,
            CompanyConfidence.Excelente,
        ]
        v1, v2 = rnd.sample(available_options, 2)
        new_confidence = v1 if actual_confidence == v2 else v2
        new_parameter = OptimizerParameter(
            self.value.company_name,
            self.value.company_type,
            new_confidence,
        )
        return OptimizerParameterGene(new_parameter)

    def clone(self) -> Self:
        parameter: OptimizerParameter = self.value
        cloned_parameter = OptimizerParameter(
            parameter.company_name, parameter.company_type, parameter.confidence
        )
        return cloned_parameter

    def __str__(self) -> str:
        parameter: OptimizerParameter = self.value
        return f"The company '{parameter.company_name}' of type '{parameter.company_type}', has confidence of {parameter.confidence}"


def build_optimizer_chromosome(
    optimizer_parameter_list: list[OptimizerParameter],
    fitness: Callable[[list[OptimizerParameter]], float],
    maximization_problem: bool,
) -> SimpleChromosome:
    """This function creates the chromosome used for optimize the supply chain"""

    genes = [
        OptimizerParameterGene(optimizer_parameter)
        for optimizer_parameter in optimizer_parameter_list
    ]
    for gene in genes:
        print(gene)
    return SimpleChromosome(genes, fitness, maximization_problem)


def supply_optimizer(
    optimizer_parameter_list: list[OptimizerParameter],
    fitness: Callable[[list[OptimizerParameter]], float],
    maximization_problem: bool,
    stop_criteria: Callable[[float], bool],
    population_size: int = 50,
    max_iterations: int = 20,
) -> list[OptimizerParameter]:
    """This is the function to call to optimize the supply chain"""
    sample_chromosome = build_optimizer_chromosome(
        optimizer_parameter_list, fitness, maximization_problem
    )
    genetic_algorithm = TournamentGeneticAlgorithm(sample_chromosome, 0.3)
    best_chromosome = genetic_algorithm.solve(
        population_size, max_iterations, stop_criteria
    )
    return best_chromosome.get_solution_values()
