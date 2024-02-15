import datasets
import re
import random


def process_docs(dataset: datasets.Dataset) -> datasets.Dataset:
    def _process_doc(doc):
        num = random.random()
        num2 = random.random()
        sample_list = [0, 1, 2, 3]
        doc["label"] = int(doc["answer"])
        sample_list.remove(int(doc["label"]))
        chosen_item = random.choice(sample_list)
        # sample_list.remove(chosen_item)
        # chosen_item2 = random.choice(sample_list)
        if num < 0.5:
            gold = 0
            answer1 = doc["choices"][int(doc["label"])]
            answer2 = doc["choices"][chosen_item]
            # answer3 = doc["choices"][chosen_item2]
        elif num > 0.5:
            gold = 1
            answer1 = doc["choices"][chosen_item]
            answer2 = doc["choices"][int(doc["label"])]
            # answer3 = doc["choices"][chosen_item2]
        out_doc = {
            "query": doc["question"],
            "answer1": answer1,
            "answer2": answer2,
            "choices": ["0", "1"],
            "gold": gold,
        }
        return out_doc

    return dataset.map(_process_doc)
