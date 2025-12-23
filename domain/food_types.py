from typing import TypedDict

from domain.food_category_types import FoodCategory
from domain.common_alias import Gram, KCAL, Price, FoodID


class FoodItem(TypedDict):
    id: FoodID
    name: str
    category: FoodCategory

    protein_g: Gram
    fat_g: Gram
    carb_g: Gram

    kcal: KCAL
    price: Price


class MealItem(TypedDict):
    """
    1食分の構成要素
    food: 100gあたりの栄養情報を持つ FoodItem
    grams: 実際に摂取する量(g)
    """

    food: FoodItem
    grams: Gram
