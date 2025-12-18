import pytest

from domain.protein_types import ProteinItem
from services.protein_service import (
    calculate_remaining_weight,
    calculate_total_servings,
)


@pytest.fixture
def whey() -> ProteinItem:
    return {
        "id": "whey",
        "name": "ホエイ",
        "total_weight_g": 1000.0,
        "serving_size_g": 25.0,
        "price": 4000,
    }


def test_calculate_remaining_weight(whey: ProteinItem) -> None:
    assert calculate_remaining_weight(whey, used_servings=10) == 750.0


def test_calculate_total_servings(whey: ProteinItem) -> None:
    assert calculate_total_servings(whey) == 40
