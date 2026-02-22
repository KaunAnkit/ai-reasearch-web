import fitz
import os

def extract_image(path):
    doc = fitz.open(path)
    os.makedirs("app/static/images", exist_ok=True)
    output_data = []

    for page_index in range(len(doc)):
        page = doc[page_index]
        
        
        paths = page.get_drawings()
        
       
        if paths:
            
            page_rect = fitz.EMPTY_RECT()
            for p in paths:
                page_rect |= p["rect"]
            
            
            if page_rect.width > 100 and page_rect.height > 100:
                
                page_rect = page_rect + (-20, -20, 20, 20)
                
                
                page_rect &= page.rect 

                
                pix = page.get_pixmap(clip=page_rect, matrix=fitz.Matrix(2, 2))
                
                filename = f"page_{page_index}_drawing.png"
                filepath = f"app/static/images/{filename}"
                pix.save(filepath)
                
                output_data.append({
                    "image_url": f"/static/images/{filename}",
                    "caption": f"Diagram from page {page_index + 1}"
                })

        
        image_info = page.get_image_info()
        for i, img in enumerate(image_info):
            rect = fitz.Rect(img["bbox"])
            if rect.width < 50 or rect.height < 50: continue 
            
            pix = page.get_pixmap(clip=rect, matrix=fitz.Matrix(2, 2))
            filename = f"page_{page_index}_img_{i}.png"
            pix.save(f"app/static/images/{filename}")
            
            output_data.append({
                "image_url": f"/static/images/{filename}",
                "caption": f"Figure from page {page_index + 1}"
            })

    return output_data