@echo off

REM Activate the virtual environment
call env\Scripts\activate

REM Run tests
pytest -vvv -s tests/

REM Generate test coverage report
pytest --cov --cov-report html

REM Open coverage report in default browser
start htmlcov\index.html
