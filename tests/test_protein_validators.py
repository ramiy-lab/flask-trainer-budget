import pytest

from domain.protein_types import ProteinItem
from services.validators import validate_protein_item


def test_validate_protein_item_valid() -> None:
    protein: ProteinItem = {
        "id": "whey_protein",
        "name": "ホエイプロテイン",
        "total_weight_g": 1000.0,
        "serving_size_g": 30.0,
        "price": 4000,
    }

    validate_protein_item(protein)


def test_validate_protein_item_serving_exceeds_total() -> None:
    protein: ProteinItem = {
        "id": "invalid_protein",
        "name": "invalid_protein",
        "total_weight_g": 500.0,
        "serving_size_g": 600.0,
        "price": 3000,
    }

    with pytest.raises(ValueError):
        validate_protein_item(protein)
