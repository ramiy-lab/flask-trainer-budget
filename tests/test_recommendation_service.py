from __future__ import annotations

import pytest

from services.recommendation_service import build_recommendation
from domain.phase_types import PhaseSetting
from domain.recommendation_types import Macros


def _phase_bulk() -> PhaseSetting:
    return {
        "phase": "bulk",
        "protein_ratio": 0.30,
        "fat_ratio": 0.20,
        "carb_ratio": 0.50,
    }


def _actual(*, protein: float, fat: float, carb: float, kcal: float) -> Macros:
    return {
        "protein_g": protein,
        "fat_g": fat,
        "carb_g": carb,
        "kcal": kcal,
    }


def test_build_recommendation_ok_when_within_tolerance() -> None:
    """
    actual が target ± tolerance 内 → すべて ok
    """
    actual = _actual(
        protein=75.0,
        fat=22.0,
        carb=125.0,
        kcal=1000.0,
    )

    result = build_recommendation(
        actual=actual,
        target_kcal=1000.0,
        phase_setting=_phase_bulk(),
        tolerance_ratio=0.10,
    )

    assert result["status"]["protein_g"] == "ok"
    assert result["status"]["fat_g"] == "ok"
    assert result["status"]["carb_g"] == "ok"


def test_build_recommendation_low_when_below_threshold() -> None:
    """
    actual < target - threshold → low
    """
    actual = _actual(
        protein=50.0,  # 明確に不足
        fat=20.0,
        carb=125.0,
        kcal=1000.0,
    )

    result = build_recommendation(
        actual=actual,
        target_kcal=1000.0,
        phase_setting=_phase_bulk(),
        tolerance_ratio=0.10,
    )

    assert result["status"]["protein_g"] == "low"


def test_build_recommendation_high_when_above_threshold() -> None:
    """
    actual > target + threshold → high
    """
    actual = _actual(
        protein=120.0,  # 明確に過剰
        fat=20.0,
        carb=125.0,
        kcal=1000.0,
    )

    result = build_recommendation(
        actual=actual,
        target_kcal=1000.0,
        phase_setting=_phase_bulk(),
        tolerance_ratio=0.10,
    )

    assert result["status"]["protein_g"] == "high"


def test_target_zero_special_case() -> None:
    """
    target == 0 の特例判定
    """
    actual = _actual(
        protein=0.0,
        fat=0.0,
        carb=0.0,
        kcal=0.0,
    )

    result = build_recommendation(
        actual=actual,
        target_kcal=0.0,
        phase_setting={
            "phase": "bulk",
            "protein_ratio": 0.0,
            "fat_ratio": 0.0,
            "carb_ratio": 0.0,
        },
    )

    assert result["status"]["protein_g"] == "ok"


def test_negative_tolerance_ratio_raises_error() -> None:
    """
    tolerance_ratio < 0 は設計上エラー
    """
    actual = _actual(
        protein=70.0,
        fat=20.0,
        carb=120.0,
        kcal=1000.0,
    )

    with pytest.raises(ValueError):
        build_recommendation(
            actual=actual,
            target_kcal=1000.0,
            phase_setting=_phase_bulk(),
            tolerance_ratio=-0.1,
        )
