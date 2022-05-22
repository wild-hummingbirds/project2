from duck_search_api import duckduckgo_search
from bing_search_api import bing_search_api
from google_sel import google_nav
from dotenv import load_dotenv
load_dotenv()

def all_engines_data(query):
    all_data = []

    print('Searching DuckDuckGo.....')
    duck_data = duckduckgo_search(query)    
    print('Total DuckDuckGo results: ', len(duck_data))
    print('\n\n')

    
    print('Searching Bing.....')
    bing_data = bing_search_api(query)
    print('Total Bing results: ', len(bing_data))
    print('\n')


    print('Searching Google.....')
    google_data = google_nav(query)
    print('Total Google results: ', len(google_data))
    print('\n')

    all_data.extend(duck_data)
    all_data.extend(bing_data)
    all_data.extend(google_data)
    

    return all_data

if __name__ == '__main__':
    
    all_data = all_engines_data('Avengers Endgame')
    for data in all_data:
        print(data)
    print('Total length of combined data: ', len(all_data))
