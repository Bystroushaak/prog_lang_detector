#! /usr/bin/env python3
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

    print("done")


if __name__ == '__main__':
    generate_models("datasets", "models")