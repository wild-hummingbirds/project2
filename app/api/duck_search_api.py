from duckduckgo_search import ddg

def duckduckgo_search(query='data science', max_results=28):
    duckduckgo_response = ddg(query, region='wt-wt', safesearch='Moderate', time='y', max_results=max_results)
    duckduckgo_results = [('DuckDuckGo',res['title'], res['href'], res['body']) for res in duckduckgo_response]

    return duckduckgo_results[:max_results] if len(duckduckgo_results) > max_results else duckduckgo_results


if __name__ == '__main__':
    duckduckgo_data = duckduckgo_search(query='data science')
    for data in duckduckgo_data:
        print(data)
        print('----------------------------')
    print('Results Collected: ', len(duckduckgo_data))
