from PIL import Image
import pytesseract
import os
import json
from concurrent.futures import ThreadPoolExecutor

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.chdir(r"C:\Users\Asus\Desktop\QSeekr\database")
database = os.listdir(r"C:\Users\Asus\Desktop\QSeekr\database")

def ocr_image(img_path):
    if not img_path.lower().endswith(('.webp', '.png', '.jpg', '.jpeg')):
        return ""
    return pytesseract.image_to_string(Image.open(img_path))

for f in range(len(database)):
    print(f"\n[{f+1}/{len(database)}] Processing {database[f]}...")
    with open(database[f], "r") as file:
        data = json.load(file)
        qs_list = data["questions"]
        
        for s in range(len(qs_list)):
            if s % 10 == 0:
                print(f"  Question {s}/{len(qs_list)}", end='\r')
            qs_data = qs_list[s]
            qs_img = qs_data["question_images"]
            
            with ThreadPoolExecutor(max_workers=4) as executor:
                results = list(executor.map(ocr_image, qs_img))
            
            qs_data["question_text"] = " ".join(results)
    
    with open(database[f], "w") as file:
        json.dump(data, file, indent=2)
    print(f"\n  ✓ Saved {database[f]}")