import pytest

from services.phase_service import calculate_target_macros
from domain.phase_types import PhaseSetting


def test_calculate_target_macros_bulk() -> None:
    phase: PhaseSetting = {
        "phase": "bulk",
        "protein_ratio": 0.3,
        "fat_ratio": 0.2,
        "carb_ratio": 0.5,
    }

    result = calculate_target_macros(total_kcal=2000.0, phase=phase)

    assert result["protein_g"] == 150.0
    assert result["fat_g"] == pytest.approx(44.44, rel=1e-2)
    assert result["carb_g"] == 250.0


def test_calculate_target_macros_cut() -> None:
    phase: PhaseSetting = {
        "phase": "cut",
        "protein_ratio": 0.4,
        "fat_ratio": 0.3,
        "carb_ratio": 0.3,
    }

    result = calculate_target_macros(total_kcal=2000.0, phase=phase)

    assert result["protein_g"] == 200.0
    assert result["fat_g"] == pytest.approx(66.67, rel=1e-2)
    assert result["carb_g"] == 150.0
