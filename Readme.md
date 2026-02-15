# AI Research Web

A web application for processing research papers and PDFs using AI-powered analysis.

## Features

- PDF parsing and text extraction
- Intelligent document chunking
- AI-powered summarization and analysis
- Interactive web interface
- Flashcard generation for learning

## Tech Stack

- **Backend:** FastAPI, Python
- **LLM:** Groq API
- **Frontend:** HTML, CSS, JavaScript
- **PDF Processing:** PyMuPDF

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your API keys:
   ```
   GROQ_API_KEY=your_key_here
   ```

## Running the App

```bash
uvicorn app.main:app --reload
```

Visit `http://localhost:8000` in your browser.

## Project Structure

```
app/
├── api/          # API routes
├── services/     # AI, PDF, and chunking services
├── models/       # Response models
├── static/       # Frontend files
└── utils/        # Helper utilities
```

## License

MIT
