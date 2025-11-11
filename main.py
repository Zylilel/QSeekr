from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import json
import io
from PIL import Image
import pytesseract
from rapidfuzz import fuzz
from typing import List, Dict


app = FastAPI()

def load_database():
    with open("database/all_database.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    questions = []
    for i in range(1, len(data), 2):
        if isinstance(data[i], dict) and "questions" in data[i]:
            questions.extend(data[i]["questions"])
    return questions

database = load_database()

origin = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8000/docs",
    "http://localhost:8000/"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.chdir(r"C:\Users\Asus\Desktop\QSeekr")

@app.get("/", response_class=HTMLResponse)
async def home():
    with open("index.html", "r") as f:
        return f.read()

@app.get("/script.js")
async def get_script():
    return FileResponse("script.js")

@app.get("/style.css")
async def get_style():
    return FileResponse("style.css")

def search_questions(query: str, top_n: int = 10) -> List[Dict]:
    """
    Search questions using fuzzy matching
    Returns top_n most similar questions
    """
    results = []

    for question in database:
        question_text = question.get("question_text", "")
        if question_text:
            score = fuzz.partial_ratio(query.lower(), question_text.lower())

            results.append({
                "score": score,
                "id": question.get("id"),
                "subject": question.get("subject"),
                "topic": question.get("topic"),
                "paper_code": question.get("paper_code"),
                "question_number": question.get("question_number"),
                "question_text": question_text,
                "question_images": question.get("question_images", []),
                "markscheme_images": question.get("markscheme_images", [])
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_n]

@app.post("/search")
async def search_question(query: str = Form(None), file: UploadFile = File(None)):
    if file and file.filename:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        query = pytesseract.image_to_string(image)

    if not query:
        return {"query": "No input provided", "results": []}

    print(f"Searching for: {query}")
    print(f"Query length: {len(query)} characters")

    results = search_questions(query, top_n=10)

    print(f"Found {len(results)} results")
    if results:
        print(f"Top result score: {results[0]['score']}")

    return {
        "query": query,
        "results": results
    }


