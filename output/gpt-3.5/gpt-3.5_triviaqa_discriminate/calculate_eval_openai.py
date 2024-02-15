import json
import sys

correct, invalid, total = 0, 0, 0
for line in open(sys.argv[1]):
    total += 1
    d = json.loads(line.strip())
    try:
        answer_choice = d["discriminate_answer"].strip()
    except:
        invalid += 1
        print(d["discriminate_answer"])
        continue
    if answer_choice not in ['1', '2']:
        invalid += 1
        print(d["discriminate_answer"])
    elif answer_choice == '1' and d['answer1_correct']:
        correct += 1
    elif answer_choice == '2' and d['answer2_correct']:
        correct += 1

print("Total correct: " + str(round(float(correct / total * 100), 2)) + ' Total invalid: ' + str(round(float(invalid / total * 100), 2)))
print(total, correct, invalid)
