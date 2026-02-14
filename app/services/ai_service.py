import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL_NAME = "openai/gpt-oss-20b"


def generate_summary(text):

    prompt = f"""
You are an academic research assistant. Your task is to provide a high-density, structured analysis of the research paper.

OUTPUT FORMATTING RULES:
- The "summary" value must be formatted with Markdown for readability.
- Use '###' for headers and '**' for bolding key terms.
- Organize the "summary" string into these 4 sections: 
  1. ### The Research Gap (What was missing?)
  2. ### Methodology & Approach (How was it solved?)
  3. ### Key Findings & Data (What were the results?)
  4. ### Critical Limitations (What are the weaknesses?)

JSON SCHEMA RULES:
- Return ONLY valid JSON. 
- Do NOT include markdown code blocks (```json) in the raw output.
- The "summary" must be one single string containing the headers mentioned above.
- "key_concepts": 5-10 technical terms.
- "flashcards": 5 pairs testing "Why" and "How".

JSON SCHEMA:
{{
  "summary": "### **The Research Gap**\\n...\\n### **Methodology & Approach**\\n...",
  "key_concepts": ["string"],
  "flashcards": [{{ "question": "string", "answer": "string" }}]
}}

Now analyze the following text:
{text}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
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
You are an academic research assistant. Extract the technical essence of this section.

RULES:
- Return ONLY a JSON object: {{ "summary": "string" }}
- Inside the "summary" string, use **bolding** for any specific metrics, percentages, or tool names.
- Use a bulleted format (starting with "-") within the string to separate different points found in this chunk.
- The content must be dense and factual (6-10 sentences equivalent).

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
        



    





        