#!/bin/bash
virtualenv .env -p python3
. .env/bin/activate && pip install django
. .env/bin/activate && pip install djangorestframework
. .env/bin/activate && pip install selenium==3.141.0
. .env/bin/activate && pip install PyYAML==5.1.1
