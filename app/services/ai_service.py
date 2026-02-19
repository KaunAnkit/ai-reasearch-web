import os
import re
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"





def safe_json_load(raw: str):
    

    
    raw = re.sub(r"^```.*?\n|```$", "", raw, flags=re.DOTALL).strip()

    
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in LLM output")

    json_str = match.group(0)

    
    json_str = json_str.encode("utf-8", "backslashreplace").decode("utf-8")

    return json.loads(json_str)




def generate_summary(text):

    fallback_data = {
        "abstract": "Failed to parse summary.",
        "background": "N/A",
        "contributions": "N/A",
        "methodology": "N/A",
        "key_results": "N/A",
        "limitations_future_work": "N/A",
        "key_concepts": [],
        "flashcards": []
    }

    prompt = f"""
You are an elite academic research analyst.
Your task is to extract the intellectual structure of this research paper into a structured JSON format.

STRICT RULES:
- Return ONLY valid JSON.
- Do NOT include markdown code blocks (no ```json).
- Double-escape all backslashes for JSON compatibility (e.g., \\n or \\section).
- Use **bolding** for important metrics or values within the strings.

JSON SCHEMA:
{{
  "abstract": "The central thesis, problem addressed, and main result.",
  "background": "Prior work and what was previously missing.",
  "contributions": "New theories, models, or methods introduced.",
  "methodology": "Detailed research approach, data, and architecture.",
  "key_results": "Important numbers and improvements (e.g., **95% accuracy**).",
  "limitations_future_work": "Weaknesses and open problems.",
  "key_concepts": ["List of 5-10 technical terms"],
  "flashcards": [
    {{ "question": "string", "answer": "string" }}
  ]
}}

Analyze the following paper text:
{text}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )

    raw = response.choices[0].message.content.strip()

    try:
        return safe_json_load(raw)

    except Exception as e:
        print("Summary JSON parsing failed:")
        print(raw)
        print("ERROR:", e)

        return fallback_data


def generate_chunk_summary(text):

    prompt =   f"""
You are an academic research assistant.

STRICT RULES:
- Return ONLY valid JSON.
- Do NOT include markdown code blocks.
- Do NOT include markdown code blocks (no ```json).
- Double-escape all backslashes for JSON compatibility (e.g., \\n or \\section).
- Output must follow this schema exactly:
- Max 4 bullet points
- Each bullet ≤ 15 words

{{ "summary": "string" }}

Inside the summary:
- Use bullet points starting with '-'
- Bold metrics, percentages, and tool names using **
- Dense, factual, technical

Analyze:
Text:
{text}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    raw = response.choices[0].message.content.strip()

    try:
        return safe_json_load(raw)

    except Exception as e:
        print(" Chunk JSON parsing nahi ho pa raha")
        print(raw)
        print("ERROR:", e)

        return {"summary": raw}
