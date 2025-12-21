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

  function sumSelected(foodMap, selectedIds) {
    let protein = 0.0;
    let fat = 0.0;
    let carb = 0.0;
    let kcal = 0.0;
    let price = 0;

    for (const id of selectedIds) {
      const food = foodMap.get(id);
      if (!food) continue;

      protein += Number(food.protein_g);
      fat += Number(food.fat_g);
      carb += Number(food.carb_g);
      kcal += Number(food.kcal);
      price += Number(food.price);
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

    document.addEventListener("change", (e) => {
      const target = e.target;
      if (target && target.classList && target.classList.contains("food-checkbox")) {
        recalc();
      }
    });

    // 初期表示（サーバー側でチェック済み状態から再計算）
    recalc();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", setup);
  } else {
    setup();
  }
})();
