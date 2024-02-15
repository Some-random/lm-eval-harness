import json
import random
import sys

the_same, correct, invalid, total = 0, 0, 0, 0
upper, lower, rand = 0, 0, 0
for line in open(sys.argv[1]):
    total += 1
    d = json.loads(line.strip())
    try:
        answer_choice = d["discriminate_answer"].split('### ')[1]
    except:
        invalid += 1
        print(d["discriminate_answer"])
        correct += min(int(d['answer1_correct']), int(d['answer2_correct']))
        continue
    if answer_choice not in ['1', '2']:
        invalid += 1
        correct += min(int(d['answer1_correct']), int(d['answer2_correct']))
        print(d["discriminate_answer"])
        continue
    elif answer_choice == '1' and d['answer1_correct']:
        correct += 1
    elif answer_choice == '2' and d['answer2_correct']:
        correct += 1
    if d['answer1_correct'] or d['answer2_correct']:
        upper += 1

print("Total correct: " + str(round(float(correct / total * 100), 2)) + ' Total invalid: ' + str(round(float(invalid / total * 100), 2)) + ' Total random: ' +  str(round(float(rand) / total * 100, 2)) + ' Upper limit: ' + str(round(float(upper) / total * 100, 2)) + ' Lower limit: ' + str(round(float(lower) / total * 100, 2)))
print(total, the_same)
print(round(float(upper) * 100 / total, 2), round(float(lower) * 100 / total, 2), round(float(rand) * 100 / total, 2))
