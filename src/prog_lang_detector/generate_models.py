#! /usr/bin/env python3
import argparse
import os
import os.path
import json

from markov import train_char_model


def generate_models(datasets_root, models_root):
    for fn in os.listdir(datasets_root):
        path = os.path.join(datasets_root, fn)

        if not os.path.isfile(path):
            continue

        print("Generating models for %s.." % fn)
        with open(path, "rb") as f:
            data = f.read().decode("utf-8", "ignore")

        model = train_char_model(data, 4)

        model_name = str(fn).rsplit(".", 1)[0] + ".json"
        with open(os.path.join(models_root, model_name), "w") as f:
            f.write(json.dumps(model))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--datasets",
        default=os.path.join(os.path.dirname(__file__), "datasets"),
        help="Path to the directory with datasets. Default %(default)s."
    )
    parser.add_argument(
        "-m",
        "--models",
        default=os.path.join(os.path.dirname(__file__), "models"),
        help="Path to the directory with models. Default %(default)s."
    )
    args = parser.parse_args()

    generate_models(args.datasets, args.models)


if __name__ == '__main__':
    main()
