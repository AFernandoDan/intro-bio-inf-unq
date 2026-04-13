from dataclasses import dataclass
import math
from .aminoacido import Aminoacido

@dataclass
class Residuo3D:
    """
    Actúa como un 'nodo' que une la semántica química con la geometría.
    En biología estructural a un aminoácido en una cadena se le llama 'Residuo'.
    """
    aminoacido: Aminoacido
    x: float
    y: float
    z: float

    def coordenadas(self) -> tuple[float, float, float]:
        return (self.x, self.y, self.z)


class EstructuraTerciaria:
    def __init__(self, residuos: list[Residuo3D]):
        self.residuos = residuos
        self._validar_continuidad()

    def _validar_continuidad(self):
        """Valida que la distancia entre residuos consecutivos sea ~3.8 Å."""
        for i in range(len(self.residuos) - 1):
            r1, r2 = self.residuos[i], self.residuos[i + 1]
            dist = math.dist(r1.coordenadas(), r2.coordenadas())
            if not (3.7 <= dist <= 3.9):
                raise ValueError(
                    f"Física rota entre {r1.aminoacido.nombre} y {r2.aminoacido.nombre}. "
                    f"Distancia: {dist:.2f} Å"
                )

    def obtener_secuencia_primaria(self) -> list[Aminoacido]:
        """Para el biólogo: devuelve solo qué aminoácidos son."""
        return [r.aminoacido for r in self.residuos]

    def obtener_matriz_coordenadas(self) -> list[list[float]]:
        """
        Para el algoritmo matemático: devuelve una matriz pura N x 3.
        Aquí es donde alimentas a NumPy o librerías de machine learning.
        """
        return [[r.x, r.y, r.z] for r in self.residuos]

    def buscar_por_posicion(self, indice: int) -> Residuo3D:
        """Permite a los humanos consultar el espacio tridimensional semánticamente."""
        return self.residuos[indice]