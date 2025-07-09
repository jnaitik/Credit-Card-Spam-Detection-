document.addEventListener("DOMContentLoaded", async () => {
  try {
    const res = await fetch("http://localhost:5000/api/dashboard-data");
    const data = await res.json();

    if (data.error) {
      throw new Error(data.error);
    }

    // Create chart only if the element exists
    const createChart = (id, config) => {
      const ctx = document.getElementById(id);
      if (ctx) new Chart(ctx, config);
    };

    // 1. Fraud Stats
    createChart("fraudStatsChart", {
      type: "bar",
      data: {
        labels: Object.keys(data.fraudStats).map(k => k === "1" ? "Fraud" : "Safe"),
        datasets: [{
          label: "Count",
          data: Object.values(data.fraudStats),
          backgroundColor: ["#e74c3c", "#2ecc71"]
        }]
      }
    });

    // 2. Transaction Type
    createChart("transactionTypeChart", {
      type: "pie",
      data: {
        labels: Object.keys(data.transactionType),
        datasets: [{
          data: Object.values(data.transactionType),
          backgroundColor: ["#3498db", "#f1c40f", "#9b59b6", "#1abc9c"]
        }]
      }
    });

    // 3. Merchant Category
    createChart("merchantCategoryChart", {
      type: "pie",
      data: {
        labels: Object.keys(data.merchantCategory),
        datasets: [{
          data: Object.values(data.merchantCategory),
          backgroundColor: ["#e67e22", "#16a085", "#2980b9", "#8e44ad"]
        }]
      }
    });

    // 4. Card Presence
    createChart("cardPresenceChart", {
      type: "bar",
      data: {
        labels: Object.keys(data.cardPresence).map(k => k === "1" ? "Card Present" : "Card Not Present"),
        datasets: [{
          label: "Transactions",
          data: Object.values(data.cardPresence),
          backgroundColor: ["#27ae60", "#d35400"]
        }]
      }
    });

    // 5. Average Amount
    createChart("avgAmountChart", {
      type: "bar",
      data: {
        labels: Object.keys(data.avgAmounts).map(k => k === "1" ? "Fraud" : "Safe"),
        datasets: [{
          label: "Avg Amount ($)",
          data: Object.values(data.avgAmounts),
          backgroundColor: ["#c0392b", "#2980b9"]
        }]
      }
    });

  } catch (err) {
    alert("❌ Error loading dashboard data. Is backend running?");
    console.error("Dashboard Load Error:", err);
  }
});
