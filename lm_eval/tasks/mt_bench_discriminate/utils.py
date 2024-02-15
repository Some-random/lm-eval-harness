import datasets
import re
import random
import json


def process_docs(dataset: datasets.Dataset) -> datasets.Dataset:
    def _process_doc(doc):
        num = random.random()
        try:
            if num > 0.5:
                answer1 = doc["max_value"]
                answer2 = doc["min_value"]
                answer1_score = doc["max_score"]
                answer2_score = doc["min_score"]
                choice = 1
            else:
                answer1 = doc["min_value"]
                answer2 = doc["max_value"]
                answer1_score = doc["min_score"]
                answer2_score = doc["max_score"]
                choice = 2
            
            out_doc = {
                "answer1": answer1,
                "answer2": answer2,
                "answer1_score": answer1_score,
                "answer2_score": answer2_score,
                "choice": choice
            }
            return out_doc
        except:
            return None


    return dataset.map(_process_doc)

