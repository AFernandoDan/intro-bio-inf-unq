from __future__ import annotations

import sys
from dataclasses import dataclass
from enum import Enum
from statistics import fmean
from typing import Iterable, Sequence

from .aminoacido import Aminoacido
from .desafio2 import Proteina


class TipoEstructuraSecundaria(Enum):
    HELICE = "H"
    LAMINA = "B"
    BUCLE = "L"


@dataclass(frozen=True)
class PropensionesResiduo:
    aminoacido: Aminoacido
    alfa: float
    beta: float

    def __repr__(self) -> str:
        return (
            f"PropensionesResiduo({self.aminoacido.simbolo}: "
            f"alfa={self.alfa:.2f}, beta={self.beta:.2f})"
        )


class TablaPropensiones:
    def __init__(self, entradas: Iterable[PropensionesResiduo]):
        self._por_simbolo: dict[str, PropensionesResiduo] = {
            entrada.aminoacido.simbolo: entrada
            for entrada in entradas
        }

    def contiene(self, simbolo: str) -> bool:
        return simbolo in self._por_simbolo

    def alfa(self, simbolo: str) -> float:
        return self._por_simbolo[simbolo].alfa

    def beta(self, simbolo: str) -> float:
        return self._por_simbolo[simbolo].beta

    def aminoacido(self, simbolo: str) -> Aminoacido:
        return self._por_simbolo[simbolo].aminoacido

    @property
    def simbolos(self) -> set[str]:
        return set(self._por_simbolo)

    def __repr__(self) -> str:
        return f"TablaPropensiones({len(self._por_simbolo)} residuos)"

    @classmethod
    def chou_fasman_estandar(cls) -> "TablaPropensiones":
        return cls(
            [
                PropensionesResiduo(Aminoacido.acido_glutamico(), alfa=1.59, beta=0.52),
                PropensionesResiduo(Aminoacido.alanina(), alfa=1.41, beta=0.72),
                PropensionesResiduo(Aminoacido.leucina(), alfa=1.34, beta=1.22),
                PropensionesResiduo(Aminoacido.metionina(), alfa=1.30, beta=1.14),
                PropensionesResiduo(Aminoacido.glutamina(), alfa=1.27, beta=0.98),
                PropensionesResiduo(Aminoacido.lisina(), alfa=1.23, beta=0.69),
                PropensionesResiduo(Aminoacido.arginina(), alfa=1.21, beta=0.84),
                PropensionesResiduo(Aminoacido.histidina(), alfa=1.05, beta=0.80),
                PropensionesResiduo(Aminoacido.valina(), alfa=0.90, beta=1.87),
                PropensionesResiduo(Aminoacido.isoleucina(), alfa=1.09, beta=1.67),
                PropensionesResiduo(Aminoacido.tirosina(), alfa=0.74, beta=1.45),
                PropensionesResiduo(Aminoacido.cisteina(), alfa=0.66, beta=1.40),
                PropensionesResiduo(Aminoacido.triptofano(), alfa=1.02, beta=1.35),
                PropensionesResiduo(Aminoacido.fenilalanina(), alfa=1.16, beta=1.33),
                PropensionesResiduo(Aminoacido.treonina(), alfa=0.76, beta=1.17),
                PropensionesResiduo(Aminoacido.glicina(), alfa=0.43, beta=0.58),
                PropensionesResiduo(Aminoacido.asparagina(), alfa=0.76, beta=0.48),
                PropensionesResiduo(Aminoacido.prolina(), alfa=0.34, beta=0.31),
                PropensionesResiduo(Aminoacido.serina(), alfa=0.57, beta=0.96),
                PropensionesResiduo(Aminoacido.acido_aspartico(), alfa=0.99, beta=0.39),
            ]
        )


@dataclass(frozen=True)
class Region:
    start: int
    end: int

    def contiene(self, indice: int) -> bool:
        return self.start <= indice <= self.end

    def __repr__(self) -> str:
        return f"Region({self.start}-{self.end})"


@dataclass(frozen=True)
class ChouFasmanConfig:
    helix_seed_window: int = 6
    helix_min_strong: int = 4
    strand_seed_window: int = 5
    strand_min_strong: int = 3
    extension_window: int = 4
    extension_threshold: float = 1.0


@dataclass(frozen=True)
class SegmentoEstructural:
    region: Region
    tipo: TipoEstructuraSecundaria

    def __repr__(self) -> str:
        return f"SegmentoEstructural(tipo={self.tipo.name}, region={self.region})"


