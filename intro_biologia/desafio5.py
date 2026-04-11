from __future__ import annotations

from dataclasses import dataclass
from statistics import fmean
from typing import Iterable, Sequence


# Tabla Chou-Fasman (propensiones por residuo, codigo de una letra).
PROPENSION_ALFA: dict[str, float] = {
    "E": 1.59,
    "A": 1.41,
    "L": 1.34,
    "M": 1.30,
    "Q": 1.27,
    "K": 1.23,
    "R": 1.21,
    "H": 1.05,
    "V": 0.90,
    "I": 1.09,
    "Y": 0.74,
    "C": 0.66,
    "W": 1.02,
    "F": 1.16,
    "T": 0.76,
    "G": 0.43,
    "N": 0.76,
    "P": 0.34,
    "S": 0.57,
    "D": 0.99,
}

PROPENSION_BETA: dict[str, float] = {
    "V": 1.87,
    "I": 1.67,
    "Y": 1.45,
    "C": 1.40,
    "W": 1.35,
    "F": 1.33,
    "T": 1.17,
    "L": 1.22,
    "M": 1.14,
    "H": 0.80,
    "R": 0.84,
    "K": 0.69,
    "Q": 0.98,
    "E": 0.52,
    "A": 0.72,
    "N": 0.48,
    "G": 0.58,
    "P": 0.31,
    "S": 0.96,
    "D": 0.39,
}


@dataclass(frozen=True)
class Region:
    start: int
    end: int

    def contains(self, index: int) -> bool:
        return self.start <= index <= self.end


@dataclass(frozen=True)
class ChouFasmanConfig:
    helix_seed_window: int = 6
    helix_min_strong: int = 4
    strand_seed_window: int = 5
    strand_min_strong: int = 3
    extension_window: int = 4
    extension_threshold: float = 1.0
    helix_label: str = "H"
    strand_label: str = "B"
    loop_label: str = "L"


@dataclass(frozen=True)
class PredictionResult:
    sequence: tuple[str, ...]
    helix_regions: tuple[Region, ...]
    strand_regions: tuple[Region, ...]
    secondary_structure: str


class ChouFasmanPredictor:
    def __init__(
        self,
        config: ChouFasmanConfig | None = None,
        propension_alfa: dict[str, float] | None = None,
        propension_beta: dict[str, float] | None = None,
    ):
        self.config = config or ChouFasmanConfig()
        self.propension_alfa = propension_alfa or PROPENSION_ALFA
        self.propension_beta = propension_beta or PROPENSION_BETA

    def predict(self, sequence_ids: Iterable[str]) -> PredictionResult:
        sequence = _normalize_sequence(sequence_ids)
        _validate_residue_symbols(sequence, self.propension_alfa)

        helix_regions = _find_and_extend_regions(
            sequence=sequence,
            propensity=self.propension_alfa,
            seed_window=self.config.helix_seed_window,
            min_strong=self.config.helix_min_strong,
            extension_window=self.config.extension_window,
            extension_threshold=self.config.extension_threshold,
        )
        strand_regions = _find_and_extend_regions(
            sequence=sequence,
            propensity=self.propension_beta,
            seed_window=self.config.strand_seed_window,
            min_strong=self.config.strand_min_strong,
            extension_window=self.config.extension_window,
            extension_threshold=self.config.extension_threshold,
        )

        secondary_structure = _resolve_labels(
            sequence=sequence,
            helix_regions=helix_regions,
            strand_regions=strand_regions,
            propension_alfa=self.propension_alfa,
            propension_beta=self.propension_beta,
            helix_label=self.config.helix_label,
            strand_label=self.config.strand_label,
            loop_label=self.config.loop_label,
        )

        return PredictionResult(
            sequence=tuple(sequence),
            helix_regions=tuple(helix_regions),
            strand_regions=tuple(strand_regions),
            secondary_structure=secondary_structure,
        )


def predict_secondary_structure(sequence_ids: Iterable[str]) -> str:
    return ChouFasmanPredictor().predict(sequence_ids).secondary_structure


def _normalize_sequence(sequence_ids: Iterable[str]) -> list[str]:
    sequence = [str(symbol).strip().upper() for symbol in sequence_ids]
    if not sequence:
        raise ValueError("La secuencia no puede estar vacia.")
    return sequence


def _validate_residue_symbols(sequence: Sequence[str], reference: dict[str, float]) -> None:
    unknown = sorted({symbol for symbol in sequence if symbol not in reference})
    if unknown:
        symbols = ", ".join(unknown)
        raise ValueError(f"Simbolos de aminoacidos no soportados: {symbols}")


def _window_average(
    sequence: Sequence[str],
    propensity: dict[str, float],
    start: int,
    size: int,
) -> float:
    values = [propensity[residue] for residue in sequence[start:start + size]]
    return fmean(values)


def _count_strong(
    sequence: Sequence[str],
    propensity: dict[str, float],
    start: int,
    size: int,
    threshold: float,
) -> int:
    return sum(
        propensity[residue] > threshold
        for residue in sequence[start:start + size]
    )


def _find_and_extend_regions(
    sequence: Sequence[str],
    propensity: dict[str, float],
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
    propensity: dict[str, float],
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
    propension_alfa: dict[str, float],
    propension_beta: dict[str, float],
    helix_label: str,
    strand_label: str,
    loop_label: str,
) -> str:
    n = len(sequence)
    labels = [loop_label] * n
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
                propension_alfa[residue]
                for residue in sequence[conflict_start:conflict_end + 1]
            )
            beta_avg = fmean(
                propension_beta[residue]
                for residue in sequence[conflict_start:conflict_end + 1]
            )
            winner = helix_label if alpha_avg >= beta_avg else strand_label
            for i in range(conflict_start, conflict_end + 1):
                labels[i] = winner
        elif in_helix:
            labels[index] = helix_label
        elif in_strand:
            labels[index] = strand_label

        index += 1

    return "".join(labels)


def _build_mask(length: int, regions: Sequence[Region]) -> list[bool]:
    mask = [False] * length
    for region in regions:
        for i in range(region.start, region.end + 1):
            mask[i] = True
    return mask
