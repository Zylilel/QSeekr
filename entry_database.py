import json
import os
from collections import defaultdict

question_path = r"C:\Users\Asus\Desktop\QSeekr\A-LEVEL\Biology (9700)\questions\BIODIVERSITY, CLASSIFICATION AND CONSERVATION\2009\Summer\Paper 2\9700_21_MJ_09"
qs_section = question_path.split("\\")
subject = qs_section[6]
topic = qs_section[8]
paper_code = qs_section[12]

answer_path = r"C:\Users\Asus\Desktop\QSeekr\A-LEVEL\Biology (9700)\answers\BIODIVERSITY, CLASSIFICATION AND CONSERVATION\2009\Summer\Paper 2\9700_21_MJ_09"

all_question = os.listdir(question_path)
grouped_questions = defaultdict(list)
for img in all_question:
    question_num = img.split('_')[0]
    grouped_questions[question_num].append(img)
grouped_questions = dict(grouped_questions)

all_answer = os.listdir(answer_path)
grouped_answers = defaultdict(list)
for img in all_answer:
    question_num = img.split('_')[0]
    grouped_answers[question_num].append(img)

for question_num in grouped_questions.keys():
    question_imgs = grouped_questions[question_num]
    answer_imgs = grouped_answers.get(question_num, [])

questions_list = []

question_img_paths = [os.path.join(question_path, img) for img in question_imgs]
answer_img_paths = [os.path.join(answer_path, img) for img in answer_imgs]

entry = {
        "id": f"{paper_code}_{question_num}",
        "subject": subject,
        "topic": topic,
        "paper_code": paper_code,
        "question_number": question_num,
        "marks": None,
        "question_text": "",
        "question_images": question_img_paths,
        "markscheme_images": answer_img_paths
    }
questions_list.append(entry)

with open(f"{subject}.json", "w") as f:
    json.dump({"questions": questions_list}, f, indent=2)