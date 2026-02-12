import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"


def generate_summary(text):

    prompt = f""" 
You are an academic research assistant.

Do the following:
1. Provide a concise summary.
2. Extract key concepts (bullet list).
3. Generate 5 flashcards (Q & A format).

Text:
{text}
"""
    

    response = requests.post(
        OLLAMA_URL,
        json = {
            "model" : MODEL_NAME,
            "prompt" : prompt,
            "stream" : False
        }
    )

    data = response.json()
    return data["response"]
