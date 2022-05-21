
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def duckduckgo_scrape_page(soup):

    page_results = []

    search_results_data = soup.find_all('div', class_='result__body')

    for result in search_results_data:
        title = result.find('h2', class_='result__title').text
        link = result.find('a', class_='result__a')['href']

        check_snippet = result.find('div', class_= 'result__snippet')
        snippet = check_snippet.text if check_snippet else ''

        page_results.append(('DuckDuckGo' ,title, link, snippet))

    return page_results


def duckduckgo_nav(query='data science'):
    
    # Configuration options for Selenium WebDriver
    options = Options()  
    options.add_argument("--headless")

    service=Service(ChromeDriverManager(log_level=logging.ERROR).install())

    duckduckgo_data = []

    # Selenium WebDriver execution 
    with webdriver.Chrome(service=service, options=options) as driver:
        driver.set_window_size(1440, 712)
        driver.get('http://www.duckduckgo.com')

        # Simulate search
        driver.find_element(By.ID, 'search_form_input_homepage').send_keys(query)
        driver.find_element(By.ID, 'search_button_homepage').submit()

        WebDriverWait(driver, 10).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete'
        )

        for _ in range(4):
            check_more_pg_elt = driver.find_elements(By.CLASS_NAME, 'result--more__btn')
            if check_more_pg_elt is None:
                print('Can\'t find element to load more search results')
                break
            check_more_pg_elt[0].click()
            WebDriverWait(driver, 10).until(
                visibility_of_element_located((By.CLASS_NAME,'result--more__btn'))
            )


        soup = BeautifulSoup(driver.page_source, 'html.parser')
        data_scr = duckduckgo_scrape_page(soup)

        if len(data_scr):
            duckduckgo_data.extend(data_scr)
    return duckduckgo_data

if __name__ == '__main__':
    duckduckgo_data = duckduckgo_nav(query='Grand Canyon')
    for data in duckduckgo_data:
        print(data)
        print('----------------------------')
    print('Results Collected: ', len(duckduckgo_data))
    