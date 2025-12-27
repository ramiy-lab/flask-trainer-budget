from domain.phase_types import PhaseSetting
from domain.recommendation_types import Macros
from domain.common_alias import KCAL, Gram


def calculate_target_macros(
    total_kcal: KCAL,
    phase: PhaseSetting,
) -> Macros:
    """
    Phase 設定と総 kcal から目標 P/F/C(g) を算出する
    """
    protein_kcal: KCAL = total_kcal * phase["protein_ratio"]
    fat_kcal: KCAL = total_kcal * phase["fat_ratio"]
    carb_kcal: KCAL = total_kcal * phase["carb_ratio"]

    protein_g: Gram = protein_kcal / 4.0
    fat_g: Gram = fat_kcal / 9.0
    carb_g: Gram = carb_kcal / 4.0

    return {
        "protein_g": protein_g,
        "fat_g": fat_g,
        "carb_g": carb_g,
        "kcal": total_kcal,
    }
