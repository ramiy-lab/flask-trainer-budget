from typing import Iterable

from domain.food_types import FoodItem
from ._common import _ensure_positive_float, _ensure_positive_int


def validate_food_item(food: FoodItem) -> None:
    _ensure_positive_float(food["protein_g"], "protein_g")
    _ensure_positive_float(food["fat_g"], "fat_g")
    _ensure_positive_float(food["carb_g"], "carb_g")
    _ensure_positive_float(food["kcal"], "kcal")
    _ensure_positive_int(food["price"], "price")


def validate_food_items(foods: Iterable[FoodItem]) -> None:
    for food in foods:
        validate_food_item(food)
