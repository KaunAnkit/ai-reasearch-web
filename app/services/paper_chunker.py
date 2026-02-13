def para_text_chunker(text):

    chunk = []

    stop_chunk = text.split("\n\n")
    empty_string = ""
        
    for x in stop_chunk:

        if len(empty_string) + len(x) <= 6000:
            empty_string += x + "\n\n"
        
        else:
    
            if empty_string:
                chunk.append(empty_string.strip())
            empty_string = x + "\n\n"


    if empty_string:
        chunk.append(empty_string.strip())
    return chunk