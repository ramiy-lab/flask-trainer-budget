import pytest

from domain.phase_types import PhaseSetting
from services.validators import validate_phase_setting


def test_validate_phase_setting_valid() -> None:
    phase: PhaseSetting = {
        "phase": "bulk",
        "protein_ratio": 0.3,
        "fat_ratio": 0.2,
        "carb_ratio": 0.5,
    }

    validate_phase_setting(phase)


def test_validate_phase_setting_invalid_ratio_sum() -> None:
    phase: PhaseSetting = {
        "phase": "cut",
        "protein_ratio": 0.4,
        "fat_ratio": 0.4,
        "carb_ratio": 0.4,
    }

    with pytest.raises(ValueError):
        validate_phase_setting(phase)
