import sys
import json

f = sys.argv[1]
the_same, correct, invalid, total = 0, 0, 0, 0

for line in open(f).readlines():
    obj = json.loads(line.strip())
    total += 1
    answer1_correct = int(obj["answer1_correct"])
    answer2_correct = int(obj["answer2_correct"])
    print(answer1_correct, answer2_correct)
    obj["filtered_resps"] = obj["discriminate_answer"]
    try:
        obj["filtered_resps"] = obj["filtered_resps"].strip().split("### ")[1]
        if str(obj["filtered_resps"]) not in ["1", "2"]:
            print(str(obj["filtered_resps"]))
            invalid += 1
        elif str(obj["filtered_resps"]) == "1":
            correct += answer1_correct
        elif str(obj["filtered_resps"]) == "2":
            correct += answer2_correct
        if answer1_correct and answer2_correct:
            the_same += 1
        elif not answer1_correct and not answer2_correct:
            the_same += 1
    except:
        invalid += 1

print(round(float(correct) * 100 / total, 2), round(float(invalid) * 100 / total, 2))
print(the_same, total)
