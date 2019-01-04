#!/bin/bash

export FLASK_DEBUG=1 #auto relaod modification
export FLASK_ENV=development #dev mode traceback

export FLASK_APP=weblabel.py

flask run --host=0.0.0.0
