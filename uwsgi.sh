#!/bin/sh

pipenv run uwsgi --ini uwsgi.ini --home $(pipenv --venv)
