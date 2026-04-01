#!/bin/bash

export PORT=5000
unset PIP_USER

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python main.py