import datasets
import re
import random
import json

file_path = "/bask/projects/j/jlxi8926-auto-sum/dongwei/lm-evaluation-harness/lm_eval/tasks/triviaqa_discriminate/pretrained__meta-llama__Llama-2-7b-hf,tensor_parallel_size__1,dtype__auto_triviaqa.jsonl"
with open(file_path, 'r') as file:
    data = file.read()
json_data = json.loads(data)
answers_list = []
for item in json_data:
    answers_list.append(item["doc"]["answer"]["aliases"])


def random_excluding_A(A):
    # Check if A is a positive integer
    if A > 0 and isinstance(A, int):
        while True:
            num = random.randint(0, 2 * A)
            if num != A:
                return num
    # Check if A is a negative integer
    elif A < 0 and isinstance(A, int):
        while True:
            num = random.randint(2 * A, 0)
            if num != A:
                return num
    elif A == 0:
        return 1
    # Check if A is a floating-point number
    elif isinstance(A, float):
        while True:
            if A > 0:
                num = random.uniform(0, 2 * A)
            else:
                num = random.uniform(2 * A, 0)
            if num != A:
                return num

def process_docs(dataset: datasets.Dataset) -> datasets.Dataset:
    def _process_doc(doc):
        answers = doc["answer"]["aliases"]
        num = random.random()
        if num > 0.5:
            answer1 = answers
            answer2 = random.choice(answers_list)
        else:
            answer1 = random.choice(answers_list)
            answer2 = answers
        out_doc = {
            "question": doc["question"],
            "answer1": answer1,
            "answer2": answer2,
            "answer": doc["answer"],
        }
        return out_doc

    return dataset.map(_process_doc)

def flatten_dict_to_string(d):
    return ', '.join(f"{key}={value}" for key, value in d.items())

d_7b = {}
for line in open('/bask/projects/j/jlxi8926-auto-sum/dongwei/lm-evaluation-harness/output/meta-llama/Llama-2-7b-chat-hf_triviaqa/triviaqa_7b_evaluative.jsonl'):
    temp = json.loads(line.strip())
    if temp['question'] not in d_7b:
        d_7b[temp['question']] = temp

def process_docs_7b(dataset: datasets.Dataset) -> datasets.Dataset:
    def _process_doc(doc):
        try:
            out_doc = {
                "question": doc["question"],
                "answer1": (d_7b[doc["question"]])["answer1"],
                "answer2": (d_7b[doc["question"]])["answer2"],
                "answer": doc["answer"],
                "answer1_correct": (d_7b[doc["question"]])["answer1_correct"],
                "answer2_correct": (d_7b[doc["question"]])["answer2_correct"],
            }
            return out_doc
        except:
            return None

    return dataset.map(_process_doc).filter(lambda x: x is not None)

d_7b_bad = {}
for line in open('/bask/projects/j/jlxi8926-auto-sum/dongwei/lm-evaluation-harness/output/meta-llama/Llama-2-7b-chat-hf_triviaqa_bad/triviaqa_7b_evaluative_bad.jsonl'):
    temp = json.loads(line.strip())
    if temp['question'] not in d_7b_bad:
        d_7b_bad[temp['question']] = temp

d_7b_no_chat = {}
for line in open('/bask/projects/j/jlxi8926-auto-sum/dongwei/lm-evaluation-harness/output/meta-llama/Llama-2-7b-hf_triviaqa/triviaqa_7b_evaluative.jsonl'):
    temp = json.loads(line.strip())
    if temp['question'] not in d_7b_no_chat:
        d_7b_no_chat[temp['question']] = temp

def process_docs_7b_no_chat(dataset: datasets.Dataset) -> datasets.Dataset:
    def _process_doc(doc):
        try:
            out_doc = {
                "question": doc["question"],
                "answer1": (d_7b_no_chat[doc["question"]])["answer1"],
                "answer2": (d_7b_no_chat[doc["question"]])["answer2"],
                "answer": doc["answer"],
                "answer1_correct": (d_7b_no_chat[doc["question"]])["answer1_correct"],
                "answer2_correct": (d_7b_no_chat[doc["question"]])["answer2_correct"],
            }
            return out_doc
        except:
            return None

    return dataset.map(_process_doc).filter(lambda x: x is not None)