@dataclass(frozen=True)
class PrediccionEstructuraSecundaria:
    sequence: tuple[Aminoacido, ...]
    helix_regions: tuple[Region, ...]
    strand_regions: tuple[Region, ...]
    secondary_structure: tuple[TipoEstructuraSecundaria, ...]

    @property
    def secondary_structure_string(self) -> str:
        return "".join(tipo.value for tipo in self.secondary_structure)

    @property
    def secuencia(self) -> tuple[Aminoacido, ...]:
        return self.sequence

    @property
    def regiones_helice(self) -> tuple[Region, ...]:
        return self.helix_regions

    @property
    def regiones_lamina(self) -> tuple[Region, ...]:
        return self.strand_regions

    @property
    def estructura_secundaria(self) -> tuple[TipoEstructuraSecundaria, ...]:
        return self.secondary_structure

    @property
    def estructura_secundaria_string(self) -> str:
        return self.secondary_structure_string

    def segmentos(self) -> tuple[SegmentoEstructural, ...]:
        return tuple(
            SegmentoEstructural(region=region, tipo=TipoEstructuraSecundaria.HELICE)
            for region in self.helix_regions
        ) + tuple(
            SegmentoEstructural(region=region, tipo=TipoEstructuraSecundaria.LAMINA)
            for region in self.strand_regions
        )

    def __repr__(self) -> str:
        simbolos = "".join(aa.simbolo for aa in self.sequence)
        return (
            f"PrediccionEstructuraSecundaria(len={len(self.sequence)}, "
            f"secuencia='{simbolos}', estructura='{self.secondary_structure_string}')"
        )

class ChouFasmanPredictor:
    def __init__(
        self,
        config: ChouFasmanConfig | None = None,
        tabla_propensiones: TablaPropensiones | None = None,
    ):
        self.config = config or ChouFasmanConfig()
        self.tabla_propensiones = tabla_propensiones or TablaPropensiones.chou_fasman_estandar()

    def predecir(
        self,
        entrada: Proteina | Iterable[Aminoacido] | Iterable[str],
    ) -> PrediccionEstructuraSecundaria:
        sequence = _normalize_sequence(entrada, self.tabla_propensiones)
        simbolos = [aminoacido.simbolo for aminoacido in sequence]

        helix_regions = _find_and_extend_regions(
            sequence=simbolos,
            propensity=lambda simbolo: self.tabla_propensiones.alfa(simbolo),
            seed_window=self.config.helix_seed_window,
            min_strong=self.config.helix_min_strong,
            extension_window=self.config.extension_window,
            extension_threshold=self.config.extension_threshold,
        )
        strand_regions = _find_and_extend_regions(
            sequence=simbolos,
            propensity=lambda simbolo: self.tabla_propensiones.beta(simbolo),
            seed_window=self.config.strand_seed_window,
            min_strong=self.config.strand_min_strong,
            extension_window=self.config.extension_window,
            extension_threshold=self.config.extension_threshold,
        )

        secondary_structure = _resolve_labels(
            sequence=simbolos,
            helix_regions=helix_regions,
            strand_regions=strand_regions,
            propension_alfa=lambda simbolo: self.tabla_propensiones.alfa(simbolo),
            propension_beta=lambda simbolo: self.tabla_propensiones.beta(simbolo),
        )

        return PrediccionEstructuraSecundaria(
            sequence=tuple(sequence),
            helix_regions=tuple(helix_regions),
            strand_regions=tuple(strand_regions),
            secondary_structure=secondary_structure,
        )

    def predecir_estructura_secundaria(
        self,
        entrada: Proteina | Iterable[Aminoacido] | Iterable[str],
    ) -> PrediccionEstructuraSecundaria:
        return self.predecir(entrada)

    def predecir_estructura_secundaria_de_proteina(
        self,
        proteina: Proteina,
    ) -> PrediccionEstructuraSecundaria:
        return self.predecir(proteina)

def predecir_estructura_secundaria(entrada: Proteina | Iterable[Aminoacido] | Iterable[str]) -> str:
    return ChouFasmanPredictor().predecir(entrada).secondary_structure_string


def parsear_secuencia_texto(texto: str, tabla: TablaPropensiones | None = None) -> list[Aminoacido]:
    tabla_propensiones = tabla or TablaPropensiones.chou_fasman_estandar()
    simbolos = _extraer_simbolos_secuencia(texto)
    return _normalize_sequence(simbolos, tabla_propensiones)


def parsear_secuencia_desde_stdin(tabla: TablaPropensiones | None = None) -> list[Aminoacido]:
    return parsear_secuencia_texto(sys.stdin.read(), tabla)


def parse_proteina_desde_texto(
    nombre: str,
    texto: str,
    tabla: TablaPropensiones | None = None,
) -> Proteina:
    return Proteina(nombre=nombre, secuencia=parsear_secuencia_texto(texto, tabla))


def _normalize_sequence(
    entrada: Proteina | Iterable[Aminoacido] | Iterable[str],
    tabla: TablaPropensiones,
) -> list[Aminoacido]:
    if isinstance(entrada, Proteina):
        sequence = list(entrada.secuencia)
    else:
        sequence = []
        for residuo in entrada:
            if isinstance(residuo, Aminoacido):
                sequence.append(residuo)
                continue
            simbolo = str(residuo).strip().upper()
            if not tabla.contiene(simbolo):
                raise ValueError(f"Simbolos de aminoacidos no soportados: {simbolo}")
            sequence.append(tabla.aminoacido(simbolo))

    if not sequence:
        raise ValueError("La secuencia no puede estar vacia.")

    _validate_residue_symbols(sequence, tabla)
    return sequence


