# Project 2

## To Use Pipenv Virtual Environment:
    - pipenv shell (Activates virtual environment)
    - pipenv install (Run this if you have dependency issues -- ModuleNotFound)
    - pipenv install <package> (Install packages needed)

## Set environment variables:
    - Run the following commands while in your virtual environment
    ```
    export DB=dbname
    export PWD=password
    export USER=username
    ```

# To Test main.py:
    - python3 -m app.helpers.main FROM THE ROOT DIRECTORY

# To Run Flask App:
    - cd app
    - flask run --reload

# Adding DB:
    - Open MySQL and run the create_DB_Tables.sql command to clone Wild Hummingbird DB 
