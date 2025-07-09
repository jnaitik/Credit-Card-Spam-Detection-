document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("fraudForm");
  const resultBox = document.getElementById("result");

  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    const data = {};

    // Format all values correctly
    formData.forEach((value, key) => {
      if (value === "true") value = true;
      else if (value === "false") value = false;
      else if (!isNaN(value) && value.trim() !== "") value = Number(value);
      data[key] = value;
    });

    try {
      const res = await fetch("http://localhost:5000/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      const result = await res.json();

      // Check if error returned
      if (result.error) {
        resultBox.innerHTML = `<div class="error">❌ Error: ${result.error}</div>`;
        console.error("Backend Error:", result.error);
        return;
      }

      const prediction = result.prediction ?? "N/A";
      const confidence = result.confidence ?? "N/A";
      const explanation = result.explanation ?? "No explanation available.";

      resultBox.innerHTML = `
        <div>
          <strong>Prediction:</strong> ${prediction === 1 ? "🚨 Fraud Detected" : "✅ Safe Transaction"}<br>
          <strong>Confidence:</strong> ${confidence}%<br>
          <strong>AI Explanation:</strong><br> ${explanation}
        </div>
      `;
    } catch (error) {
      console.error("Request Failed:", error);
      resultBox.innerHTML = `<div class="error">❌ Failed to connect to backend. Is it running?</div>`;
    }
  });
});
