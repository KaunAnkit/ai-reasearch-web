
import requests
import time
import asyncio

from app.services.pdf_service import extract_column # pdf se text nikalata hai  1
from app.services.ai_service import generate_summary # final summary banayega 4


from app.services.ai_service import generate_chunk_summary # chunks ki summary banayega 3
from app.services.paper_chunker import para_text_chunker # bade text ka chunk bana ke bhejta hai 2


from app.services.extract_image import extract_image #images extract karta hai 


sem = asyncio.Semaphore(3)

async def async_chunk_summary(chunk):
    async with sem:
        res = await generate_chunk_summary(chunk)
        y = res["summary"]
        return "\n".join(y) if isinstance(y , list) else y


async def output(path):
    
    text = extract_column(path)

    chunk_list = para_text_chunker(text)

    all_summaries = await asyncio.gather(*[async_chunk_summary(c) for c in chunk_list])


    final_text = "n\n".join(all_summaries)

    data_dic_task = generate_summary(final_text)

    image_task = asyncio.to_thread(extract_image, path)

    data_dic, images = await asyncio.gather(data_dic_task, image_task)

    data_dic["images"] = images

    return data_dic


# def output(path):

#     text = extract_column(path)

#     chunk_list = para_text_chunker(text)

#     all_summaries = []

#     for x in chunk_list:

#         y = generate_chunk_summary(x)["summary"]

#         if isinstance(y, list):
#             y = "\n".join(y)

#         all_summaries.append(y)

#         time.sleep(1)

#     chunked_summaries = chunk_chunker(all_summaries)



#     #function 

#     final_text = "\n\n".join(chunked_summaries)

#     if len(final_text) > 3000:
#         final_text = generate_chunk_summary(final_text)["summary"]
#         time.sleep(6)

#     data_dic = generate_summary(final_text)


#     images = extract_image(path)
#     data_dic["images"] = images



#     return data_dic

    
# # print(output("cnn.pdf"))


# def chunk_chunker(data,batch_size = 10):

#     if len(data)<= batch_size:
#         return data
    
#     new_chunk = []

#     for x in range(0,len(data),batch_size):

#         batch = "\n\n".join(data[x:x+batch_size])

#         compressed = generate_chunk_summary(batch)["summary"]

#         new_chunk.append(compressed)

#         time.sleep(10)

#     return chunk_chunker(new_chunk,batch_size)
    














