from typing import Iterable

from domain.protein_types import ProteinItem
from domain.common_alias import Gram, Price
from ._common import _ensure_positive_float, _ensure_positive_int


def validate_protein_item(protein: ProteinItem) -> None:
    total_weight: Gram = protein["total_weight_g"]
    serving_size: Gram = protein["serving_size_g"]
    price: Price = protein["price"]

    _ensure_positive_float(total_weight, "total_weight_g")
    _ensure_positive_float(serving_size, "serving_size_g")
    _ensure_positive_int(price, "price")

    if serving_size == 0:
        raise ValueError("serving_size_g must be greater than 0")

    if serving_size > total_weight:
        raise ValueError("serving_size_g must not exceed total_weight_g")


def validate_protein_items(proteins: Iterable[ProteinItem]) -> None:
    for protein in proteins:
        validate_protein_item(protein)
