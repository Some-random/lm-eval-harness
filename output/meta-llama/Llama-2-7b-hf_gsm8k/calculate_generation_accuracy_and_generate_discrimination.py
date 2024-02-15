import jsonlines
import random
import sys
import json
import re

patterns_to_ignore = r",|\$|(?s).*####"

write_file = open('gsm8k_7b_evaluative.jsonl', 'w')

total = 0
exact_match = 0
invalid = 0
real_total = 0
in_answer = 0

j = sys.argv[1]
line = open(j).read().strip()
correct_list = [0.0, 0.0, 0.0, 0.0]
invalid_list = [0.0, 0.0, 0.0, 0.0]

d = json.loads(line)
for obj in d:
    total += 1
    gt_answer = str(obj["target"].strip().split('#### ')[1].strip())
    # print('gt: ' + gt_answer)
    new_d = {}
    new_d['question'] = obj['doc']['question']
    new_d['answer'] = obj['doc']['answer']
    for i in range(len(obj["resps"][0])):
        answer = obj["resps"][0][i].strip()
        try:
            answer = re.sub(patterns_to_ignore, "", answer)
            answer = answer.replace('</s>', '').replace('</SYS>', '').strip()
            if answer == gt_answer:
                correct_list[i] += 1
                is_correct = True
            else:
                is_correct = False
        except:
            invalid_list[i] += 1
            print(answer)
            answer = None
            is_correct = False
        
        s = "answer" + str(i + 1)
        new_d[s] = answer
        new_d[s + "_correct"] = is_correct

    new_d['doc_id'] = obj['doc_id']
    write_file.write(json.dumps(new_d) + '\n')

print([item / total for item in correct_list], [item / total for item in invalid_list])
print("Avg accuracy: " + str(round(100 * sum(correct_list) / total / len(correct_list), 2)))
print("Avg invalid: " + str(round(100 * sum(invalid_list) / total / len(invalid_list), 2)))
