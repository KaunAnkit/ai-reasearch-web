
import requests


from services.pdf_service import extract_column
from services.ai_service import generate_summary

text = extract_column("cnn.pdf")[:6000]
summary = generate_summary(text)


print(summary)
