
import requests


from app.services.pdf_service import extract_column # pdf se text nikalata hai  1
from app.services.ai_service import generate_summary # final summary banayega 4


from app.services.ai_service import generate_chunk_summary # chunks ki summary banayega 3
from app.services.paper_chunker import para_text_chunker # bade text ka chunk bana ke bhejta hai 2


def output(path):

    text = extract_column(path)

    chunk_list = para_text_chunker(text)

    

    all_summaries = []

    for x in chunk_list:

        y = generate_chunk_summary(x)["summary"]

        all_summaries.append(y)

    final_text = "\n\n".join(all_summaries)

    return generate_summary(final_text)

    
# print(output("cnn.pdf"))

















