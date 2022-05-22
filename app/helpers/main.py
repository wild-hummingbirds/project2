from app.api.all_engine_search import all_engines_data
from app.helpers.sql_helper import *
import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
import os

load_dotenv()

DB = os.environ['DB']
PWD = os.environ['DB_PASSWORD']
USER = os.environ['USERNAME']

insert_search_query = "INSERT INTO WildHummingbirds.search_query VALUES (%s, %s);"
insert_search_urls = "INSERT INTO WildHummingbirds.urls VALUES (%s, %s, %s, %s, %s, %s);"
insert_content = "INSERT INTO WildHummingbirds.content VALUES (%s, %s, %s, %s, %s)"
check_url_exists = "SELECT * FROM WildHummingbirds.content where url = (%s)"


# search_query = input('Enter a search query: ')

def data_dump(search_query):
    try:
        connection = mysql.connector.connect(host='127.0.0.1', database=DB,
                                             user=USER, password=PWD)
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()

            input_data = all_engines_data(search_query, max_results=5)

            search_id = id_generator()
            cursor.execute(insert_search_query, (search_id, search_query))

            for row in input_data:
                engine_name, title, url, snippet = row[:4]
                url_id = id_generator()
                cursor.execute(insert_search_urls, (engine_name, title, url, snippet, url_id, search_id))

                try:
                    page_content = getWebpageText(url)
                except:
                    page_content = None

                cursor.execute(check_url_exists, (url,))
                url_exists = len(cursor.fetchall())

                if not url_exists:
                    freq = wordFreqCount(full_text=page_content, search_term=search_query)
                    cursor.execute(insert_content, (url_id, url, page_content, 'Webpage', freq))

            connection.commit()


    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
