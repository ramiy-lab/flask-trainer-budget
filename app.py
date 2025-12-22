from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, Mapping, no_type_check

from flask import Flask, render_template, request, Response

from config.settings import AppConfig, load_config
from domain.common_alias import Price, Gram
from domain.food_types import FoodItem
from domain.protein_types import ProteinItem
from domain.phase_types import PhaseSetting
from services.meal_service import (
    calculate_meal_pfc,
    calculate_meal_price,
)
from services.protein_service import (
    calculate_total_servings,
    calculate_remaining_weight,
)
from services.phase_service import calculate_target_macros
from services.validators import (
    validate_food_items,
    validate_protein_items,
    validate_phase_settings,
)
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


def _load_food_data(*, config: AppConfig) -> LoadedData:
    foods_raw = _read_json_file(path=config.foods_json_path)
    foods = _parse_food_items(raw=foods_raw)
    food_by_id = {food["id"]: food for food in foods}
    return LoadedData(foods=foods, food_by_id=food_by_id)


def _load_protein_items(*, config: AppConfig) -> list[ProteinItem]:
    proteins_raw = _read_json_file(path=config.protein_json_path)

    if not isinstance(proteins_raw, list):
        raise ValueError("proteins.json must be a list")

    proteins: list[ProteinItem] = []
    for item in proteins_raw:
        if not isinstance(item, Mapping):
            raise ValueError("protein item must be an object")

        protein: ProteinItem = {
            "id": str(item["id"]),
            "name": str(item["name"]),
            "total_weight_g": float(item["total_weight_g"]),
            "serving_size_g": float(item["serving_size_g"]),
            "price": int(item["price"]),
        }
        proteins.append(protein)

    validate_protein_items(proteins)
    return proteins


def _load_phase_settings(*, config: AppConfig) -> list[PhaseSetting]:
    phases_raw = _read_json_file(path=config.phase_json_path)

    if not isinstance(phases_raw, list):
        raise ValueError("phase.json must be a list")

    phases: list[PhaseSetting] = []
    for item in phases_raw:
        if not isinstance(item, Mapping):
            raise ValueError("phase setting must be an object")

        phase_name = item["phase"]
        if phase_name not in ("bulk", "cut"):
            raise ValueError("invalid phase")

        phase_setting: PhaseSetting = {
            "phase": phase_name,
            "protein_ratio": float(item["protein_ratio"]),
            "fat_ratio": float(item["fat_ratio"]),
            "carb_ratio": float(item["carb_ratio"]),
        }
        phases.append(phase_setting)

    validate_phase_settings(phases)
    return phases


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


@app.get("/protein")
@no_type_check
def protein_cycle() -> Response:
    config: AppConfig = load_config()
    proteins: list[ProteinItem] = _load_protein_items(config=config)

    view_proteins: list[dict[str, object]] = []
    for protein in proteins:
        total_servings = calculate_total_servings(protein)
        remaining_weight = calculate_remaining_weight(
            protein=protein,
            used_servings=0,
        )

        view_proteins.append(
            {
                "protein": protein,
                "total_servings": total_servings,
                "remaining_weight_g": remaining_weight,
            }
        )

    return render_template(
        "protein_cycle.html",
        proteins=view_proteins,
    )


@app.get("/phase")
@no_type_check
def phase_form() -> Response:
    return render_template("phase_form.html")


@app.post("/phase")
@no_type_check
def phase_recommend() -> Response:
    config: AppConfig = load_config()
    phases: list[PhaseSetting] = _load_phase_settings(config=config)

    total_kcal = float(request.form["total_kcal"])
    phase_name = request.form["phase"]

    phase = next(p for p in phases if p["phase"] == phase_name)
    target = calculate_target_macros(total_kcal, phase)

    return render_template(
        "phase_result.html",
        phase=phase_name,
        total_kcal=total_kcal,
        target=target,
    )


@app.get("/report")
@no_type_check
def monthly_report() -> Response:
    """
    月間レポート表示 (Sprint4)
    ※ 今は固定のダミー日別データを使用
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
