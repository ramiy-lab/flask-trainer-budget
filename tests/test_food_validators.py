import pytest

from domain.food_types import FoodItem
from services.validators import validate_food_item


def test_validate_food_item_valid() -> None:
    food: FoodItem = {
        "id": "chicken_breast",
        "name": "鶏むね肉",
        "protein_g": 23.0,
        "fat_g": 1.5,
        "carb_g": 0.0,
        "kcal": 120.0,
        "price": 300,
    }

    validate_food_item(food)


def test_validate_food_item_negative_value() -> None:
    food: FoodItem = {
        "id": "invalid_food",
        "name": "invalid_food",
        "protein_g": -10.0,
        "fat_g": 1.0,
        "carb_g": 0.0,
        "kcal": 100.0,
        "price": 200,
    }

    with pytest.raises(ValueError):
        validate_food_item(food)
