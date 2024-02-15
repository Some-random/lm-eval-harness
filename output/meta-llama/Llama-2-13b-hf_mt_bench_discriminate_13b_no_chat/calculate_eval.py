import sys
import json
import random

f = sys.argv[1]
line = open(f).read().strip()
d = json.loads(line)
correct, invalid, total = 0, 0, 0
is_2 = 0

for obj in d:
    total += 1
    obj["filtered_resps"] = obj["filtered_resps"][0].strip().replace('</s>', '')
    if str(obj["filtered_resps"]) not in ["1", "2"]:
        print(str(obj["filtered_resps"]))
        invalid += 1
        correct += min(obj["doc"]["answer1_score"], obj["doc"]["answer2_score"])
        # if random.random() < 0.5
        # correct += obj["doc"]["answer1_score"]
        # else:
        #     correct += obj["doc"]["answer2_score"]
    elif str(obj["filtered_resps"]) == "1":
        correct += obj["doc"]["answer1_score"]
    elif str(obj["filtered_resps"]) == "2":
        correct += obj["doc"]["answer2_score"]
    if int(obj["doc"]["choice"]) == 2:
        is_2 += 1

print(round(float(correct) / total, 2), round(float(invalid) * 100 / total, 2))
print(is_2, total)
