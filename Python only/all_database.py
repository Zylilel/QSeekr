import os
import json
all_question = []

path = os.listdir(r"C:\Users\Asus\Desktop\QSeekr\database")
os.chdir(r"C:\Users\Asus\Desktop\QSeekr\database")

for i in range(len(path)):
    with open(path[i], "r") as file:
        data = json.load(file)
        all_question.append(path[i])
        all_question.append(data)
os.chdir(r"C:\Users\Asus\Desktop\QSeekr")
with open("all_database.json", "w") as file:
    json.dump(all_question, file, indent=2)

        