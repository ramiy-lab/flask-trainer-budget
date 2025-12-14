from typing import TypedDict

from domain.common_alias import Gram, KCAL, Price, FoodID


class FoodItem(TypedDict):
    id: FoodID
    name: str

    protein_g: Gram
    fat_g: Gram
    carb_g: Gram

    kcal: KCAL
    price: Price
