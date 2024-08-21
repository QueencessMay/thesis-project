#!/usr/bin/env bash

python3 -m pip install -r requirements.txt

python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

python3 manage.py collectstatic --noinput