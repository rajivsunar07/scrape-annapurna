
import requests
import json
import os

def get_articles(search, limit=None, file_name=None):
    ''' 'search' is the term to search and 'limit' is the number of pages to scrape '''

    page = 1 

    if file_name == None:
        file_name = search + '.json' # file with the search term is created

    if os.path.isfile(file_name):
        with open(file_name) as f:
            articles = list(json.load(f))
            page = articles[-1]['page'] + 1
    else: 
        with open(file_name, mode='w') as f:
            f.write(json.dumps([]))

    # if the file contains required no. of articles return 
    if limit != None and page != 1:
        if limit == (page - 1):
            print('All required articles are collected in the file: ', str(file_name))
            return
                
    while True:
        try:
            if page == 1:
                url = 'https://bg.annapurnapost.com/api/search?title={}'.format(search)
            else:
                url = 'https://bg.annapurnapost.com/api/search?title={}&page={}'.format(search, page)  
            items = requests.get(url).json()['data']['items']
            print(requests.get(url).json())
            
            articles = []
            # dump the articles to the file
            with open(file_name) as f:
                articles = list(json.load(f)) + [{'page': page, 'articles': items}]
              
            with open(file_name, mode = 'w') as fw:
                fw.write(json.dumps(articles))

            # break the loop if limit of pages reached
            # or it is the last page
            if limit != None: 
                if limit == page:
                    break
            if len(items)<10:
                print('This is the last page:', page)
                break

            page += 1
           
        except requests.ConnectionError as e:
            print('A network error occured while connecting. Please check your internet connection.')
            print(str(e))
            break
        except requests.RequestException as e:
            print('An error occured while connecting at pagination: ', page)
            print(str(e))
            break
        except KeyError as e:
            print('This is the last page: ', page - 1 )
            break