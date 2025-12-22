(function () {
  "use strict";

  function readFoods() {
    const el = document.getElementById("foods-json");
    if (!el) return [];
    try {
      return JSON.parse(el.textContent || "[]");
    } catch {
      return [];
    }
  }

  function buildFoodMap(foods) {
    const map = new Map();
    for (const food of foods) {
      map.set(food.id, food);
    }
    return map;
  }

  function getSelectedIds() {
    const nodes = document.querySelectorAll("input.food-checkbox:checked");
    const ids = [];
    for (const node of nodes) {
      ids.push(node.value);
    }
    return ids;
  }

  // ★ 量(g)を考慮した集計
  function sumSelected(foodMap, selectedIds) {
    let protein = 0.0;
    let fat = 0.0;
    let carb = 0.0;
    let kcal = 0.0;
    let price = 0.0;

    for (const id of selectedIds) {
      const food = foodMap.get(id);
      if (!food) continue;

      const range = document.querySelector(
        `.amount-range[data-food-id="${id}"]`
      );
      const grams = range ? Number(range.value) : 100;
      const ratio = grams / 100.0;

      protein += Number(food.protein_g) * ratio;
      fat += Number(food.fat_g) * ratio;
      carb += Number(food.carb_g) * ratio;
      kcal += Number(food.kcal) * ratio;
      price += Number(food.price) * ratio;
    }

    return { protein, fat, carb, kcal, price };
  }

  function setText(id, value) {
    const el = document.getElementById(id);
    if (!el) return;
    el.textContent = value;
  }

  function renderSums(sums) {
    setText("sum-protein", sums.protein.toFixed(1));
    setText("sum-fat", sums.fat.toFixed(1));
    setText("sum-carb", sums.carb.toFixed(1));
    setText("sum-kcal", sums.kcal.toFixed(1));
    setText("sum-price", String(Math.trunc(sums.price)));
  }

  function setup() {
    const foods = readFoods();
    const foodMap = buildFoodMap(foods);

    function recalc() {
      const ids = getSelectedIds();
      const sums = sumSelected(foodMap, ids);
      renderSums(sums);
    }

    // チェック切替
    document.addEventListener("change", (e) => {
      const target = e.target;
      if (target && target.classList.contains("food-checkbox")) {
        recalc();
      }
    });

    // ★ g数変更（スライダー）
    document.addEventListener("input", (e) => {
      const target = e.target;
      if (target.classList.contains("amount-range")) {
        const valueSpan = target
          .closest(".food-item")
          .querySelector(".amount-value");

        valueSpan.textContent = target.value;

        // 量変更時も再計算
        recalc();
      }
    });

    // 初期表示
    recalc();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", setup);
  } else {
    setup();
  }
})();
