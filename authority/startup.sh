#!/bin/bash

python manage.py makemigrations api
python manage.py migrate
python manage.py populate_database
python manage.py create_admin
python manage.py tests
python manage.py runserver