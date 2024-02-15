import sys
import json

f = sys.argv[1]
line = open(f).read().strip()
d = json.loads(line)
correct, invalid, total = 0, 0, 0
write_file = open("triviaqa_discriminate_7b_finetune.jsonl", 'w')

for obj in d:
    answer1_correct = int(obj["doc"]["answer1_correct"])
    answer2_correct = int(obj["doc"]["answer2_correct"])
    if (answer1_correct and answer2_correct) or (not answer1_correct and not answer2_correct):
        question = obj["doc"]["question"]
        answer1 = obj["doc"]["answer1"]
        answer2 = obj["doc"]["answer2"]
        if answer1_correct:
            final_answer = '1'
        else:
            final_answer = '2'
        final_string = "[INST]Question: " + question + "\nHere are the two lists of answer choices.\nAnswer1: " + str(answer1) + '\nAnswer2:' + str(answer2) + "\nAnswer:[/INST]" + final_answer + '\n'
        write_file.write(json.dumps({"text": final_string}) + '\n')

