import fitz
import os


def extract_image(path):
    doc = fitz.open(path)

    os.makedirs("app/static/images", exist_ok=True)

    output_data =[]

    for page_index in range(len(doc)):

        page = doc[page_index]
        images = page.get_images(full=True)

        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]


            filename = f"image_{page_index}_{img_index}.{image_ext}"
            filepath = f"app/static/images/{filename}"

            with open(filepath, "wb") as f:
                f.write(image_bytes)

            output_data.append({
                "image_url": f"/static/images/{filename}",
                "caption": f"Image from page {page_index + 1}"
            })
    return output_data