d_7b_bad = {}
for line in open('/bask/projects/j/jlxi8926-auto-sum/dongwei/lm-evaluation-harness/output/meta-llama/Llama-2-7b-chat-hf_triviaqa_bad/triviaqa_7b_evaluative_bad.jsonl'):
    temp = json.loads(line.strip())
    if temp['question'] not in d_7b_bad:
        d_7b_bad[temp['question']] = temp

def process_docs_7b_bad(dataset: datasets.Dataset) -> datasets.Dataset:
    def _process_doc(doc):
        try:
            out_doc = {
                "question": doc["question"],
                "answer1": (d_7b_bad[doc["question"]])["answer1"],
                "answer2": (d_7b_bad[doc["question"]])["answer2"],
                "answer": doc["answer"],
                "answer1_correct": (d_7b_bad[doc["question"]])["answer1_correct"],
                "answer2_correct": (d_7b_bad[doc["question"]])["answer2_correct"],
            }
            return out_doc
        except:
            return None

    return dataset.map(_process_doc).filter(lambda x: x is not None)


d_13b = {}
for line in open('/bask/projects/j/jlxi8926-auto-sum/dongwei/lm-evaluation-harness/output/meta-llama/Llama-2-13b-chat-hf_triviaqa/triviaqa_13b_evaluative.jsonl'):
    temp = json.loads(line.strip())
    if temp['question'] not in d_13b:
        d_13b[temp['question']] = temp

def process_docs_13b(dataset: datasets.Dataset) -> datasets.Dataset:
    def _process_doc(doc):
        try:
            out_doc = {
                "question": doc["question"],
                "answer1": (d_13b[doc["question"]])["answer1"],
                "answer2": (d_13b[doc["question"]])["answer2"],
                "answer": doc["answer"],
                "answer1_correct": (d_13b[doc["question"]])["answer1_correct"],
                "answer2_correct": (d_13b[doc["question"]])["answer2_correct"],
            }
            return out_doc
        except:
            return None

    return dataset.map(_process_doc).filter(lambda x: x is not None)

d_13b_no_chat = {}
for line in open('/bask/projects/j/jlxi8926-auto-sum/dongwei/lm-evaluation-harness/output/meta-llama/Llama-2-13b-hf_triviaqa/triviaqa_7b_evaluative.jsonl'):
    temp = json.loads(line.strip())
    if temp['question'] not in d_13b_no_chat:
        d_13b_no_chat[temp['question']] = temp

def process_docs_13b_no_chat(dataset: datasets.Dataset) -> datasets.Dataset:
    def _process_doc(doc):
        try:
            out_doc = {
                "question": doc["question"],
                "answer1": (d_13b_no_chat[doc["question"]])["answer1"],
                "answer2": (d_13b_no_chat[doc["question"]])["answer2"],
                "answer": doc["answer"],
                "answer1_correct": (d_13b_no_chat[doc["question"]])["answer1_correct"],
                "answer2_correct": (d_13b_no_chat[doc["question"]])["answer2_correct"],
            }
            return out_doc
        except:
            return None

    return dataset.map(_process_doc).filter(lambda x: x is not None)

d_13b_bad = {}
for line in open('/bask/projects/j/jlxi8926-auto-sum/dongwei/lm-evaluation-harness/output/meta-llama/Llama-2-13b-chat-hf_triviaqa_bad/triviaqa_13b_evaluative_bad.jsonl'):
    temp = json.loads(line.strip())
    if temp['question'] not in d_13b_bad:
        d_13b_bad[temp['question']] = temp

