from domain.protein_types import ProteinItem
from domain.common_alias import Gram


def calculate_total_servings(
    protein: ProteinItem,
) -> int:
    """
    1袋あたりのそう摂取回数を算出する
    """
    total_weight: Gram = protein["total_weight_g"]
    serving_size: Gram = protein["serving_size_g"]

    return int(total_weight // serving_size)


def calculate_remaining_weight(protein: ProteinItem, used_servings: int) -> Gram:
    """
    既に摂取した回数から残量(g)を算出する
    """
    consumed_weight: Gram = protein["serving_size_g"] * used_servings
    remaining: Gram = protein["total_weight_g"] - consumed_weight

    return max(remaining, 0.0)
