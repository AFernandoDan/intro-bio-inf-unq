from .aminoacido import Aminoacido


class Proteina:
    def __init__(self, nombre: str, secuencia: list[Aminoacido]):
        if not secuencia:
            raise ValueError("No se puede crear una proteína sin secuencia.")
        self.nombre = nombre
        self.secuencia = secuencia

    def mostrar_estructura_primaria(self):
        """Muestra la secuencia lineal con los extremos químicos."""
        cuerpo = "-".join([repr(aa) for aa in self.secuencia])
        return f"NH2-{cuerpo}-COOH"

    def calcular_masa_total(self):
        """Calcula la masa restando la pérdida de agua por enlace peptídico."""
        MASA_H2O = 18.01
        suma_masas = sum(aa.masa for aa in self.secuencia)
        n_enlaces = len(self.secuencia) - 1
        return suma_masas - (n_enlaces * MASA_H2O)

    def __repr__(self):
        return f"Proteina: {self.nombre} ({len(self.secuencia)} residuos)"