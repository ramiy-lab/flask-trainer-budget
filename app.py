from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, Mapping, no_type_check

from flask import Flask, render_template, request, Response

from config.settings import AppConfig, load_config
from domain.common_alias import Price, Gram
from domain.food_category_types import FoodCategory
from domain.food_types import FoodItem
from services.meal_service import (
    calculate_meal_pfc,
    calculate_meal_price,
)
from services.validators import validate_food_items
from services.report_service import (
    aggregate_daily_macros,
    calculate_monthly_cost,
)


app: Final[Flask] = Flask(__name__)


@dataclass(frozen=True)
class LoadedData:
    foods: list[FoodItem]
    food_by_id: dict[str, FoodItem]


def _read_json_file(*, path: Path) -> Any:
    with open(path, mode="r", encoding="utf-8") as f:
        return json.load(f)


def _parse_food_items(*, raw: Any) -> list[FoodItem]:
    if not isinstance(raw, list):
        raise ValueError("foods.json must be a list")

    foods: list[FoodItem] = []
    for item in raw:
        if not isinstance(item, Mapping):
            raise ValueError("food item must be an object")

        category_raw = item["category"]
        if not isinstance(category_raw, str):
            raise ValueError("category must be a string")

        category: FoodCategory = category_raw  # type: ignore[assignment]

        food: FoodItem = {
            "id": str(item["id"]),
            "name": str(item["name"]),
            "category": category,
            "protein_g": float(item["protein_g"]),
            "fat_g": float(item["fat_g"]),
            "carb_g": float(item["carb_g"]),
            "kcal": float(item["kcal"]),
            "price": int(item["price"]),
        }
        foods.append(food)

    validate_food_items(foods)
    return foods


def _load_food_data(*, config: AppConfig) -> LoadedData:
    foods_raw = _read_json_file(path=config.foods_json_path)
    foods = _parse_food_items(raw=foods_raw)
    food_by_id = {food["id"]: food for food in foods}
    return LoadedData(foods=foods, food_by_id=food_by_id)


def _get_selected_foods(
    *,
    data: LoadedData,
    selected_ids: list[str],
) -> list[FoodItem]:
    return [
        data.food_by_id[food_id]
        for food_id in selected_ids
        if food_id in data.food_by_id
    ]


@app.get("/")
@no_type_check
def meal_form() -> Response:
    config: AppConfig = load_config()
    data: LoadedData = _load_food_data(config=config)

    return render_template(
        "meal_form.html",
        foods=data.foods,
        selected_ids=[],
        result=None,
    )


@app.post("/")
@no_type_check
def meal_submit() -> Response:
    config: AppConfig = load_config()
    data: LoadedData = _load_food_data(config=config)

    selected_ids: list[str] = request.form.getlist("food_ids")

    amounts: dict[str, float] = {
        food_id: float(request.form.get(f"food_amounts[{food_id}]", 100))
        for food_id in selected_ids
    }

    selected_foods: list[FoodItem] = _get_selected_foods(
        data=data,
        selected_ids=selected_ids,
    )

    meal_items = [
        {
            "food": food,
            "grams": amounts.get(food["id"], 100.0),
        }
        for food in selected_foods
    ]

    macros = calculate_meal_pfc(meal_items)
    price = calculate_meal_price(meal_items)

    result = {
        "items": meal_items,
        "protein_g": macros["protein_g"],
        "fat_g": macros["fat_g"],
        "carb_g": macros["carb_g"],
        "kcal": macros["kcal"],
        "price": price,
    }

    return render_template(
        "meal_form.html",
        foods=data.foods,
        selected_ids=selected_ids,
        amounts=amounts,
        result=result,
    )


@app.get("/report")
@no_type_check
def monthly_report() -> Response:
    """
    月間レポート表示
    ※ 現在はダミー日別データを使用
    """
    daily_records: list[dict[str, Gram | Price]] = [
        {
            "protein_g": 120.0,
            "fat_g": 50.0,
            "carb_g": 300.0,
            "price": 900,
        },
        {
            "protein_g": 140.0,
            "fat_g": 55.0,
            "carb_g": 280.0,
            "price": 950,
        },
        {
            "protein_g": 130.0,
            "fat_g": 55.0,
            "carb_g": 280.0,
            "price": 950,
        },
    ]

    macros = aggregate_daily_macros(
        [
            {
                "protein_g": d["protein_g"],
                "fat_g": d["fat_g"],
                "carb_g": d["carb_g"],
            }
            for d in daily_records
        ]
    )

    daily_costs: list[Price] = [int(d["price"]) for d in daily_records]
    total_cost: Price = sum(daily_costs)
    avg_daily_cost: Price = total_cost // len(daily_costs)

    monthly_cost: Price = calculate_monthly_cost(
        daily_cost=avg_daily_cost,
        days=30,
    )

    return render_template(
        "report.html",
        daily_records=daily_records,
        macros=macros,
        total_cost=monthly_cost,
    )


if __name__ == "__main__":
    app.run(debug=True)
