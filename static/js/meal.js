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
    let protein = 0,
      fat = 0,
      carb = 0,
      kcal = 0,
      price = 0;

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

  // =========================
  // リアルタイム：選択中の食材
  // =========================
  function renderSelected(foodMap, ids) {
    const tbody = document.getElementById("realtime-items-body");
    if (!tbody) return;

    tbody.innerHTML = "";

    if (ids.length === 0) {
      const tr = document.createElement("tr");
      tr.innerHTML = `<th class="muted">未選択</th><td></td>`;
      tbody.appendChild(tr);
      return;
    }

    for (const id of ids) {
      const food = foodMap.get(id);
      if (!food) continue;

      const range = document.querySelector(
        `.amount-range[data-food-id="${id}"]`
      );
      const grams = range ? range.value : 100;

      const tr = document.createElement("tr");
      tr.innerHTML = `
        <th>${food.name}</th>
        <td class="muted">${grams} g</td>
      `;
      tbody.appendChild(tr);
    }
  }

  function renderSums(sums) {
    document.getElementById("sum-protein").textContent = sums.protein.toFixed(1);
    document.getElementById("sum-fat").textContent = sums.fat.toFixed(1);
    document.getElementById("sum-carb").textContent = sums.carb.toFixed(1);
    document.getElementById("sum-kcal").textContent = sums.kcal.toFixed(1);
    document.getElementById("sum-price").textContent = Math.trunc(sums.price);
  }

  // =========================
  // カテゴリ選択（data-has-category 方式）
  // =========================
  function setupCategorySelect(foods) {
    const select = document.getElementById("category-select");
    const grid = document.getElementById("food-grid");
    if (!select || !grid) return;

    const categories = Array.from(new Set(foods.map((f) => f.category)));

    for (const category of categories) {
      const option = document.createElement("option");
      option.value = category;
      option.textContent = category;
      select.appendChild(option);
    }

    select.addEventListener("change", () => {
      const selected = select.value;

      // カテゴリ未選択 → 全非表示（CSSに任せる）
      if (!selected) {
        grid.dataset.hasCategory = "false";
        return;
      }

      // カテゴリ選択済み
      grid.dataset.hasCategory = "true";

      const items = grid.querySelectorAll(".food-item");
      items.forEach((item) => {
        item.style.display =
          item.dataset.category === selected ? "" : "none";
      });
    });
  }

  function setup() {
    const foods = readFoods();
    const foodMap = buildFoodMap(foods);

    setupCategorySelect(foods);

    function recalc() {
      const ids = getSelectedIds();
      const sums = sumSelected(foodMap, ids);
      renderSums(sums);
      renderSelected(foodMap, ids);
    }

    document.addEventListener("change", (e) => {
      if (e.target.classList.contains("food-checkbox")) {
        recalc();
      }
    });

    document.addEventListener("input", (e) => {
      if (!e.target.classList.contains("amount-range")) return;

      const item = e.target.closest(".food-item");
      if (!item) return;

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
