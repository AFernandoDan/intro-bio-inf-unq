from .aminoacido import Aminoacido
from .grupo_quimico import GrupoQuimico
from .desafio2 import Proteina
from .desafio5 import ChouFasmanPredictor, ChouFasmanConfig, PredictionResult, predict_secondary_structure

__all__ = [
    "Aminoacido",
    "GrupoQuimico",
    "Proteina",
    "ChouFasmanPredictor",
    "ChouFasmanConfig",
    "PredictionResult",
    "predict_secondary_structure",
]
