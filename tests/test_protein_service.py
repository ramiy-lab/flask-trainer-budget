import pytest

from services.protein_service import calculate_remaining_weight
from domain.protein_types import ProteinItem


@pytest.mark.parametrize(
    "protein, used_servings, expected",
    [
        (
            {
                "id": "whey",
                "name": "ホエイ",
                "total_weight_g": 1000.0,
                "serving_size_g": 25.0,
                "price": 4000,
            },
            10,
            750.0,
        ),
        (
            {
                "id": "whey",
                "name": "ホエイ",
                "total_weight_g": 500.0,
                "serving_size_g": 50.0,
                "price": 3000,
            },
            20,
            0.0,
        ),
    ],
)
def test_calculate_remaining_weight(
    protein: ProteinItem,
    used_servings: int,
    expected: float,
) -> None:
    assert calculate_remaining_weight(protein, used_servings) == expected
