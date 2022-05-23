import os
from dotenv import load_dotenv
import time
import requests
import json

def bing_search_api(query='data science', max_results=30):
  '''
  1. Create a free Azure subscription
  2. Login to https://portal.azure.com/#home 
  3. Create a resource >> "Bing Search v7"
  4. Go to Keys and Endpoint tab and copy the key to use a subscription_key
  5. Save the key in a .env file under BING_SEARCH_V7_SUBSCRIPTION_KEY=YOUR_KEY_FROM_#4

  '''
  subscription_key = os.environ['BING_SEARCH_V7_SUBSCRIPTION_KEY']

  results_raw = [] # list to store raw results
  headers = { 'Ocp-Apim-Subscription-Key': subscription_key}

  params = { 'q': query, 'mkt': 'en-US' ,'count': max_results, 'offset':0}
  r = requests.get('https://api.bing.microsoft.com/v7.0/search', headers=headers, params=params)
  
  #check if the key exists
  if 'webPages' in r.json():
    search_results = r.json()['webPages']['value']

    # getting the desired fields and appending to the list
    for res in search_results:
      # if the result set is not already in results_raw >> append
      if [res['name'], res['url'], res['snippet']] not in results_raw:
        results_raw.append([res['name'], res['url'], res['snippet'], 'HTML'])
    
    # incrementing offset by n_results to get to the next page
    # https://docs.microsoft.com/en-us/bing/search-apis/bing-web-search/page-results
      

  results_trimmed = [['Bing']+[r for r in res] for res in results_raw[:500]]

  # converting to tuples according to the template
  results_final = [tuple(x) for x in results_trimmed]

  # print(f'Final number of search results is: {len(results_final)}')
  return results_final

if __name__ =='__main__':
    load_dotenv()
    bing_data = bing_search_api()
    # for data in bing_data:
    #     print(data)
    print(bing_data[0])
    print('Results Collected: ', len(bing_data))