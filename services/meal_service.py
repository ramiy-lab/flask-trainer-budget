from domain.food_types import FoodItem
from domain.common_alias import Gram, KCAL, Price


def calculate_meal_pdc(
    foods: list[FoodItem],
) -> dict[str, Gram | KCAL]:
    """
    1食分の食品リストから P/F/C/kcal 合計を算出する
    """
    total_protein: Gram = 0.0
    total_fat: Gram = 0.0
    total_carb: Gram = 0.0
    total_kcal: KCAL = 0.0

    for food in foods:
        total_protein += food["protein_g"]
        total_fat += food["fat_g"]
        total_carb += food["carb_g"]
        total_kcal += food["kcal"]

    return {
        "protein_g": total_protein,
        "fat_g": total_fat,
        "carb_g": total_carb,
        "kcal": total_kcal,
    }


def calculate_meal_price(
    foods: list[FoodItem],
) -> Price:
    """
    1食分の合計価格を算出する
    """
    total_price: Price = 0

    for food in foods:
        total_price += food["price"]

    return total_price