def _extraer_simbolos_secuencia(texto: str) -> list[str]:
    sequence_text = "".join(
        line.strip()
        for line in texto.splitlines()
        if line.strip() and not line.startswith(">")
    )
    return [symbol.upper() for symbol in sequence_text]


def _validate_residue_symbols(sequence: Sequence[Aminoacido], tabla: TablaPropensiones) -> None:
    unknown = sorted({aminoacido.simbolo for aminoacido in sequence if not tabla.contiene(aminoacido.simbolo)})
    if unknown:
        symbols = ", ".join(unknown)
        raise ValueError(f"Simbolos de aminoacidos no soportados: {symbols}")


def _window_average(
    sequence: Sequence[str],
    propensity,
    start: int,
    size: int,
) -> float:
    values = [propensity(residue) for residue in sequence[start:start + size]]
    return fmean(values)


def _count_strong(
    sequence: Sequence[str],
    propensity,
    start: int,
    size: int,
    threshold: float,
) -> int:
    return sum(
        propensity(residue) > threshold
        for residue in sequence[start:start + size]
    )


def _find_and_extend_regions(
    sequence: Sequence[str],
    propensity,
    seed_window: int,
    min_strong: int,
    extension_window: int,
    extension_threshold: float,
) -> list[Region]:
    regions: list[Region] = []
    n = len(sequence)
    i = 0

    while i <= n - seed_window:
        strong_count = _count_strong(
            sequence,
            propensity,
            start=i,
            size=seed_window,
            threshold=extension_threshold,
        )
        if strong_count >= min_strong:
            region = _extend_region(
                sequence=sequence,
                propensity=propensity,
                start=i,
                end=i + seed_window - 1,
                extension_window=extension_window,
                extension_threshold=extension_threshold,
            )
            regions.append(region)
            i = region.end + 1
            continue

        i += 1

    return _merge_regions(regions)


def _extend_region(
    sequence: Sequence[str],
    propensity,
    start: int,
    end: int,
    extension_window: int,
    extension_threshold: float,
) -> Region:
    n = len(sequence)

    while start - extension_window >= 0:
        avg_left = _window_average(
            sequence,
            propensity,
            start=start - extension_window,
            size=extension_window,
        )
        if avg_left < extension_threshold:
            break
        start -= 1

    while end + extension_window < n:
        avg_right = _window_average(
            sequence,
            propensity,
            start=end + 1,
            size=extension_window,
        )
        if avg_right < extension_threshold:
            break
        end += 1

    return Region(start=start, end=end)


def _merge_regions(regions: Sequence[Region]) -> list[Region]:
    if not regions:
        return []

    ordered = sorted(regions, key=lambda region: region.start)
    merged = [ordered[0]]

    for region in ordered[1:]:
        current = merged[-1]
        if region.start <= current.end + 1:
            merged[-1] = Region(start=current.start, end=max(current.end, region.end))
            continue
        merged.append(region)

    return merged


def _resolve_labels(
    sequence: Sequence[str],
    helix_regions: Sequence[Region],
    strand_regions: Sequence[Region],
    propension_alfa,
    propension_beta,
) -> tuple[TipoEstructuraSecundaria, ...]:
    n = len(sequence)
    labels = [TipoEstructuraSecundaria.BUCLE] * n
    helix_mask = _build_mask(n, helix_regions)
    strand_mask = _build_mask(n, strand_regions)

    index = 0
    while index < n:
        in_helix = helix_mask[index]
        in_strand = strand_mask[index]

        if in_helix and in_strand:
            conflict_start = index
            while index + 1 < n and helix_mask[index + 1] and strand_mask[index + 1]:
                index += 1
            conflict_end = index

            alpha_avg = fmean(
                propension_alfa(residue)
                for residue in sequence[conflict_start:conflict_end + 1]
            )
            beta_avg = fmean(
                propension_beta(residue)
                for residue in sequence[conflict_start:conflict_end + 1]
            )
            winner = TipoEstructuraSecundaria.HELICE if alpha_avg >= beta_avg else TipoEstructuraSecundaria.LAMINA
            for i in range(conflict_start, conflict_end + 1):
                labels[i] = winner
        elif in_helix:
            labels[index] = TipoEstructuraSecundaria.HELICE
        elif in_strand:
            labels[index] = TipoEstructuraSecundaria.LAMINA

        index += 1

    return tuple(labels)


def _build_mask(length: int, regions: Sequence[Region]) -> list[bool]:
    mask = [False] * length
    for region in regions:
        for i in range(region.start, region.end + 1):
            mask[i] = True
    return mask
