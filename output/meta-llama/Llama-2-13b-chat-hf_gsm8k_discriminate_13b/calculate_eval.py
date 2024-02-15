import sys
import json
import random

f = sys.argv[1]
line = open(f).read().strip()
d = json.loads(line)
correct, invalid, total, upper, rand, lower = 0, 0, 0, 0, 0, 0

for obj in d:
    total += 1
    answer1_correct = int(obj["doc"]["answer1_correct"])
    answer2_correct = int(obj["doc"]["answer2_correct"])
    print(answer1_correct, answer2_correct)
    obj["filtered_resps"] = obj["filtered_resps"][0]
    if str(obj["filtered_resps"]) not in ["1", "2"]:
        print(str(obj["filtered_resps"]))
        invalid += 1
    elif str(obj["filtered_resps"]) == "1":
        correct += answer1_correct
    elif str(obj["filtered_resps"]) == "2":
        correct += answer2_correct
    if obj["doc"]["answer1_correct"] or obj["doc"]["answer2_correct"]:
        upper += 1
    elif not obj["doc"]["answer1_correct"] and not obj["doc"]["answer1_correct"]:
        lower += 1
    r = random.random()
    if r < 0.5:
        rand += answer1_correct
    else:
        rand += answer2_correct


print(round(float(correct) * 100 / total, 2), round(float(invalid) * 100 / total, 2))
print(round(float(upper) * 100 / total, 2), round(float(lower) * 100 / total, 2), round(float(rand) * 100 / total, 2))
