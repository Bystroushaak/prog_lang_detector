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
    for _ in range(nletters):
        c = generate_letter(model, history, order)
        history = history[-order:] + c
        out.append(c)

    return "".join(out)



def compare_models(classified, lang_model, penalty=0):
    score = 0
    matches = 0

    for substr, probabilities in classified.items():
        lang_model_probabilities = lang_model.get(substr)

        if lang_model_probabilities is None:
            score -= penalty
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
                score -= penalty

    return score / matches
