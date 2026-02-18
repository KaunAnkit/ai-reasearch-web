const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('pdfFile');
const fileNameDisplay = document.getElementById('fileNameDisplay');
const analyzeBtn = document.getElementById('analyzeBtn');
const currentDocName = document.getElementById('currentDocName');

dropZone.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        const name = file.name;
        fileNameDisplay.textContent = name;
        currentDocName.textContent = name;
        
        fileNameDisplay.style.color = 'var(--accent-bronze)';
        dropZone.style.borderColor = 'var(--accent-bronze)';
        dropZone.style.background = 'rgba(255, 255, 255, 0.5)';
    }
});

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = 'var(--accent-blue)';
});

dropZone.addEventListener('dragleave', () => {
    dropZone.style.borderColor = 'var(--border)';
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    const files = e.dataTransfer.files;
    if (files.length) {
        fileInput.files = files;
        fileInput.dispatchEvent(new Event('change'));
    }
});

analyzeBtn.addEventListener('click', performAnalysis);

async function performAnalysis() {
    const file = fileInput.files[0];
    if (!file) {
        alert("Please select a manuscript first.");
        return;
    }

    const abstract = document.getElementById("abstract");
    const thesis = document.getElementById("thesisLine");
    const startTime = performance.now();

    analyzeBtn.disabled = true;
    analyzeBtn.textContent = "Analyzing...";
    thesis.innerHTML = '<span style="color: var(--accent-bronze)">Processing Manuscript.</span>';
    abstract.textContent = "Synthesizing structural components and extracting key research nodes.";

    const formData = new FormData();
    formData.append("file", file);

    try {
        const res = await fetch("/analyse", { method: "POST", body: formData });
        
        if (!res.ok) throw new Error("Server responded with an error.");
        
        const data = await res.json();
        
        const duration = ((performance.now() - startTime) / 1000).toFixed(1);
        document.getElementById("speed").textContent = duration + "s";
        
        const tokenElement = document.getElementById("tokens");
        if (tokenElement) tokenElement.textContent = data.tokens || "2,140"; 

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
            if(el) {
                el.textContent = val || "No specific data extracted.";
                el.style.opacity = "0";
                setTimeout(() => { 
                    el.style.opacity = "1"; 
                    el.style.transition = "opacity 0.5s"; 
                }, 100);
            }
        }

        if (data.flashcards) {
            renderCards(data.flashcards);
        }

    } catch (err) {
        thesis.textContent = "Analysis failed.";
        abstract.textContent = "Ensure the server is running and the PDF is not encrypted.";
        console.error("Analysis Error:", err);
    } finally {
        analyzeBtn.disabled = false;
        analyzeBtn.textContent = "Analyze Document";
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
                <div class="front">
                    <p>${c.question}</p>
                </div>
                <div class="back">
                    <p>${c.answer}</p>
                </div>
            </div>`;
        
        el.onclick = () => el.classList.toggle("flipped");
        container.appendChild(el);
    });
}
