document.getElementById("summary-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const button = document.getElementById("summarize-button");
  const text = document.getElementById("text-input").value;
  const resultBox = document.getElementById("result");
  const summaryText = document.getElementById("summary-text");
  const downloadLink = document.getElementById("download-link");

  // 🔁 Trigger bounce animation
  button.classList.remove("bouncing");
  void button.offsetWidth;
  button.classList.add("bouncing");

  // 🔄 Reset previous state
  button.disabled = true;
  summaryText.textContent = "";
  downloadLink.style.display = "none";
  resultBox.style.display = "none";

  try {
    const response = await fetch("/summarize", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });

    const data = await response.json();

    if (response.ok) {
      summaryText.textContent = data.summary;
      resultBox.style.display = "block";

      if (data.filename) {
        const filename = data.filename;
        downloadLink.href = `/download/${filename}`;
        downloadLink.setAttribute("download", filename); // Suggested "Save As" name
        downloadLink.style.display = "inline-block";
      }
    } else {
      summaryText.textContent = "❌ Error: " + data.detail;
      resultBox.style.display = "block";
    }
  } catch (err) {
    summaryText.textContent = "❌ Error connecting to server.";
    resultBox.style.display = "block";
  }

  button.disabled = false;
});
