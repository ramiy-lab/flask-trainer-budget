(function () {
  "use strict";

  function readReportData() {
    const el = document.getElementById("report-data");
    if (!el) return [];
    try {
      return JSON.parse(el.textContent || "[]");
    } catch {
      return [];
    }
  }

  function buildPfcChart(ctx, records) {
    const labels = records.map((_, i) => `Day ${i + 1}`);
    const protein = records.map(r => r.protein_g);
    const fat = records.map(r => r.fat_g);
    const carb = records.map(r => r.carb_g);

    new Chart(ctx, {
      type: "line",
      data: {
        labels,
        datasets: [
          { label: "Protein (g)", data: protein },
          { label: "Fat (g)", data: fat },
          { label: "Carb (g)", data: carb },
        ],
      },
      options: {
        responsive: true,
        scales: {
          y: { beginAtZero: true },
        },
      },
    });
  }

  function buildCostChart(ctx, records) {
    const labels = records.map((_, i) => `Day ${i + 1}`);
    const costs = records.map(r => r.price);

    new Chart(ctx, {
      type: "bar",
      data: {
        labels,
        datasets: [
          {
            label: "Daily Cost (¥)",
            data: costs,
          },
        ],
      },
      options: {
        responsive: true,
        scales: {
          y: { beginAtZero: true },
        },
      },
    });
  }

  function setup() {
    const records = readReportData();
    if (records.length === 0) return;

    const pfcCtx = document.getElementById("pfcChart");
    const costCtx = document.getElementById("costChart");

    if (pfcCtx) {
      buildPfcChart(pfcCtx, records);
    }
    if (costCtx) {
      buildCostChart(costCtx, records);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", setup);
  } else {
    setup();
  }
})();