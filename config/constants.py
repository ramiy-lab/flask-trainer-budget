from domain.food_category_types import FoodCategory
from domain.meal_timing_types import MealTiming


FOOD_CATEGORIES: list[FoodCategory] = [
    "meat",
    "protein",
    "soy",
    "fish",
    "grain",
    "dairy",
    "vegetable",
    "fruit",
]

FOOD_CATEGORY_LABELS: dict[FoodCategory, str] = {
    "meat": "肉",
    "soy": "豆製品",
    "fish": "魚",
    "protein": "プロテイン",
    "grain": "穀物",
    "dairy": "乳製品",
    "vegetable": "野菜",
    "fruit": "果物",
}

# UI表示順を明示的に管理
FOOD_CATEGORY_ORDER: list[FoodCategory] = [
    "meat",
    "protein",
    "soy",
    "fish",
    "grain",
    "dairy",
    "vegetable",
    "fruit",
]

MEAL_TIMINGS: list[MealTiming] = [
    "after_wakeup",
    "breakfast",
    "morning_snack",
    "lunch",
    "afternoon_snack",
    "dinner",
    "night_snack",
    "other",
]

MEAL_TIMING_LABELS: dict[MealTiming, str] = {
    "after_wakeup": "起床後",
    "breakfast": "朝食",
    "morning_snack": "午前間食",
    "lunch": "昼食",
    "afternoon_snack": "午後間食",
    "dinner": "夕食",
    "night_snack": "夜間食",
    "other": "その他",
}
DEFAULT_KCAL_BY_TIMING: dict[MealTiming, float] = {
    "after_wakeup": 200.0,
    "breakfast": 600.0,
    "morning_snack": 200.0,
    "lunch": 700.0,
    "afternoon_snack": 200.0,
    "dinner": 700.0,
    "night_snack": 200.0,
    "other": 300.0,
}