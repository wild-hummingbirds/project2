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

def data_dump(search_query, max_results=5):
    try:
        connection = mysql.connector.connect(host='127.0.0.1', database=DB,
                                             user=USER, password=PWD)
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()

            input_data = all_engines_data(search_query, max_results=max_results)

            search_id = id_generator()
            cursor.execute(insert_search_query, (search_id, search_query))

            for row in input_data:
                engine_name, title, url, snippet, res_type = row[:5]
                url_id = id_generator()
                cursor.execute(insert_search_urls, (engine_name, title, url, snippet, url_id, search_id))

                if res_type == 'HTML':
                    try:
                        page_content = getWebpageText(url)
                        print('Webpage text extracted!')
                    except:
                        page_content = None
                
                elif res_type == 'PDF':
                    try:
                        print('Starting PDF extraction')
                        print(url)
                        if url.endswith('.pdf'):
                            page_content = extract_pdf_by_url(url)
                        else:
                            page_content = None
                        print('PDF text extracted!')
                    except:
                        page_content = None

                cursor.execute(check_url_exists, (url,))
                url_exists = len(cursor.fetchall())

                if not url_exists:
                    freq = wordFreqCount(full_text=page_content, search_term=search_query)
                    print('Frequency counter complete!')
                    cursor.execute(insert_content, (url_id, url, page_content, res_type, freq))

            connection.commit()


    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

if __name__ == '__main__':
    query = input('Enter search query: ')
    max_searches = input('Enter number of searches per engine: ')
    data_dump(query, int(max_searches))
