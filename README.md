# prog_lang_detector

Experimental detector of programming languages based on simple Markov chain models.

It seems to be working just fine, but this was just a project for one afternoon, so I wouldn't use it anywhere where it actually matters.

## Usage

### generate_models.py

This generates markov models and stores them as JSON for later.

If you want to add new language just add file with examples to the `datasets/` directory. Then run this script and your language will be available for classification.

### classify.py

    $ ./classify.py generate_models.py 
    python

Use `-v` for verbose output:

    $ ./classify.py -v generate_models.py
    java -1.1340277863553143
    cpp -0.3374316948487715
    c -1.4215450489996726
    tinySelf -9.214666771760813
    python 0.6627492013338969
    python

# Licence

MIT
