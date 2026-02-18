import re
import json
import ollama


MODEL_NAME = "qwen2.5:14b"



def safe_json_load(raw: str):

    raw = re.sub(r"^```.*?\n|```$", "", raw, flags=re.DOTALL).strip()

    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in LLM output")

    json_str = match.group(0)

    json_str = json_str.encode("utf-8", "backslashreplace").decode("utf-8")

    return json.loads(json_str)



def generate_summary(text):

    prompt = f"""
You are an elite academic research analyst.

Return ONLY valid JSON.

STRUCTURE:

1. ### Abstract – Core Idea
2. ### Historical Context & Background
3. ### Core Contributions
4. ### Methodology
5. ### Key Results
6. ### Limitations & Future Work

JSON SCHEMA:
{{
  "summary": "string",
  "key_concepts": ["5-10 technical terms"],
  "flashcards": [
    {{ "question": "Why ...?", "answer": "..." }},
    {{ "question": "How ...?", "answer": "..." }}
  ]
}}

Analyze:
{text}
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    raw = response["message"]["content"].strip()

    try:
        return safe_json_load(raw)

    except Exception as e:
        print("Summary JSON parsing failed:")
        print(raw)
        print("ERROR:", e)

        return {
            "summary": raw,
            "key_concepts": [],
            "flashcards": []
        }


def generate_chunk_summary(text):

    prompt = f"""
Return ONLY valid JSON:

{{ "summary": "string" }}

Inside summary:
- Use bullet points starting with '-'
- Bold metrics using **

Analyze:
{text}
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    raw = response["message"]["content"].strip()

    try:
        return safe_json_load(raw)

    except Exception as e:
        print("Chunk JSON parsing failed:")
        print(raw)
        print("ERROR:", e)

        return {"summary": raw}
