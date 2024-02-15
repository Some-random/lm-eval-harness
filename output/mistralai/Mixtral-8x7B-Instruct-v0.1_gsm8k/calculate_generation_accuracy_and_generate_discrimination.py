import jsonlines
import random
import sys
import json
import re

patterns_to_ignore = r",|\$|(?s).*####"

write_file = open('gsm8k_13b_evaluative.jsonl', 'w')

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
    correct_answer, incorrect_answer, candidate_answer, is_correct = None, None, None, True
    for i in range(len(obj["resps"][0])):
        answer = obj["resps"][0][i].strip()
        try:
            # new_answer = float(answer.replace('</s>', '').split('#### ')[1])
            # answer = answer.replace('</s>', '').split('#### ')[1]
            answer = re.sub(patterns_to_ignore, "", answer)
            answer = answer.replace('</s>', '').strip()
            temp_answer = float(answer)
            if answer == gt_answer:
                correct_list[i] += 1
                correct_answer = answer
            else:
                if incorrect_answer is None:
                    incorrect_answer = answer
            if answer != gt_answer and answer != incorrect_answer:
                candidate_answer = answer
        except:
            invalid_list[i] += 1
    if correct_answer is None:
        correct_answer = candidate_answer
        is_correct = False
    
    new_d = {}
    new_d['question'] = obj['doc']['question']
    new_d['answer'] = obj['doc']['answer']
    num = random.random()
    if num > 0.5:
        new_d['answer1'] = correct_answer
        new_d['answer1_correct'] = is_correct
        new_d['answer2'] = incorrect_answer
        new_d['answer2_correct'] = False
    else:
        new_d['answer1'] = incorrect_answer
        new_d['answer1_correct'] = False
        new_d['answer2'] = correct_answer
        new_d['answer2_correct'] = is_correct

    new_d['doc_id'] = obj['doc_id']
    write_file.write(json.dumps(new_d) + '\n')

print([item / total for item in correct_list], [item / total for item in invalid_list])
print("Avg accuracy: " + str(round(100 * sum(correct_list) / total / len(correct_list), 2)))
print("Avg invalid: " + str(round(100 * sum(invalid_list) / total / len(invalid_list), 2)))
