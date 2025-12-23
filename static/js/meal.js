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
    return Array.from(
      document.querySelectorAll(".food-checkbox:checked"),
      (el) => el.value
    );
  }

  function sumSelected(foodMap, ids) {
    let protein = 0, fat = 0, carb = 0, kcal = 0, price = 0;

    for (const id of ids) {
      const food = foodMap.get(id);
      if (!food) continue;

      const range = document.querySelector(
        `.amount-range[data-food-id="${id}"]`
      );
      const grams = range ? Number(range.value) : 100;
      const ratio = grams / 100;

      protein += food.protein_g * ratio;
      fat += food.fat_g * ratio;
      carb += food.carb_g * ratio;
      kcal += food.kcal * ratio;
      price += food.price * ratio;
    }

    return { protein, fat, carb, kcal, price };
  }

  function renderSelected(foodMap, ids) {
    const ul = document.getElementById("selected-items");
    if (!ul) return;

    ul.innerHTML = "";

    if (ids.length === 0) {
      ul.innerHTML = "<li class='muted'>未選択</li>";
      return;
    }

    for (const id of ids) {
      const food = foodMap.get(id);
      const range = document.querySelector(
        `.amount-range[data-food-id="${id}"]`
      );
      const grams = range ? range.value : 100;

      const li = document.createElement("li");
      li.textContent = `${food.name}：${grams} g`;
      ul.appendChild(li);
    }
  }

  function renderSums(sums) {
    document.getElementById("sum-protein").textContent = sums.protein.toFixed(1);
    document.getElementById("sum-fat").textContent = sums.fat.toFixed(1);
    document.getElementById("sum-carb").textContent = sums.carb.toFixed(1);
    document.getElementById("sum-kcal").textContent = sums.kcal.toFixed(1);
    document.getElementById("sum-price").textContent = Math.trunc(sums.price);
  }

  function setup() {
    const foods = readFoods();
    const foodMap = buildFoodMap(foods);

    function recalc() {
      const ids = getSelectedIds();
      const sums = sumSelected(foodMap, ids);
      renderSums(sums);
      renderSelected(foodMap, ids);
    }

    document.addEventListener("change", (e) => {
      if (e.target.classList.contains("food-checkbox")) recalc();
    });

    document.addEventListener("input", (e) => {
      if (!e.target.classList.contains("amount-range")) return;

      const item = e.target.closest(".food-item");
      item.querySelector(".amount-value").textContent = e.target.value;
      item.querySelector(".amount-hidden").value = e.target.value;

      recalc();
    });

    recalc();
  }

  document.readyState === "loading"
    ? document.addEventListener("DOMContentLoaded", setup)
    : setup();
})();
