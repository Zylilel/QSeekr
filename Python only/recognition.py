from PIL import Image
import pytesseract
import os
import json
from rapidfuzz import fuzz
import webbrowser

max_ratio = 0
max_ratio_data = None
max_ratio_qs_path = None
max_ratio_ms_path = None
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.chdir(r"C:\Users\Asus\Desktop\QSeekr")

data = pytesseract.image_to_string(Image.open(r"C:\Users\Asus\Desktop\QSeekr\Screenshot 2025-11-09 150758.png"))
print(data)


with open("Computer Science (9618).json", "r") as file:
    database = json.load(file)
    qs_data = database["questions"]
    for f in range(len(qs_data)):
        qs_text = qs_data[f]["question_text"]
        match_ratio = fuzz.partial_ratio(data, qs_text)
        if match_ratio > max_ratio:
            max_ratio = match_ratio
            max_ratio_data = qs_data[f]
    max_ratio_qs_path = max_ratio_data["question_images"]
    max_ratio_ms_path = max_ratio_data["markscheme_images"]

print(max_ratio)
print(max_ratio_data["paper_code"])
for s in range(len(max_ratio_qs_path)):
    full_path = os.path.join(r"C:\Users\Asus\Desktop\QSeekr", max_ratio_qs_path[s])
    os.startfile(full_path)

full_ms_path = os.path.join(r"C:\Users\Asus\Desktop\QSeekr", max_ratio_ms_path[0])
os.startfile(full_ms_path)
        
