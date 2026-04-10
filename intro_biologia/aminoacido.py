from .grupo_quimico import GrupoQuimico


class Aminoacido:
    def __init__(self, simbolo: str, nombre: str, grupo: GrupoQuimico, masa: float):
        self.simbolo = simbolo
        self.nombre = nombre
        self.grupo = grupo
        self.masa = masa

    # --- NO POLARES ---
    @classmethod
    def glicina(cls, m=75.07): return cls("G", "Glicina", GrupoQuimico.NO_POLAR, m)
    @classmethod
    def alanina(cls, m=89.09): return cls("A", "Alanina", GrupoQuimico.NO_POLAR, m)
    @classmethod
    def valina(cls, m=117.15): return cls("V", "Valina", GrupoQuimico.NO_POLAR, m)
    @classmethod
    def leucina(cls, m=131.17): return cls("L", "Leucina", GrupoQuimico.NO_POLAR, m)
    @classmethod
    def isoleucina(cls, m=131.17): return cls("I", "Isoleucina", GrupoQuimico.NO_POLAR, m)
    @classmethod
    def metionina(cls, m=149.21): return cls("M", "Metionina", GrupoQuimico.NO_POLAR, m)
    @classmethod
    def fenilalanina(cls, m=165.19): return cls("F", "Fenilalanina", GrupoQuimico.NO_POLAR, m)
    @classmethod
    def triptofano(cls, m=204.23): return cls("W", "Triptófano", GrupoQuimico.NO_POLAR, m)
    @classmethod
    def prolina(cls, m=115.13): return cls("P", "Prolina", GrupoQuimico.NO_POLAR, m)

    # --- POLARES NEUTROS ---
    @classmethod
    def serina(cls, m=105.09): return cls("S", "Serina", GrupoQuimico.POLAR_NEUTRO, m)
    @classmethod
    def treonina(cls, m=119.12): return cls("T", "Treonina", GrupoQuimico.POLAR_NEUTRO, m)
    @classmethod
    def cisteina(cls, m=121.16): return cls("C", "Cisteína", GrupoQuimico.POLAR_NEUTRO, m)
    @classmethod
    def tirosina(cls, m=181.19): return cls("Y", "Tirosina", GrupoQuimico.POLAR_NEUTRO, m)
    @classmethod
    def asparagina(cls, m=132.12): return cls("N", "Asparagina", GrupoQuimico.POLAR_NEUTRO, m)
    @classmethod
    def glutamina(cls, m=146.14): return cls("Q", "Glutamina", GrupoQuimico.POLAR_NEUTRO, m)

    # --- CARGADOS POSITIVOS (Básicos) ---
    @classmethod
    def lisina(cls, m=146.19): return cls("K", "Lisina", GrupoQuimico.CARGADO_POSITIVO, m)
    @classmethod
    def arginina(cls, m=174.20): return cls("R", "Arginina", GrupoQuimico.CARGADO_POSITIVO, m)
    @classmethod
    def histidina(cls, m=155.15): return cls("H", "Histidina", GrupoQuimico.CARGADO_POSITIVO, m)

    # --- CARGADOS NEGATIVOS (Ácidos) ---
    @classmethod
    def acido_aspartico(cls, m=133.10): return cls("D", "Ácido Aspártico", GrupoQuimico.CARGADO_NEGATIVO, m)
    @classmethod
    def acido_glutamico(cls, m=147.13): return cls("E", "Ácido Glutámico", GrupoQuimico.CARGADO_NEGATIVO, m)

    def __repr__(self):
        # Representación corta de 3 letras
        return self.nombre[:3].capitalize()