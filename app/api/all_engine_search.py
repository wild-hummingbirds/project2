from app.api.duckduckgo_sel import duckduckgo_nav
from app.api.google_sel import google_nav
from app.api.bing_search_api import bing_search_api
from dotenv import load_dotenv
load_dotenv()

def all_engines_data(query):
    all_data = []

    
    # print('Searching Bing.....')
    # bing_data = bing_search_api(query)
    # print('Total Bing results: ', len(bing_data))
    # print('\n')

    print('Searching Google.....')
    google_data = google_nav(query)
    print('Total Google results: ', len(google_data))
    print('\n')

    print('Searching DuckDuckGo.....')
    duck_data = duckduckgo_nav(query)    
    print('Total DuckDuckGo results: ', len(duck_data))
    print('\n\n')

    #all_data.extend(bing_data)
    all_data.extend(google_data)
    all_data.extend(duck_data)

    return all_data

# if __name__ == '__main__':
#
#     all_data = all_engines_data('Avengers Endgame')
#     for data in all_data:
#         print(data)
#     print('Total length of combined data: ', len(all_data))
