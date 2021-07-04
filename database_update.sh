#!/bin/sh
. env/bin/activate
python3 src/manage.py makemigrations
python3 src/manage.py migrate
deactivate