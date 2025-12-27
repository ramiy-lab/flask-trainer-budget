from __future__ import annotations

from typing import Final

from domain.common_alias import Gram, KCAL
from domain.phase_types import PhaseSetting
from domain.recommendation_types import (
    Macros,
    MacroStatus,
    RecommendationResult,
    Status,
)
from services.phase_service import calculate_target_macros


DEFAULT_TOLERANCE_RATIO: Final[float] = 0.10


def _judge(*, diff: Gram, target: Gram, tolerance_ratio: float) -> Status:
    """
    diff = actual - target を前提に判定する
    """
    if tolerance_ratio < 0:
        raise ValueError("tolerance_ratio must be >= 0")

    if target == 0:
        if diff == 0:
            return "ok"
        return "high" if diff > 0 else "low"

    threshold: float = float(target) * tolerance_ratio

    if diff < -threshold:
        return "low"
    if diff > threshold:
        return "high"
    return "ok"


def _to_gram(value: float) -> Gram:
    return float(value)


def _to_kcal(value: float) -> KCAL:
    return float(value)


def build_recommendation(
    *,
    actual: Macros,
    target_kcal: KCAL,
    phase_setting: PhaseSetting,
    tolerance_ratio: float = DEFAULT_TOLERANCE_RATIO,
) -> RecommendationResult:
    """
    推奨PFC (target) を算出し、実測 (actual) との差分 (diff) と判定 (status) を返す。
    meal_serviceには依存しない (actual は呼び出し側が用意する)
    将来DB導入しても、入力が "actual/target_kcal/phase_setting" のままなので壊れない
    """
    target: Macros = calculate_target_macros(target_kcal, phase_setting)

    diff: Macros = {
        "protein_g": _to_gram(actual["protein_g"] - target["protein_g"]),
        "fat_g": _to_gram(actual["fat_g"] - target["fat_g"]),
        "carb_g": _to_gram(actual["carb_g"] - target["carb_g"]),
        "kcal": _to_kcal(actual["kcal"] - target["kcal"]),
    }

    status: MacroStatus = {
        "protein_g": _judge(
            diff=diff["protein_g"],
            target=target["protein_g"],
            tolerance_ratio=tolerance_ratio,
        ),
        "fat_g": _judge(
            diff=diff["fat_g"], target=target["fat_g"], tolerance_ratio=tolerance_ratio
        ),
        "carb_g": _judge(
            diff=diff["carb_g"],
            target=target["carb_g"],
            tolerance_ratio=tolerance_ratio,
        ),
    }

    return {
        "target": target,
        "actual": actual,
        "diff": diff,
        "status": status,
    }
