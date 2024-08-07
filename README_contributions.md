# Project Objectives

This document outlines the objectives assigned to me for the project.

1. Increase statement coverage during testing.
2. Implement missing functionalities as per the problem outline.
3. Enhance existing routes and functionalities as required.
4. Ensure comprehensive testing for all modifications.

## Installation

1. Fork this repository to your GitHub account.
2. Clone the forked repository and proceed with the steps mentioned below.

### Linux/Mac

- **Create and activate a virtual environment:**
    ```bash
    virtualenv env --python=python3.8
    source env/bin/activate
    ```

- **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

- **Reset the database:**
    ```bash
    export FLASK_APP=core/server.py
    rm core/store.sqlite3
    flask db upgrade -d core/migrations/
    ```

- **Start the server:**
    ```bash
    bash run.sh
    ```

- **Run tests:**
    ```bash
    pytest -vvv -s tests/

    # For test coverage report:
    # pytest --cov
    # open htmlcov/index.html
    ```

### Windows

- **Create and activate a virtual environment:**
    ```cmd
    virtualenv env --python=python3.8
    .\env\Scripts\activate
    ```

- **Install Python dependencies:**
    ```cmd
    pip install -r requirements.txt
    ```

- **Reset the database:**
    ```cmd
    set FLASK_APP=core/server.py
    del core\store.sqlite3
    flask db upgrade -d core/migrations/
    ```

- **Start the server:**
    ```cmd
    run.bat
    ```

- **Run tests:**
    ```cmd
    pytest -vvv -s tests\

    REM For test coverage report:
    REM pytest --cov
    REM open htmlcov\index.html
    ```

### Docker Setup and Running

- **Build Docker Images:**
    ```bash
    docker-compose build
    ```

- **Run Docker Containers:**
    ```bash
    docker-compose up
    ```

- **Stop Docker Containers:**
    ```bash
    docker-compose down
    ```

### Running Tests

