#lib

import mysql.connector
from datetime import datetime
from mysql.connector import Error
import string
import random

def pre_processing_data(input_data,squery):
    # processing data before inserting to improve performance
    #search_meta (url, title,snippet, url_id, search_id)
    #search_query ( id, search_query, browser)
    for row in input_data:
        id_val1 = id_generator()
        id_val2 = id_generator()
        yield ("INSERT INTO WildHummingbirds.search_query VALUES ('{}', '{}','{}');".format(id_val1,squery,row[0]),
               "INSERT INTO WildHummingbirds.search_meta VALUES ('{}', '{}','{}','{}','{}');".format(row[2], row[1], row[3], id_val2,id_val1))


def id_generator(size=16, chars=string.ascii_uppercase + string.digits):
    # generating random var to ID value
    return ''.join(random.choice(chars) for _ in range(size))


def check_search_query_exist(squery, db, pwd):
    ''' this function will check if a search text will processed in the past, for project one we will ignore any
    search text that already exsit in DB'''
    myresult = ''  # in the event query fail we will return 0
    try:
        connection = mysql.connector.connect(host='127.0.0.1', database=db,
                                             user='root', password=pwd)
        if connection.is_connected():
            cursor = connection.cursor()
            q = "SELECT * FROM WildHummingbirds.search_query where search_query = '{}';".format(squery)
            cursor.execute(q)
            myresult = cursor.fetchall()

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    return len(myresult)
