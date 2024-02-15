import datasets
import re
import random
import json



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
        num = random.random()
        print(doc["answer"].split(' ')[-1].replace(',', ''))
        if num > 0.5:
            answer1 = int(doc["answer"].split(' ')[-1].replace(',', ''))
            answer2 = random_excluding_A(answer1)
        else:
            answer2 = int(doc["answer"].split(' ')[-1].replace(',', ''))
            answer1 = random_excluding_A(answer2)
        out_doc = {
            "few_shot": few_shot,
            "question": doc["question"],
            "answer1": answer1,
            "answer2": answer2,
            "answer": doc["answer"],
        }
        return out_doc

    return dataset.map(_process_doc)

d_7b = {}
for line in open('/bask/projects/j/jlxi8926-auto-sum/dongwei/lm-evaluation-harness/output/meta-llama/Llama-2-7b-chat-hf_gsm8k/gsm8k_7b_evaluative.jsonl'):
    temp = json.loads(line.strip())
    if temp['answer'] not in d_7b:
        d_7b[temp['answer']] = temp

def process_docs_7b(dataset: datasets.Dataset) -> datasets.Dataset:
    def _process_doc(doc):
        out_doc = {
            "question": doc["question"],
            "answer1": d_7b[doc["answer"]]["answer1"],
            "answer2": d_7b[doc["answer"]]["answer2"],
            "answer": doc["answer"],
            "answer1_correct": d_7b[doc["answer"]]["answer1_correct"],
            "answer2_correct": d_7b[doc["answer"]]["answer2_correct"],
        }
        return out_doc

    return dataset.map(_process_doc)

d_7b_no_chat = {}
for line in open('/bask/projects/j/jlxi8926-auto-sum/dongwei/lm-evaluation-harness/output/meta-llama/Llama-2-7b-hf_gsm8k/gsm8k_7b_evaluative.jsonl'):
    temp = json.loads(line.strip())
    if temp['answer'] not in d_7b_no_chat:
        d_7b_no_chat[temp['answer']] = temp

def process_docs_7b_no_chat(dataset: datasets.Dataset) -> datasets.Dataset:
    def _process_doc(doc):
        out_doc = {
            "question": doc["question"],
            "answer1": d_7b_no_chat[doc["answer"]]["answer1"],
            "answer2": d_7b_no_chat[doc["answer"]]["answer2"],
            "answer": doc["answer"],
            "answer1_correct": d_7b_no_chat[doc["answer"]]["answer1_correct"],
            "answer2_correct": d_7b_no_chat[doc["answer"]]["answer2_correct"],
        }
        return out_doc

    return dataset.map(_process_doc)

d_7b_no_chat_four_options = {}
for line in open('/bask/projects/j/jlxi8926-auto-sum/dongwei/lm-evaluation-harness/output/meta-llama/Llama-2-7b-hf_gsm8k/gsm8k_7b_evaluative_four_options.jsonl'):
    temp = json.loads(line.strip())
    if temp['answer'] not in d_7b_no_chat_four_options:
        d_7b_no_chat_four_options[temp['answer']] = temp

def process_docs_7b_no_chat_four_options(dataset: datasets.Dataset) -> datasets.Dataset:
    def _process_doc(doc):
        out_doc = {
            "question": doc["question"],
            "answer1": d_7b_no_chat_four_options[doc["answer"]]["answer1"],
            "answer2": d_7b_no_chat_four_options[doc["answer"]]["answer2"],
            "answer3": d_7b_no_chat_four_options[doc["answer"]]["answer3"],
            "answer4": d_7b_no_chat_four_options[doc["answer"]]["answer4"],
            "answer": doc["answer"],
            "answer1_correct": d_7b_no_chat_four_options[doc["answer"]]["answer1_correct"],
            "answer2_correct": d_7b_no_chat_four_options[doc["answer"]]["answer2_correct"],
            "answer3_correct": d_7b_no_chat_four_options[doc["answer"]]["answer3_correct"],
            "answer4_correct": d_7b_no_chat_four_options[doc["answer"]]["answer4_correct"],
        }
        return out_doc

    return dataset.map(_process_doc)

d_13b = {}
for line in open('/bask/projects/j/jlxi8926-auto-sum/dongwei/lm-evaluation-harness/output/meta-llama/Llama-2-13b-chat-hf_gsm8k/gsm8k_13b_evaluative.jsonl'):
    temp = json.loads(line.strip())
    if temp['answer'] not in d_13b:
        d_13b[temp['answer']] = temp

def process_docs_13b(dataset: datasets.Dataset) -> datasets.Dataset:
    def _process_doc(doc):
        out_doc = {
            "question": doc["question"],
            "answer1": d_13b[doc["answer"]]["answer1"],
            "answer2": d_13b[doc["answer"]]["answer2"],
            "answer": doc["answer"],
            "answer1_correct": d_13b[doc["answer"]]["answer1_correct"],
            "answer2_correct": d_13b[doc["answer"]]["answer2_correct"],
        }
        return out_doc

    return dataset.map(_process_doc)

d_13b_no_chat = {}
for line in open('/bask/projects/j/jlxi8926-auto-sum/dongwei/lm-evaluation-harness/output/meta-llama/Llama-2-13b-hf_gsm8k/gsm8k_7b_evaluative.jsonl'):
    temp = json.loads(line.strip())
    if temp['answer'] not in d_13b_no_chat:
        d_13b_no_chat[temp['answer']] = temp

