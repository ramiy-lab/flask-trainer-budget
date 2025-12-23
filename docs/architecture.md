flask_trainer_budget/
├─ app.py
│
├─ config/
│   ├─ __init__.py
│   ├─ settings.py
│   └─ constants.py
│       ├─ MEAL_TIMINGS
│       ├─ MEAL_TIMING_LABELS
│       ├─ DEFAULT_KCAL_BY_TIMING
│       ├─ FOOD_CATEGORIES
│       ├─ FOOD_CATEGORY_LABELS
│       └─ FOOD_CATEGORY_ORDER
│
├─ data/
│   ├─ foods.json              ← protein含めて統合（categoryで区別）
│   └─ phase.json
│       ※ proteins.json 削除
│
├─ domain/
│   ├─ __init__.py
│   ├─ common_alias.py
│   │
│   ├─ food_types.py
│   │   └─ FoodItem TypedDict（category含む）
│   │
│   ├─ food_category_types.py      ← ★ 追加
│   │   └─ FoodCategory Literal
│   │
│   ├─ meal_timing_types.py        ← ★ 追加
│   │   └─ MealTiming Literal
│   │
│   ├─ phase_types.py
│   │   └─ PhaseSetting TypedDict
│   │
│   ├─ phase_enum.py
│   │   └─ Enum("bulk", "cut")
│   │
│   └─ recommendation_types.py     ← ★ 追加
│       └─ RecommendationResult TypedDict
│
├─ services/
│   ├─ meal_service.py
│   │
│   ├─ phase_service.py
│   │
│   ├─ recommendation_service.py   ← ★ 追加
│   │   └─ 推奨PFC / 差分 / 判定ロジック
│   │
│   ├─ report_service.py
│   │
│   └─ validators/
│       ├─ __init__.py              ← Facade
│       ├─ _common.py
│       ├─ food.py
│       └─ phase.py
│       ※ protein validators 削除
│
├─ templates/
│   ├─ base.html
│   ├─ meal_form.html              ← phase + timing + category UI 統合
│   └─ report.html
│       ※ protein_cycle.html 削除
│
├─ static/
│   ├─ css/
│   │   └─ style.css
│   └─ js/
│       ├─ meal.js                 ← category → food 切替対応
│       └─ report.js
│       ※ protein.js 削除
│
├─ tests/
│   ├─ test_meal_service.py
│   ├─ test_phase_service.py
│   ├─ test_report_service.py
│   ├─ test_recommendation_service.py   ← ★ 追加
│   │
│   ├─ test_food_validators.py
│   ├─ test_validators_common.py
│   └─ test_phase_validators.py
│       ※ protein系テスト削除
│
├─ requirements.txt
├─ README.md
└─ .env
