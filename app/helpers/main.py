from app.api.all_engine_search import all_engines_data
from app.helpers.driver_script import check_search_query_exist, id_generator
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
import os
load_dotenv()


db = 'WildHummingbirds'
pwd = os.environ['DB_PASSWORD']

insert_search_query = "INSERT INTO WildHummingbirds.search_query VALUES (%s, %s);"
insert_search_meta = "INSERT INTO WildHummingbirds.search_meta VALUES (%s, %s, %s, %s, %s, %s);"

search_query = input('Enter a search query: ')

input_data = all_engines_data(search_query)
if check_search_query_exist(search_query,db,pwd):
    print("Search query result already exsit in Database")
else:
    #inserting data into db
    #need to include validation for data already exsit
    #need to include update script if a query is run multiple time
    try:
        connection = mysql.connector.connect(host='127.0.0.1',database=db,
                                                user='root',password=pwd)
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()

            id_val1 = id_generator()
            cursor.execute(insert_search_query,(id_val1,search_query))

            for row in input_data:
                id_val2 = id_generator()
                cursor.execute(insert_search_meta, (row[0], row[2], row[1], row[3], id_val2,id_val1))
            connection.commit()


    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")




