(function () {
  "use strict";

  function recalc(input) {
    const total = Number(input.dataset.total);
    const serving = Number(input.dataset.serving);
    const used = Number(input.value);

    const consumed = serving * used;
    const remaining = Math.max(total - consumed, 0);

    const container = input.closest(".protein-item");
    const output = container.querySelector(".remaining");

    output.textContent = remaining.toFixed(1);

    if (remaining <= serving * 3) {
      container.classList.add("warning");
    } else {
      container.classList.remove("warning");
    }
  }

  document.addEventListener("input", (e) => {
    const target = e.target;
    if (target.classList.contains("serving-input")) {
      recalc(target);
    }
  });
})();