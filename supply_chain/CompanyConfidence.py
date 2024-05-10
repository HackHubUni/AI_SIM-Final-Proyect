from enum import Enum


class CompanyConfidence(Enum):
    """The confidence level of a company"""

    Fatal = "Fatal"
    Mal = "Mal"
    Regular = "Regular"
    Bien = "Bien"
    MuyBien = "Muy_bien"
    Excelente = "Excelente"