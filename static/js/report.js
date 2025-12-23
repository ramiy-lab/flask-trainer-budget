(function () {
  "use strict";

  function getFoods() {
    const el = document.getElementById("foods-json");
    if (!el) return [];
    try {
      return JSON.parse(el.textContent || "[]");
    } catch {
      return [];
    }
  }

  function setupCategorySelect(foods) {
    const select = document.getElementById("category-select");
    if (!select) return;

    const categories = [...new Set(foods.map(f => f.category))];

    for (const category of categories) {
      const option = document.createElement("option");
      option.value = category;
      option.textContent = category;
      select.appendChild(option);
    }

    select.addEventListener("change", () => {
      filterFoodsByCategory(select.value);
    });
  }

  function filterFoodsByCategory(category) {
    const items = document.querySelectorAll(".food-item");
    items.forEach(item => {
      const itemCategory = item.getAttribute("data-category");
      if (!category || itemCategory === category) {
        item.style.display = "";
      } else {
        item.style.display = "none";
      }
    });
  }

  function updateAmount(range) {
    const foodId = range.dataset.foodId;
    const value = range.value;

    const valueSpan = range.closest(".amount-control")
      ?.querySelector(".amount-value");
    if (valueSpan) {
      valueSpan.textContent = value;
    }

    const hidden = document.querySelector(
      `.amount-hidden[data-food-id="${foodId}"]`
    );
    if (hidden) {
      hidden.value = value;
    }
  }

  function setupAmountControls() {
    const ranges = document.querySelectorAll(".amount-range");
    ranges.forEach(range => {
      range.addEventListener("input", () => updateAmount(range));
    });
  }

  function setup() {
    const foods = getFoods();
    setupCategorySelect(foods);
    setupAmountControls();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", setup);
  } else {
    setup();
  }
})();
