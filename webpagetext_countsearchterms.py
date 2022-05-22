from bs4 import BeautifulSoup
import requests

def getWebpageText(url):
    ''' Takes in URL, returns all the text from website if accessible'''
    webpage = requests.get(url)

    if webpage.status_code is 200:
      soup = BeautifulSoup(webpage.text, 'html.parser')
      webpage_text = soup.get_text(strip=True)
      return webpage_text
    else:
      print(f'Cant access {url}')
    return None

    
def wordFreqCount(full_text, search_term):
  terms = search_term.split()
  freq = 0
  ft_lower = full_text.lower()
  for term in terms:
    freq += ft_lower.count(term.lower())
  return freq
