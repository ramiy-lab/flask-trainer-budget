from __future__ import annotations

from typing import Literal, TypedDict

from domain.common_alias import Gram, KCAL


class Macros(TypedDict):
    protein_g: Gram
    fat_g: Gram
    carb_g: Gram
    kcal: KCAL


Status = Literal["low", "ok", "high"]


class MacroStatus(TypedDict):
    protein_g: Status
    fat_g: Status
    carb_g: Status


class RecommendationResult(TypedDict):
    target: Macros
    actual: Macros
    diff: Macros
    status: MacroStatus
