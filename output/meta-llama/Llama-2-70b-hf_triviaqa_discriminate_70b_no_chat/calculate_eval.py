import sys
import json

f = sys.argv[1]
line = open(f).read().strip()
d = json.loads(line)
correct, invalid, total = 0, 0, 0

for obj in d:
    total += 1
    answer1_correct = int(obj["doc"]["answer1_correct"])
    answer2_correct = int(obj["doc"]["answer2_correct"])
    print(answer1_correct, answer2_correct)
    obj["filtered_resps"] = obj["filtered_resps"][0].strip().replace('</s>', '').replace('[/INST]', '')
    if str(obj["filtered_resps"]) not in ["1", "2"]:
        print(str(obj["filtered_resps"]))
        invalid += 1
    elif str(obj["filtered_resps"]) == "1":
        correct += answer1_correct
    elif str(obj["filtered_resps"]) == "2":
        correct += answer2_correct
print(total)
print(round(float(correct) * 100 / total, 2), round(float(invalid) * 100 / total, 2))
