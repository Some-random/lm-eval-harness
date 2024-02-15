import jsonlines
import sys
import json

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
    target = obj['target']
    filtered_resps = obj['filtered_resps'][0].replace('</s>', '')
    if filtered_resps in target:
        exact_match += 1

print('Exact match percentage: ' + str(round(float(exact_match) / real_total * 100, 2))) 
