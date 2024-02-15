import jsonlines
import sys
import json

total = 0
exact_match = 0
invalid = 0
real_total = 0
in_answer = 0

j = sys.argv[1]
line = open(j).read().strip()
# line =  open('pretrained__meta-llama__Llama-2-7b-chat-hf_gsm8k_discriminate.jsonl').read().strip()
d = json.loads(line)
for obj in d:
    real_total += 1
    # print(obj["filtered_resps"][0])
    if "invalid" not in obj["filtered_resps"][0]:
        exact_match += obj["exact_match"]
        total += 1
        if obj["filtered_resps"][0] in [str(obj['doc']['answer1']), str(obj['doc']['answer2'])]:
            in_answer += 1
    else:
        invalid += 1

print('Exact match percentage: ' + str(round(float(exact_match) / total * 100, 2))) 
print('Invalid percentage: ' + str(round(float(invalid) / real_total * 100, 2))) 
print('In answer percentage: ' + str(round(float(in_answer) / real_total * 100, 2)))
