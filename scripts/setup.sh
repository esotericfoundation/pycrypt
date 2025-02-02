#!/bin/bash
# Sets this project up to be run.

python3 -m venv ./venv
source ./venv/bin/activate

pip install -r ./requirements.txt
