from domain.food_category_types import FoodCategory


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
