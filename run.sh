#!/usr/bin/env bash
pipenv run python backend/manage.py makemigrations
pipenv run python backend/manage.py migrate
pipenv run python backend/manage.py runserver
