@echo off

REM Stop on first error
setlocal enabledelayedexpansion
set "ERR_FLAG=0"

REM Delete older .pyc files (optional)
REM This is commented out because it's not as straightforward to implement in a batch file,
REM but it can be replaced with a script if needed.
REM find . -type d \( -name env -o -name venv  \) -prune -false -o -name "*.pyc" -exec rm -rf {} \;

REM Run required migrations
set FLASK_APP=core\server.py

REM Uncomment these if you need to initialize or migrate
REM flask db init -d core\migrations\
REM flask db migrate -m "Initial migration." -d core\migrations\
REM flask db upgrade -d core\migrations\

REM Run server
REM Gunicorn is not natively supported on Windows. Instead, use Waitress.
REM Install Waitress with: pip install waitress
REM Modify the command to use Waitress as follows:

waitress-serve --host=0.0.0.0 --port=8000 core.server:app
