import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def google_scrape_page(soup):
    page_results = []
    for result in soup.find_all('div', class_='tF2Cxc'):
        title = result.find('h3', class_='DKV0Md').text
        link = result.find('div', class_='yuRUbf').find('a')['href']

        check_snippet = result.find('div', class_='lyLwlc')
        snippet = check_snippet.text if check_snippet else ''

        page_results.append(('Google' ,title, link, snippet))

    return page_results


def google_query(query='Avengers Endgame', number_of_pages=1): 
    return f'https://www.google.com/search?q={query}&num=20'


def google_nav(query='data science', max_results=20):
    url = google_query(query)

    # Configuration options for Selenium WebDriver
    options = Options()  
    options.add_argument("--headless")

    service=Service(ChromeDriverManager(log_level=logging.ERROR).install())

    google_data = []
    # Selenium WebDriver execution 
    with webdriver.Chrome(service=service, options=options) as driver:
        driver.set_window_size(1440, 712)
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        data_scr = google_scrape_page(soup)

        google_data.extend(data_scr)

    if max_results > 20:
        max_results=20

    return google_data[:max_results]


if __name__ == '__main__':
    google_data = google_nav(query='data science')
    for data in google_data:
        print(data)
        print('----------------------------')
    print('Results Collected: ', len(google_data))
    
