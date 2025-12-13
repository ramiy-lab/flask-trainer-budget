from typing import TypedDict

from domain.common_alias import Gram, Price, ProteinID


class ProteinItem(TypedDict):
    id: ProteinID
    name: str

    total_weight_g: Gram
    serving_size_g: Gram

    price: Price
