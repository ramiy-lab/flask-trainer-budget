import pytest

from services.meal_service import (
    calculate_meal_pfc,
    calculate_meal_price,
)
from domain.food_types import MealItem
from domain.common_alias import Gram, KCAL, Price


@pytest.fixture
def chicken() -> dict:
    return {
        "id": "chicken",
        "name": "鶏むね肉",
        "protein_g": 23.0,
        "fat_g": 1.5,
        "carb_g": 0.0,
        "kcal": 120.0,
        "price": 150,
    }


@pytest.fixture
def egg() -> dict:
    return {
        "id": "egg",
        "name": "全卵",
        "protein_g": 6.0,
        "fat_g": 5.0,
        "carb_g": 0.4,
        "kcal": 76.0,
        "price": 30,
    }


def test_calculate_meal_pfc_single_food_100g(chicken: dict) -> None:
    items: list[MealItem] = [
        {
            "food": chicken,
            "grams": 100,
        }
    ]

    result = calculate_meal_pfc(items)

    assert result == {
        "protein_g": 23.0,
        "fat_g": 1.5,
        "carb_g": 0.0,
        "kcal": 120.0,
    }


@pytest.mark.parametrize(
    "grams, expected_ratio",
    [
        (50, 0.5),
        (150, 1.5),
        (200, 2.0),
    ],
)
def test_calculate_meal_pfc_ratio(
    chicken: dict,
    grams: int,
    expected_ratio: float,
) -> None:
    items: list[MealItem] = [
        {
            "food": chicken,
            "grams": grams,
        }
    ]

    result = calculate_meal_pfc(items)

    assert result["protein_g"] == pytest.approx(23.0 * expected_ratio)
    assert result["fat_g"] == pytest.approx(1.5 * expected_ratio)
    assert result["carb_g"] == 0.0
    assert result["kcal"] == pytest.approx(120.0 * expected_ratio)


def test_calculate_meal_pfc_multiple_foods(
    chicken: dict,
    egg: dict,
) -> None:
    items: list[MealItem] = [
        {"food": chicken, "grams": 100},
        {"food": egg, "grams": 50},
    ]

    result = calculate_meal_pfc(items)

    assert result["protein_g"] == pytest.approx(23.0 + 3.0)
    assert result["fat_g"] == pytest.approx(1.5 + 2.5)
    assert result["carb_g"] == pytest.approx(0.0 + 0.2)
    assert result["kcal"] == pytest.approx(120.0 + 38.0)


@pytest.mark.parametrize("grams", [0, -50])
def test_calculate_meal_pfc_ignore_non_positive_grams(
    chicken: dict,
    grams: int,
) -> None:
    items: list[MealItem] = [
        {"food": chicken, "grams": grams},
    ]

    result = calculate_meal_pfc(items)

    assert result == {
        "protein_g": 0.0,
        "fat_g": 0.0,
        "carb_g": 0.0,
        "kcal": 0.0,
    }


def test_calculate_meal_price_single_food(chicken: dict) -> None:
    items: list[MealItem] = [
        {"food": chicken, "grams": 100},
    ]

    price: Price = calculate_meal_price(items)

    assert price == 150


def test_calculate_meal_price_ratio_and_truncation(chicken: dict) -> None:
    items: list[MealItem] = [
        {"food": chicken, "grams": 150},  # 150 * 1.5 = 225
    ]

    price: Price = calculate_meal_price(items)

    assert price == 225


def test_calculate_meal_price_multiple_foods(
    chicken: dict,
    egg: dict,
) -> None:
    items: list[MealItem] = [
        {"food": chicken, "grams": 100},  # 150
        {"food": egg, "grams": 50},       # 15
    ]

    price: Price = calculate_meal_price(items)

    assert price == 165


@pytest.mark.parametrize("grams", [0, -100])
def test_calculate_meal_price_ignore_non_positive_grams(
    chicken: dict,
    grams: int,
) -> None:
    items: list[MealItem] = [
        {"food": chicken, "grams": grams},
    ]

    price: Price = calculate_meal_price(items)

    assert price == 0
