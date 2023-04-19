@echo off
set FLASK_APP=api.index
set FLASK_ENV=development
python -m flask --app=app run