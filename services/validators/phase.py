from typing import Iterable

from domain.phase_types import PhaseSetting
from domain.phase_enum import PhaseEnum
from domain.common_alias import Ratio
from ._common import _ensure_positive_float


def validate_phase_setting(phase: PhaseSetting) -> None:
    phase_name = phase["phase"]

    if phase_name not in (PhaseEnum.BULK.value, PhaseEnum.CUT.value):
        raise ValueError(f"invalid phase value: {phase_name}")

    protein_ratio: Ratio = phase["protein_ratio"]
    fat_ratio: Ratio = phase["fat_ratio"]
    carb_ratio: Ratio = phase["carb_ratio"]

    _ensure_positive_float(protein_ratio, "protein_ratio")
    _ensure_positive_float(fat_ratio, "fat_ratio")
    _ensure_positive_float(carb_ratio, "carb_ratio")

    total_ratio: Ratio = protein_ratio + fat_ratio + carb_ratio

    if abs(total_ratio - 1.0) > 0.001:
        raise ValueError(f"macros ratio must sum to 1.0, got {total_ratio}")


def validate_phase_settings(phases: Iterable[PhaseSetting]) -> None:
    for phase in phases:
        validate_phase_setting(phase)
