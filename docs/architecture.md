# Architecture

flask_trainer_budget/
├─ app.py
├─ config/
│   ├─ __init__.py
│   ├─ settings.py
│   └─ constants.py
├─ data/
│   ├─ foods.json
│   ├─ proteins.json
│   └─ phase.json
├─ domain/
│   ├─ __init__.py
│   ├─ food_types.py        ← FoodItem TypedDict / TypeAlias
│   ├─ protein_types.py
│   ├─ phase_types.py       ← PhaseSetting TypedDict
│   ├─ phase_enum.py        ← Enum("bulk", "cut")
│   └─ common_alias
├─ services/
│   ├─ meal_service.py
│   ├─ protein_service.py
│   ├─ phase_service.py
│   ├─ report_service.py
│   └─ validators.py
├─ templates/
│   ├─ base.html
│   ├─ meal_form.html
│   ├─ protein_cycle.html
│   └─ report.html
├─ static/
│   ├─ css/
│   │   └─ style.css
│   └─ js/
│       ├─ meal.js
│       ├─ protein.js
│       └─ report.js
├─ tests/
│   ├─ test_meal_service.py
│   ├─ test_protein.py
│   └─ test_phase.py
├─ requirements.txt
├─ README.md
└─ .env
