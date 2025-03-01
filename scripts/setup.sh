#!/bin/bash
# Sets this project up to be run.

cd "$(dirname "$0")/.." || exit

python3 -m venv ./venv
source ./venv/bin/activate

pip install -r ./requirements.txt
