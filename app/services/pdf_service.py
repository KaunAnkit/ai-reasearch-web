import pymupdf


def extract_column(path):
    doc = pymupdf.open(path)

    full_text = []

    for page in doc:
        
        blocks = page.get_text("dict")["blocks"]


        blocks.sort(key=lambda b: (b["bbox"][1],b["bbox"][0]))

        for b in blocks:

            if b["type"] == 0:
                block_text = ""
                
                for line in b["lines"]:
                    for span in line["spans"]:

                        if span["size"] > 8.5:

                            block_text += span["text"] + " "

                
                if block_text.strip():
                    full_text.append(block_text.strip())
    
    doc.close()

    text = "\n".join(full_text)

    return text





# print(extract_column("../cnn.pdf"))
