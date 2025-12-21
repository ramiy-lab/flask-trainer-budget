from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, Mapping, no_type_check

from flask import Flask, render_template, request, Response

from config.settings import AppConfig, load_config
from domain.food_types import FoodItem
from services.meal_service import (
    calculate_meal_pfc,
    calculate_meal_price,
)
from services.validators import (
    validate_food_items,
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
        raise ValueError("food.json must be a list")

    foods: list[FoodItem] = []
    for item in raw:
        if not isinstance(item, Mapping):
            raise ValueError("food item must be an object")

        food: FoodItem = {
            "id": str(item["id"]),
            "name": str(item["name"]),
            "protein_g": float(item["protein_g"]),
            "fat_g": float(item["fat_g"]),
            "carb_g": float(item["carb_g"]),
            "kcal": float(item["kcal"]),
            "price": int(item["price"]),
        }
        foods.append(food)

    validate_food_items(foods)
    return foods


def _load_data(*, config: AppConfig) -> LoadedData:
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
    data: LoadedData = _load_data(config=config)

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
    data: LoadedData = _load_data(config=config)

    selected_ids: list[str] = request.form.getlist("food_ids")
    selected_foods: list[FoodItem] = _get_selected_foods(
        data=data,
        selected_ids=selected_ids,
    )

    macros = calculate_meal_pfc(selected_foods)
    price = calculate_meal_price(selected_foods)

    result = {
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
        result=result,
    )

if __name__ == "__main__":
    app.run(debug=True)
