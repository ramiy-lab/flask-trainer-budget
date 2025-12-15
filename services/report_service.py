from domain.common_alias import Price, Gram


def calculate_monthly_cost(
    daily_cost: Price,
    days: int,
) -> Price:
    """
    1日の食費から月間のコストを算出する
    """
    return daily_cost * days


def aggregate_daily_macros(
    daily_macros: list[dict[str, Gram]],
) -> dict[str, Gram]:
    """
    日別 P/F/C のリストから合計を算出する
    """
    total_protein: Gram = 0.0
    total_fat: Gram = 0.0
    total_carb: Gram = 0.0

    for macros in daily_macros:
        total_protein += macros["protein_g"]
        total_fat += macros["fat_g"]
        total_carb += macros["carb_g"]

    return {
        "protein_g": total_protein,
        "fat_g": total_fat,
        "carb_g": total_carb,
    }
