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
    obj["filtered_resps"] = obj["filtered_resps"][0]
    if str(obj["filtered_resps"]) not in ["1", "2"]:
        print(str(obj["resps"][0]))
        invalid += 1
        correct += min(answer1_correct, answer2_correct)
        continue
    elif str(obj["filtered_resps"]) == "1":
        correct += answer1_correct
    elif str(obj["filtered_resps"]) == "2":
        correct += answer2_correct
    if obj["doc"]["answer1_correct"] or obj["doc"]["answer2_correct"]:
        upper += 1
    if obj["doc"]["answer1_correct"] and obj["doc"]["answer2_correct"]:
        lower += 1

print("Total number of items: " + str(total))
print("Total correct percentage: " + str(round(float(correct) * 100 / total, 1)))
print("Total invalid percentage: " + str(round(float(invalid) * 100 / total, 1)))
print("Upper bound: " + str(round(float(upper) * 100 / total, 1)))


