from domain.food_types import MealItem
from domain.common_alias import Gram, KCAL, Price


def calculate_meal_pfc(
    items: list[MealItem],
) -> dict[str, Gram | KCAL]:
    """
    量(g)を考慮して、1食分の P/F/C/kcal 合計を算出する
    """
    total_protein: Gram = 0.0
    total_fat: Gram = 0.0
    total_carb: Gram = 0.0
    total_kcal: KCAL = 0.0

    for item in items:
        food = item["food"]
        grams = item["grams"]

        if grams <= 0:
            continue

        ratio = grams / 100.0

        total_protein += food["protein_g"] * ratio
        total_fat += food["fat_g"] * ratio
        total_carb += food["carb_g"] * ratio
        total_kcal += food["kcal"] * ratio

    return {
        "protein_g": total_protein,
        "fat_g": total_fat,
        "carb_g": total_carb,
        "kcal": total_kcal,
    }


def calculate_meal_price(
    items: list[MealItem],
) -> Price:
    """
    1食分の合計価格を算出する
    """
    total_price: float = 0

    for item in items:
        food = item["food"]
        grams = item["grams"]

        if grams <= 0:
            continue

        ratio = grams / 100.0
        total_price += food["price"] * ratio

    return int(total_price)
