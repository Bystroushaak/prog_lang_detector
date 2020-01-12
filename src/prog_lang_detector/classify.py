#! /usr/bin/env python3
import sys
import json
import os.path
import argparse
from markov import compare_models
from markov import train_char_model
from functools import lru_cache


MODELS_PATH = os.path.join(os.path.dirname(__file__), "models")


@lru_cache()
def read_models(models_root):
    models = []
    for fn in os.listdir(models_root):
        path = os.path.join(models_root, fn)
        if not os.path.isfile(path) or not fn.endswith(".json"):
            continue

        with open(path) as f:
            model = json.load(f)

        model_name = str(fn).rsplit(".", 1)[0]

        models.append((model_name, model))

    return models


def classify(what, models_root=MODELS_PATH, print_details=True):
    classified_model = train_char_model(what, 4)

    results = []
    for model_name, model in read_models(models_root):
        result = compare_models(classified_model, model, 1)

        if print_details:
            print(model_name, result)

        results.append([result, model_name])

    return max(results)[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print details."
    )
    parser.add_argument(
        "-m",
        "--models",
        default=MODELS_PATH,
        help="Path to the directory with models. Default %(default)s."
    )
    parser.add_argument(
        "filename"
    )
    args = parser.parse_args()

    if args.filename == "-":
        what = sys.stdin.read()
    elif os.path.isfile(args.filename):
        with open(args.filename) as f:
            what = f.read()
    else:
        sys.stderr.write("`%s` not found.\n" % args.filename)
        sys.exit(1)

    print(classify(what, args.models, args.verbose))


if __name__ == '__main__':
    main()
