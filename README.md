# Data Engineering DSE I2400: Project 2

## Search Engine Analysis

## Goal:
Web based contents search engine to perform aggregated web search across Google, Bing, and DuckDuckGo search engines that displays result set ordered by frequency match for relevant search terms. The engine is capable of performing search across web results and PDF documents.

## To Use Pipenv Virtual Environment:
    - pipenv shell (Activates virtual environment)
    - pipenv install (Run this if you have dependency issues -- ModuleNotFound)
    - pipenv install <package> (Install packages needed)

## Set environment variables:
    - Create a .env file in the root directory with the following variables:
    DB=dbname
    PWD=password
    USER=username

# Bing API 
  1. Create a free Azure subscription
  2. Login to https://portal.azure.com/#home 
  3. Create a resource >> "Bing Search v7"
  4. Go to Keys and Endpoint tab and copy the key to use a subscription_key
  5. Save the key in the .env file created earlier under BING_SEARCH_V7_SUBSCRIPTION_KEY=YOUR_KEY_FROM_#4

# To Test main.py:
    - python3 -m app.helpers.main FROM THE ROOT DIRECTORY

# To Run Flask App:
    - cd app
    - flask run --reload

# Adding DB:
    - Open MySQL and run the create_DB_Tables.sql command to clone Wild Hummingbird DB 
