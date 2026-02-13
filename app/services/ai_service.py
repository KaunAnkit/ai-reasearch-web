import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL_NAME = "openai/gpt-oss-20b"


def generate_summary(text):

    prompt = f"""
You are an academic research assistant.

Your task is to analyze the provided research paper text and return structured output.

IMPORTANT RULES:
- Return ONLY valid JSON.
- Do NOT include markdown.
- Do NOT include explanations.
- Do NOT include text before or after the JSON.
- The response must be a single valid JSON object.
- Do not use trailing commas.
- All keys must match exactly as shown.
- Always include exactly 5 flashcards.

JSON SCHEMA:

{{
  "summary": "string",
  "key_concepts": ["string", "string"],
  "flashcards": [
    {{
      "question": "string",
      "answer": "string"
    }}
  ]
}}

REQUIREMENTS:
- "summary" must be concise (5–8 sentences).
- "key_concepts" must contain 5–10 important technical concepts.
- "flashcards" must contain exactly 5 question-answer pairs.
- Questions must test understanding, not definitions only.
- Answers must be clear and concise.

Now analyze the following text:

{text}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
    )

    raw = response.choices[0].message.content
    raw = raw.strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1].strip()

    return json.loads(raw)

# agar text ka length 6000> tabhi ye function bulaynge 
# and i am thinking to segrigate these funtion probably in diffrent files 
# text har 6000 text pe chunk break karega
# to hume sarre chunks ki summary collect karni hai and then un summary ko summarise karna hai 

def generate_chunk_summary(text):

    prompt = f"""
You are an academic research assistant.

Your task is to analyze the provided research paper text chunk and return structured output 
accoring to the chunk content.

IMPORTANT RULES:
- Return ONLY valid JSON.
- Do NOT include markdown.
- Do NOT include explanations.
- Do NOT include text before or after the JSON.
- The response must be a single valid JSON object.
- Do not use trailing commas.


JSON SCHEMA:

{{
  "summary": "string"
}}

REQUIREMENTS:
- "summary" must be concise and to the point (6-10 sentences).
- You are a strict JSON generator. You only output valid JSON.

Now analyze the following text:

{text}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
    )

    raw = response.choices[0].message.content
    raw = raw.strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1].strip()

    return json.loads(raw)
        



    





        