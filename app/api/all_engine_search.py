from app.api.duck_search_api import duckduckgo_search, duckduckdgo_pdf_search
from app.api.bing_search_api import bing_search_api
from app.api.google_search_api import google_nav
from dotenv import load_dotenv

load_dotenv()


def all_engines_data(query, max_results=28):
    all_data = []

    print('Searching DuckDuckGo.....')
    duck_data = duckduckgo_search(query, max_results)
    print('Total DuckDuckGo results: ', len(duck_data))
    print('\n\n')

    print('Searching PDFs.....')
    pdf_data = duckduckdgo_pdf_search(query, max_results)
    print('Total DuckDuckGo results: ', len(pdf_data))
    print('\n\n')



    print('Searching Bing.....')
    bing_data = bing_search_api(query, max_results)
    print('Total Bing results: ', len(bing_data))
    print('\n')

    print('Searching Google.....')
    google_data = google_nav(query, max_results)
    print('Total Google results: ', len(google_data))
    print('\n')

    all_data.extend(duck_data)
    all_data.extend(pdf_data)
    all_data.extend(bing_data)
    all_data.extend(google_data)

    return all_data


if __name__ == '__main__':

    all_data = all_engines_data('Avengers Endgame')
    for data in all_data:
        print(data)
    print('Total length of combined data: ', len(all_data))
