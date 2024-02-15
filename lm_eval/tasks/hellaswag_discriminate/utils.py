import datasets
import re
import random


def preprocess(text):
    text = text.strip()
    # NOTE: Brackets are artifacts of the WikiHow dataset portion of HellaSwag.
    text = text.replace(" [title]", ". ")
    text = re.sub("\\[.*?\\]", "", text)
    text = text.replace("  ", " ")
    return text


def process_docs(dataset: datasets.Dataset) -> datasets.Dataset:
    def _process_doc(doc):
        num = random.random()
        num2 = random.random()
        sample_list = [0, 1, 2, 3]
        sample_list.remove(int(doc["label"]))
        chosen_item = random.choice(sample_list)
        ctx = doc["ctx_a"] + " " + doc["ctx_b"].capitalize()
        out_doc = {
            "query": preprocess(doc["activity_label"] + ": " + ctx),
            "answer1": preprocess(doc["endings"][int(doc["label"])]) if num > 0.5 else preprocess(doc["endings"][chosen_item]),
            "answer2": preprocess(doc["endings"][chosen_item]) if num > 0.5 else preprocess(doc["endings"][int(doc["label"])]),
            "choices": ["0", "1"],
            "gold": 0 if num > 0.5 else 1,
        }
        return out_doc

    return dataset.map(_process_doc)
