
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
            articles = json.load(f)
            page = articles['page'][-1] + 1
    else: 
        with open(file_name, mode='w') as f:
            f.write(json.dumps({'page': [], 'articles': []}))

    # if thef file contains required no. of articles return 
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
            
            new_data = []
            # dump the articles to the file
            with open(file_name) as f:
                data = json.load(f)
                pages = list(data['page']) + [page]
                articles = list(data['articles'])
                new_data = {
                    'page': pages,
                    'articles': articles + items
                }

            with open(file_name, mode = 'w') as fw:
                fw.write(json.dumps(new_data))

            # break the loop if limit of pages reached
            # or it is the last page
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

