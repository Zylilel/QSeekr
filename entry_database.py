import json
import os
from collections import defaultdict

base_path = r"C:\Users\Asus\Desktop\QSeekr\A-LEVEL\Sociology (9699)"
questions_base = os.path.join(base_path, "questions")
answers_base = os.path.join(base_path, "answers")

questions_list = []

for topic in os.listdir(questions_base):
    topic_path = os.path.join(questions_base, topic)
    if not os.path.isdir(topic_path):
        continue
    
    for year in os.listdir(topic_path):
        year_path = os.path.join(topic_path, year)
        if not os.path.isdir(year_path):
            continue
        
        for season in os.listdir(year_path):
            season_path = os.path.join(year_path, season)
            if not os.path.isdir(season_path):
                continue
            
            for paper in os.listdir(season_path):
                paper_path = os.path.join(season_path, paper)
                if not os.path.isdir(paper_path):
                    continue
                
                for paper_code in os.listdir(paper_path):
                    question_path = os.path.join(paper_path, paper_code)
                    answer_path = os.path.join(answers_base, topic, year, season, paper, paper_code)
                    
                    if not os.path.isdir(question_path):
                        continue
                    
                    all_question = os.listdir(question_path)
                    grouped_questions = defaultdict(list)
                    for img in all_question:
                        question_num = img.split('_')[0]
                        grouped_questions[question_num].append(img)
                    
                    grouped_answers = defaultdict(list)
                    if os.path.exists(answer_path):
                        all_answer = os.listdir(answer_path)
                        for img in all_answer:
                            question_num = img.split('_')[0]
                            grouped_answers[question_num].append(img)
                    
                    for question_num in grouped_questions.keys():
                        question_imgs = grouped_questions[question_num]
                        answer_imgs = grouped_answers.get(question_num, [])
                        
                        question_img_paths = [os.path.join(question_path, img) for img in question_imgs]
                        answer_img_paths = [os.path.join(answer_path, img) for img in answer_imgs]
                        
                        entry = {
                            "id": f"{paper_code}_{question_num}",
                            "subject": "Sociology (9699)",
                            "topic": topic,
                            "paper_code": paper_code,
                            "question_number": question_num,
                            "marks": None,
                            "question_text": "",
                            "question_images": question_img_paths,
                            "markscheme_images": answer_img_paths
                        }
                        
                        questions_list.append(entry)

with open("Sociology (9699).json", "w") as f:
    json.dump({"questions": questions_list}, f, indent=2)

print(f"Created {len(questions_list)} question entries")
