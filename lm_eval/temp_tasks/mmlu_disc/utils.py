import datasets
import re
import random


def process_docs(dataset: datasets.Dataset) -> datasets.Dataset:
    def _process_doc(doc):
        num = random.random()
        num2 = random.random()
        sample_list = [0, 1, 2, 3]
        doc["label"] = ord(doc["answer"]) - ord("A")
        sample_list.remove(int(doc["label"]))
        chosen_item = random.choice(sample_list)
        out_doc = {
            "query": doc["question"],
            "answer1": doc["choices"][int(doc["label"])] if num > 0.5 else doc["choices"][chosen_item],
            "answer2": doc["choices"][chosen_item] if num > 0.5 else doc["choices"][int(doc["label"])],
            "choices": ["0", "1"],
            "gold": 0 if num > 0.5 else 1,
        }
        return out_doc

    return dataset.map(_process_doc)
