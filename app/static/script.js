document.getElementById("summary-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const button = document.getElementById("summarize-button");
    const text = document.getElementById("text-input").value;
    const resultBox = document.getElementById("result");
    const summaryText = document.getElementById("summary-text");

    // 🔁 Trigger bounce animation
    button.classList.remove("bouncing"); // Reset if already bouncing
    void button.offsetWidth;             // Force reflow
    button.classList.add("bouncing");    // Add bounce class

    button.disabled = true;

    try {
        const response = await fetch("/summarize", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });

        const data = await response.json();

        if (response.ok) {
            summaryText.textContent = data.summary;
        } else {
            summaryText.textContent = "Error: " + data.detail;
        }

        resultBox.style.display = "block";
    } catch (err) {
        summaryText.textContent = "Error connecting to server.";
        resultBox.style.display = "block";
    }

    button.disabled = false;
});
