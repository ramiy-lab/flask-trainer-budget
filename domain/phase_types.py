from typing import TypedDict, Literal

from domain.common_alias import Ratio


PhaseName = Literal["bulk", "cut"]


class PhaseSetting(TypedDict):
    phase: PhaseName

    protein_ratio: Ratio
    fat_ratio: Ratio
    carb_ratio: Ratio
