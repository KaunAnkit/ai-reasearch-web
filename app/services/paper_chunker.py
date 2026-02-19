def para_text_chunker(text, max_chars=600):

    chunks = []

    
    paragraphs = text.split("\n\n")

    for para in paragraphs:

        
        if len(para) <= max_chars:
            chunks.append(para.strip())

        else:
            
            for i in range(0, len(para), max_chars):
                chunks.append(para[i:i+max_chars].strip())

    return chunks
