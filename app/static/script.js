document.getElementById("pdfFile").addEventListener("change", function(e) {
    const name = e.target.files[0]?.name || "Select Document";
    document.getElementById("fileNameDisplay").textContent = name;
    document.getElementById("currentDocName").textContent = name;
});

document.getElementById("analyzeBtn").addEventListener("click", performAnalysis);

async function performAnalysis() {
    const file = document.getElementById("pdfFile").files[0];
    if (!file) return;

    const abstract = document.getElementById("abstract");
    const thesis = document.getElementById("thesisLine");
    const startTime = performance.now();

    thesis.innerHTML = '<span style="color: var(--accent-bronze)">Processing Manuscript.</span>';
    abstract.textContent = "Synthesizing structural components and extracting key research nodes.";

    const formData = new FormData();
    formData.append("file", file);

    try {
        const res = await fetch("/analyse", { method: "POST", body: formData });
        const data = await res.json();
        
        const duration = ((performance.now() - startTime) / 1000).toFixed(1);
        document.getElementById("speed").textContent = duration + "s";
        document.getElementById("tokens").textContent = "2,140"; 

        thesis.textContent = data.abstract ? data.abstract.split('.')[0] + '.' : "Analysis complete.";
        abstract.textContent = data.abstract || "Detailed summary unavailable.";

        const fields = {
            "background": data.background,
            "contributions": data.contributions,
            "methodology": data.methodology,
            "key_results": data.key_results,
            "limitations_future_work": data.limitations_future_work
        };

        for (const [id, val] of Object.entries(fields)) {
            const el = document.getElementById(id);
            if(el) el.textContent = val || "No specific data extracted.";
        }

        if (data.flashcards) renderCards(data.flashcards);

    } catch (err) {
        thesis.textContent = "Analysis failed.";
        console.error(err);
    }
}

function renderCards(cards) {
    const container = document.getElementById("flashcardsContainer");
    container.innerHTML = "";
    cards.forEach(c => {
        const el = document.createElement("div");
        el.className = "flashcard";
        el.innerHTML = `
            <div class="flashcard-inner">
                <div class="front">${c.question}</div>
                <div class="back">${c.answer}</div>
            </div>`;
        el.onclick = () => el.classList.toggle("flipped");
        container.appendChild(el);
    });
}