#!/bin/bash

pip install -r /www/requirements.txt

python -m flask run --host=0.0.0.0
