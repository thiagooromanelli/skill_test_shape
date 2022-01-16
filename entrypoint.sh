#!/usr/bin/env bash
python -m flask db init
python -m flask db migrate
python -m flask db upgrade
python -m flask run