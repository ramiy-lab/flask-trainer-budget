import pytest

from services.meal_service import (
    calculate_meal_pfc,
    calculate_meal_price,
)
from domain.food_types import FoodItem


def test_calculate_meal_pfc_basic() -> None:
    foods: list[FoodItem] = [
        {
            "id": "chicken",
            "name": "鶏むね肉",
            "protein_g": 23.0,
            "fat_g": 1.5,
            "carb_g": 0.0,
            "kcal": 120.0,
            "price": 150,
        },
        {
            "id": "rice",
            "name": "白米",
            "protein_g": 2.5,
            "fat_g": 0.3,
            "carb_g": 37.0,
            "kcal": 168.0,
            "price": 40,
        },
    ]

    result = calculate_meal_pfc(foods)

    assert result["protein_g"] == pytest.approx(25.5)
    assert result["fat_g"] == pytest.approx(1.8)
    assert result["carb_g"] == pytest.approx(37.0)
    assert result["kcal"] == pytest.approx(288.0)


def test_calculate_meal_price_basic() -> None:
    foods: list[FoodItem] = [
        {
            "id": "egg",
            "name": "卵",
            "protein_g": 6.0,
            "fat_g": 5.0,
            "carb_g": 0.4,
            "kcal": 76.0,
            "price": 30,
        },
        {
            "id": "egg2",
            "name": "卵",
            "protein_g": 6.0,
            "fat_g": 5.0,
            "carb_g": 0.4,
            "kcal": 76.0,
            "price": 30,
        },
    ]

    assert calculate_meal_price(foods) == 60
