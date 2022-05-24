from bs4 import BeautifulSoup
import requests
import mysql.connector
from mysql.connector import Error
from stop_words import get_stop_words
import os
from dotenv import load_dotenv
import string
import random
import pdfplumber
import urllib3
import io

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

def get_data(squery,num_res=5):
    ''' this function will check if a search text will processed in the past, for project one we will ignore any
    search text that already exsit in DB'''

    myresult = ''  # in the event query fail we will return 0
    try:
        connection = mysql.connector.connect(host='127.0.0.1', database=DB,
                                             user=USER, password=PWD)
        if connection.is_connected():
            cursor = connection.cursor()
            q = "select urls.url, urls.url_id, `content`.freq, `content`.content_type from search_query INNER JOIN urls ON search_query.search_id=urls.search_id INNER JOIN `content` ON urls.url_id=`content`.url_id WHERE search_query='{}' ORDER BY `content`.freq DESC LIMIT {};".format(squery, num_res)
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

def get_data_pdf(squery,num_res=5):
    ''' this function will check if a search text will processed in the past, for project one we will ignore any
    search text that already exsit in DB'''

    myresult = ''  # in the event query fail we will return 0
    try:
        connection = mysql.connector.connect(host='127.0.0.1', database=DB,
                                             user=USER, password=PWD)
        if connection.is_connected():
            cursor = connection.cursor()
            q = "select urls.url, urls.url_id, `content`.freq, `content`.content_type from search_query INNER JOIN urls ON search_query.search_id=urls.search_id INNER JOIN `content` ON urls.url_id=`content`.url_id WHERE search_query='{}' AND `content`.content_type='PDF' ORDER BY `content`.freq DESC LIMIT {};".format(squery, num_res)
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

def get_data_web(squery,num_res=5):
    ''' this function will check if a search text will processed in the past, for project one we will ignore any
    search text that already exsit in DB'''

    myresult = ''  # in the event query fail we will return 0
    try:
        connection = mysql.connector.connect(host='127.0.0.1', database=DB,
                                             user=USER, password=PWD)
        if connection.is_connected():
            cursor = connection.cursor()
            q = "select urls.url, urls.url_id, `content`.freq, `content`.content_type from search_query INNER JOIN urls ON search_query.search_id=urls.search_id INNER JOIN `content` ON urls.url_id=`content`.url_id WHERE search_query='{}' AND `content`.content_type='HTML' ORDER BY `content`.freq DESC LIMIT {};".format(squery, num_res)
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
    headers={"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    webpage = requests.get(url, headers=headers)

    if webpage.status_code == 200:
        soup = BeautifulSoup(webpage.text, 'html.parser')
        webpage_text = soup.get_text(strip=True)
        return webpage_text
    else:
        return None

def extract_pdf_by_url(url):
    http = urllib3.PoolManager()
    temp = io.BytesIO()
    temp.write(http.request("GET", url).data)
    all_text = ''

    with pdfplumber.open(temp) as pdf:
        print(f'TOTAL PAGES IN PDF: {len(pdf.pages)}')
        for num,pdf_page in enumerate(pdf.pages):
            if num == 10:
                break
            single_page_text = pdf_page.extract_text()
            all_text = all_text + '\n' + single_page_text
    return all_text.strip()

    
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
        return freq/len(full_text.split())