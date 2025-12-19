import pytest

from services.report_service import (
    calculate_monthly_cost,
    aggregate_daily_macros,
)
from domain.common_alias import Price, Gram


def test_calculate_monthly_cost() -> None:
    daily_cost: Price = 900
    days: int = 30

    result = calculate_monthly_cost(
        daily_cost=daily_cost,
        days=days,
    )

    assert result == 27000


@pytest.mark.parametrize(
    "daily_macros, expected",
    [
        (
            [  # daily_macros
                {
                    "protein_g": 120.0,
                    "fat_g": 50.0,
                    "carb_g": 300.0,
                },
                {
                    "protein_g": 140.0,
                    "fat_g": 55.0,
                    "carb_g": 280.0,
                },
                {
                    "protein_g": 130.0,
                    "fat_g": 52.0,
                    "carb_g": 290.0,
                },
            ],
            {  # expected
                "protein_g": 390.0,
                "fat_g": 157.0,
                "carb_g": 870.0,
            },
        ),
        (
            [],  # daily_macros
            {  # expected
                "protein_g": 0.0,
                "fat_g": 0.0,
                "carb_g": 0.0,
            },
        ),
    ],
)
def test_aggregate_daily_macros(
    daily_macros: list[dict[str, Gram]],
    expected: dict[str, Gram],
) -> None:
    result = aggregate_daily_macros(daily_macros)

    assert result == expected
