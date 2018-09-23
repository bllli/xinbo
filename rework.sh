#!/usr/bin/env bash

rm db.sqlite3
rm */migrations/0*.py

python manage.py makemigrations
python manage.py migrate