def process_docs_13b_no_chat(dataset: datasets.Dataset) -> datasets.Dataset:
    def _process_doc(doc):
        out_doc = {
            "question": doc["question"],
            "answer1": d_13b_no_chat[doc["answer"]]["answer1"],
            "answer2": d_13b_no_chat[doc["answer"]]["answer2"],
            "answer": doc["answer"],
            "answer1_correct": d_13b_no_chat[doc["answer"]]["answer1_correct"],
            "answer2_correct": d_13b_no_chat[doc["answer"]]["answer2_correct"],
        }
        return out_doc

    return dataset.map(_process_doc)

d_70b = {}
for line in open('/bask/projects/j/jlxi8926-auto-sum/dongwei/lm-evaluation-harness/output/meta-llama/Llama-2-70b-chat-hf_gsm8k/gsm8k_70b_evaluative.jsonl'):
    temp = json.loads(line.strip())
    if temp['answer'] not in d_70b:
        d_70b[temp['answer']] = temp

def process_docs_70b(dataset: datasets.Dataset) -> datasets.Dataset:
    def _process_doc(doc):
        out_doc = {
            "question": doc["question"],
            "answer1": d_70b[doc["answer"]]["answer1"],
            "answer2": d_70b[doc["answer"]]["answer2"],
            "answer": doc["answer"],
            "answer1_correct": d_70b[doc["answer"]]["answer1_correct"],
            "answer2_correct": d_70b[doc["answer"]]["answer2_correct"],
        }
        return out_doc

    return dataset.map(_process_doc)

d_70b_no_chat = {}
for line in open('/bask/projects/j/jlxi8926-auto-sum/dongwei/lm-evaluation-harness/output/meta-llama/Llama-2-70b-hf_gsm8k/gsm8k_13b_evaluative.jsonl'):
    temp = json.loads(line.strip())
    if temp['answer'] not in d_70b_no_chat:
        d_70b_no_chat[temp['answer']] = temp

def process_docs_70b_no_chat(dataset: datasets.Dataset) -> datasets.Dataset:
    def _process_doc(doc):
        out_doc = {
            "question": doc["question"],
            "answer1": d_70b_no_chat[doc["answer"]]["answer1"],
            "answer2": d_70b_no_chat[doc["answer"]]["answer2"],
            "answer": doc["answer"],
            "answer1_correct": d_70b_no_chat[doc["answer"]]["answer1_correct"],
            "answer2_correct": d_70b_no_chat[doc["answer"]]["answer2_correct"],
        }
        return out_doc

    return dataset.map(_process_doc)

d_mix = {}
for line in open('/bask/projects/j/jlxi8926-auto-sum/dongwei/lm-evaluation-harness/output/mistralai/Mixtral-8x7B-Instruct-v0.1_gsm8k/gsm8k_mix_evaluative.jsonl'):
    temp = json.loads(line.strip())
    if temp['answer'] not in d_mix:
        d_mix[temp['answer']] = temp

def process_docs_mix(dataset: datasets.Dataset) -> datasets.Dataset:
    def _process_doc(doc):
        out_doc = {
            "question": doc["question"],
            "answer1": d_mix[doc["answer"]]["answer1"],
            "answer2": d_mix[doc["answer"]]["answer2"],
            "answer": doc["answer"],
            "answer1_correct": d_mix[doc["answer"]]["answer1_correct"],
            "answer2_correct": d_mix[doc["answer"]]["answer2_correct"],
        }
        return out_doc

    return dataset.map(_process_doc)

d_flan_t5_xxl = {}
for line in open('/bask/projects/j/jlxi8926-auto-sum/dongwei/lm-evaluation-harness/output/google/flan-t5-xxl_gsm8k/gsm8k_7b_evaluative.jsonl'):
    temp = json.loads(line.strip())
    if temp['answer'] not in d_flan_t5_xxl:
        d_flan_t5_xxl[temp['answer']] = temp

def process_docs_flan_t5_xxl(dataset: datasets.Dataset) -> datasets.Dataset:
    def _process_doc(doc):
        out_doc = {
            "question": doc["question"],
            "answer1": d_flan_t5_xxl[doc["answer"]]["answer1"],
            "answer2": d_flan_t5_xxl[doc["answer"]]["answer2"],
            "answer": doc["answer"],
            "answer1_correct": d_flan_t5_xxl[doc["answer"]]["answer1_correct"],
            "answer2_correct": d_flan_t5_xxl[doc["answer"]]["answer2_correct"],
        }
        return out_doc

    return dataset.map(_process_doc)

d_gpt_3_5 = {}
for line in open('/bask/projects/j/jlxi8926-auto-sum/dongwei/lm-evaluation-harness/output/gpt-3.5/gpt-3.5_gsm8k/gsm8k_gpt-3.5_evaluative.jsonl'):
    temp = json.loads(line.strip())
    if temp['answer'] not in d_gpt_3_5:
        d_gpt_3_5[temp['answer']] = temp

def process_docs_gpt_3(dataset: datasets.Dataset) -> datasets.Dataset:
    def _process_doc(doc):
        out_doc = {
            "question": doc["question"],
            "answer1": d_gpt_3_5[doc["answer"]]["answer1"],
            "answer2": d_gpt_3_5[doc["answer"]]["answer2"],
            "answer": doc["answer"],
            "answer1_correct": d_gpt_3_5[doc["answer"]]["answer1_correct"],
            "answer2_correct": d_gpt_3_5[doc["answer"]]["answer2_correct"],
        }
        return out_doc

    return dataset.map(_process_doc)