def process_docs_13b_bad(dataset: datasets.Dataset) -> datasets.Dataset:
    def _process_doc(doc):
        try:
            out_doc = {
                "question": doc["question"],
                "answer1": (d_13b_bad[doc["question"]])["answer1"],
                "answer2": (d_13b_bad[doc["question"]])["answer2"],
                "answer": doc["answer"],
                "answer1_correct": (d_13b_bad[doc["question"]])["answer1_correct"],
                "answer2_correct": (d_13b_bad[doc["question"]])["answer2_correct"],
            }
            return out_doc
        except:
            return None

    return dataset.map(_process_doc).filter(lambda x: x is not None)

d_70b = {}
for line in open('/bask/projects/j/jlxi8926-auto-sum/dongwei/lm-evaluation-harness/output/meta-llama/Llama-2-70b-chat-hf_triviaqa/triviaqa_70b_evaluative.jsonl'):
    temp = json.loads(line.strip())
    if temp['question'] not in d_70b:
        d_70b[temp['question']] = temp

def process_docs_70b(dataset: datasets.Dataset) -> datasets.Dataset:
    def _process_doc(doc):
        try:
            out_doc = {
                "question": doc["question"],
                "answer1": (d_70b[doc["question"]])["answer1"],
                "answer2": (d_70b[doc["question"]])["answer2"],
                "answer": doc["answer"],
                "answer1_correct": (d_70b[doc["question"]])["answer1_correct"],
                "answer2_correct": (d_70b[doc["question"]])["answer2_correct"],
            }
            return out_doc
        except:
            return None

    return dataset.map(_process_doc).filter(lambda x: x is not None)

d_70b_no_chat = {}
for line in open('/bask/projects/j/jlxi8926-auto-sum/dongwei/lm-evaluation-harness/output/meta-llama/Llama-2-70b-hf_triviaqa/triviaqa_7b_evaluative.jsonl'):
    temp = json.loads(line.strip())
    if temp['question'] not in d_70b_no_chat:
        d_70b_no_chat[temp['question']] = temp

def process_docs_70b_no_chat(dataset: datasets.Dataset) -> datasets.Dataset:
    def _process_doc(doc):
        try:
            out_doc = {
                "question": doc["question"],
                "answer1": (d_70b_no_chat[doc["question"]])["answer1"],
                "answer2": (d_70b_no_chat[doc["question"]])["answer2"],
                "answer": doc["answer"],
                "answer1_correct": (d_70b_no_chat[doc["question"]])["answer1_correct"],
                "answer2_correct": (d_70b_no_chat[doc["question"]])["answer2_correct"],
            }
            return out_doc
        except:
            return None

    return dataset.map(_process_doc).filter(lambda x: x is not None)

d_70b_bad = {}
for line in open('/bask/projects/j/jlxi8926-auto-sum/dongwei/lm-evaluation-harness/output/meta-llama/Llama-2-70b-chat-hf_triviaqa_bad/triviaqa_70b_evaluative_bad.jsonl'):
    temp = json.loads(line.strip())
    if temp['question'] not in d_70b_bad:
        d_70b_bad[temp['question']] = temp

def process_docs_70b_bad(dataset: datasets.Dataset) -> datasets.Dataset:
    def _process_doc(doc):
        try:
            out_doc = {
                "question": doc["question"],
                "answer1": (d_70b_bad[doc["question"]])["answer1"],
                "answer2": (d_70b_bad[doc["question"]])["answer2"],
                "answer": doc["answer"],
                "answer1_correct": (d_70b_bad[doc["question"]])["answer1_correct"],
                "answer2_correct": (d_70b_bad[doc["question"]])["answer2_correct"],
            }
            return out_doc
        except:
            return None

    return dataset.map(_process_doc).filter(lambda x: x is not None)

d_mix = {}
for line in open('/bask/projects/j/jlxi8926-auto-sum/dongwei/lm-evaluation-harness/output/mistralai/Mixtral-8x7B-Instruct-v0.1_triviaqa/triviaqa_mix_evaluative.jsonl'):
    temp = json.loads(line.strip())
    if temp['question'] not in d_mix:
        d_mix[temp['question']] = temp

