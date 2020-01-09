#! /usr/bin/env python3
import sys
import json
from random import random
from collections import Counter
from collections import defaultdict


def normalize(counter):
    s = float(sum(counter.values()))

    return [
        (char, cnt/s)
        for char, cnt in counter.items()
    ]


def train_char_model(data, order=4):
    raw_model = defaultdict(Counter)

    pad = "~" * order
    data = pad + data
    for i in range(len(data) - order):
        char = data[i+order]
        history = data[i:i+order]

        raw_model[history][char] += 1

    return {
        hist: normalize(chars)
        for hist, chars in raw_model.items()
    }


def generate_letter(model, history, order):
    history = history[-order:]
    dist = model[history]

    x = random()
    for char, prob in dist:
        x = x - prob
        if x <= 0:
            return char


def generate_text(model, order, nletters=1000):
    history = "~" * order

    out = []
    for i in range(nletters):
        c = generate_letter(model, history, order)
        history = history[-order:] + c
        out.append(c)

    return "".join(out)


def compare_models(classified, lang_model):
    score = 0
    matches = 0

    for substr, probabilities in classified.items():
        lang_model_probabilities = lang_model.get(substr)

        if lang_model_probabilities is None:
            continue

        matches += 1

        lang_model_prob_dict = dict(lang_model_probabilities)

        for char, prob in probabilities:
            lang_model_prob = lang_model_prob_dict.get(char, 0)

            if lang_model_prob != 0:
                if lang_model_prob > prob:
                    score += 1.0 - abs(lang_model_prob - prob)
                else:
                    score += 1.0 - abs(prob - lang_model_prob)
            else:
                score -= 1  # penalty for not found, helps to create bigger difference

    return matches, score / matches


if __name__ == '__main__':
    order = 4
    # c_model = train_char_model(open("c_dataset.txt").read(), order)
    # with open("c_model.json", "w") as f:
    #     f.write(json.dumps(c_model))

    # py_model = train_char_model(open("py_dataset.txt").read(), order)
    # with open("py_model.json", "w") as f:
    #     f.write(json.dumps(py_model))
    
    with open("c_model.json") as f:
        c_model = json.loads(f.read())

    with open("py_model.json") as f:
        py_model = json.loads(f.read())


    data = """for(i = 0; i < 10; i++) {"""


    # to_classify = train_char_model(open(__file__).read(), order)
    to_classify = train_char_model(data, order)

    print("py_model", compare_models(to_classify, py_model))
    print("c_model", compare_models(to_classify, c_model))


    # print(generate_text(py_model, order, nletters=2000))
    # print(to_classify)