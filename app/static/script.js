console.log("SCRIPT LOADED");

document.getElementById("analyzeBtn").addEventListener("click", uploadPdf);

async function uploadPdf() {
    const fileInput = document.getElementById("pdfFile");
    const file = fileInput.files[0];

    if (!file) {
        alert("Select a file");
        return;
    }

    const summaryElement = document.getElementById("summaryText");
    const flashcardContainer = document.getElementById("flashcardsContainer");
    
    summaryElement.innerText = "Processing...";
    flashcardContainer.innerHTML = ""; 

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("/analyse", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        // 1. Update Summary
        summaryElement.innerText = data.summary || "No summary available.";

        // 2. Render Flashcards if they exist
        if (data.flashcards && data.flashcards.length > 0) {
            renderFlashcards(data.flashcards);
        }

    } catch (error) {
        console.error(error);
        summaryElement.innerText = "There was an error while generating summary";
    }
}

function renderFlashcards(flashcards) {
    const container = document.getElementById("flashcardsContainer");
    
    flashcards.forEach(cardData => {
        const card = document.createElement("div");
        card.className = "flashcard";
        
        card.innerHTML = `
            <div class="flashcard-inner">
                <div class="front">
                    <p>${cardData.question}</p>
                </div>
                <div class="back">
                    <p>${cardData.answer}</p>
                </div>
            </div>
        `;

        // Add flip event
        card.addEventListener("click", () => {
            card.classList.toggle("flipped");
        });

        container.appendChild(card);
    });
}