def process_docs_mix(dataset: datasets.Dataset) -> datasets.Dataset:
    def _process_doc(doc):
        try:
            out_doc = {
                "question": doc["question"],
                "answer1": (d_mix[doc["question"]])["answer1"],
                "answer2": (d_mix[doc["question"]])["answer2"],
                "answer": doc["answer"],
                "answer1_correct": (d_mix[doc["question"]])["answer1_correct"],
                "answer2_correct": (d_mix[doc["question"]])["answer2_correct"],
            }
            return out_doc
        except:
            return None

    return dataset.map(_process_doc).filter(lambda x: x is not None)

d_flan = {}
for line in open('/bask/projects/j/jlxi8926-auto-sum/dongwei/lm-evaluation-harness/output/google/flan-t5-xxl_triviaqa/triviaqa_7b_evaluative.jsonl'):
    temp = json.loads(line.strip())
    if temp['question'] not in d_flan:
        d_flan[temp['question']] = temp

def process_docs_flan_t5_xxl(dataset: datasets.Dataset) -> datasets.Dataset:
    def _process_doc(doc):
        try:
            out_doc = {
                "question": doc["question"],
                "answer1": (d_flan[doc["question"]])["answer1"],
                "answer2": (d_flan[doc["question"]])["answer2"],
                "answer": doc["answer"],
                "answer1_correct": (d_flan[doc["question"]])["answer1_correct"],
                "answer2_correct": (d_flan[doc["question"]])["answer2_correct"],
            }
            return out_doc
        except:
            return None

    return dataset.map(_process_doc).filter(lambda x: x is not None)

d_mix_bad = {}
for line in open('/bask/projects/j/jlxi8926-auto-sum/dongwei/lm-evaluation-harness/output/mistralai/Mixtral-8x7B-Instruct-v0.1_triviaqa_bad/triviaqa_mix_evaluative_bad.jsonl'):
    temp = json.loads(line.strip())
    if temp['question'] not in d_mix_bad:
        d_mix_bad[temp['question']] = temp

def process_docs_mix_bad(dataset: datasets.Dataset) -> datasets.Dataset:
    def _process_doc(doc):
        try:
            out_doc = {
                "question": doc["question"],
                "answer1": (d_mix_bad[doc["question"]])["answer1"],
                "answer2": (d_mix_bad[doc["question"]])["answer2"],
                "answer": doc["answer"],
                "answer1_correct": (d_mix_bad[doc["question"]])["answer1_correct"],
                "answer2_correct": (d_mix_bad[doc["question"]])["answer2_correct"],
            }
            return out_doc
        except:
            return None

    return dataset.map(_process_doc).filter(lambda x: x is not None)

d_13b_gt_and_random = {}
for line in open('/bask/projects/j/jlxi8926-auto-sum/dongwei/lm-evaluation-harness/output/meta-llama/Llama-2-13b-chat-hf_triviaqa_gt_and_random/triviaqa_13b_evaluative_gt_and_random.jsonl'):
    temp = json.loads(line.strip())
    if temp['question'] not in d_13b_gt_and_random:
        d_13b_gt_and_random[temp['question']] = temp

def process_docs_13b_gt_and_random(dataset: datasets.Dataset) -> datasets.Dataset:
    def _process_doc(doc):
        try:
            out_doc = {
                "question": doc["question"],
                "answer1": (d_13b_gt_and_random[doc["question"]])["answer1"],
                "answer2": (d_13b_gt_and_random[doc["question"]])["answer2"],
                "answer": doc["answer"],
                "answer1_correct": (d_13b_gt_and_random[doc["question"]])["answer1_correct"],
                "answer2_correct": (d_13b_gt_and_random[doc["question"]])["answer2_correct"],
            }
            return out_doc
        except:
            return None

    return dataset.map(_process_doc).filter(lambda x: x is not None)
