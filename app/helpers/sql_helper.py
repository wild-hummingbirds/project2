from bs4 import BeautifulSoup
import requests
import mysql.connector
from mysql.connector import Error
from stop_words import get_stop_words
import os
from dotenv import load_dotenv
import string
import random

load_dotenv()
DB = os.environ['DB']
PWD = os.environ['DB_PASSWORD']
USER = os.environ['USERNAME']

STOP_WORDS = set(get_stop_words('en'))

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


def check_search_query_exist(squery):
    ''' this function will check if a search text will processed in the past, for project one we will ignore any
    search text that already exsit in DB'''
    myresult = ''  # in the event query fail we will return 0
    try:
        connection = mysql.connector.connect(host='127.0.0.1', database=DB,
                                             user=USER, password=PWD)
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

def get_data(squery):
    ''' this function will check if a search text will processed in the past, for project one we will ignore any
    search text that already exsit in DB'''

    myresult = ''  # in the event query fail we will return 0
    try:
        connection = mysql.connector.connect(host='127.0.0.1', database=DB,
                                             user=USER, password=PWD)
        if connection.is_connected():
            cursor = connection.cursor()
            q = "select urls.url, urls.url_id, `content`.freq from search_query INNER JOIN urls ON search_query.search_id=urls.search_id INNER JOIN `content` ON urls.url_id=`content`.url_id WHERE search_query='{}' ORDER BY `content`.freq DESC LIMIT 10;".format(squery)
            cursor.execute(q)
            myresult = cursor.fetchall()

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    return myresult

def getWebpageText(url):
    ''' Takes in URL, returns all the text from website if accessible'''
    webpage = requests.get(url)

    if webpage.status_code == 200:
        soup = BeautifulSoup(webpage.text, 'html.parser')
        webpage_text = soup.get_text(strip=True)
        return webpage_text
    else:
        return None

    
def wordFreqCount(full_text, search_term):
    if not full_text:
        return None
    else:
        terms = search_term.split()
        terms_not_stop_words = [word for word in terms if word not in STOP_WORDS]

        freq = 0

        ft_lower = full_text.lower()

        for term in terms_not_stop_words:
            freq += ft_lower.count(term.lower())        
        return freq