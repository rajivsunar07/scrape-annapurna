
import requests
import json
import os

def get_articles(search, limit=None, file_name=None):
    ''' 'search' is the term to search and 'limit' is the number of pages to scrape '''

    page = 1 

    if file_name == None:
        file_name = search + '.json' # file with the search term is created
    
    pagination_record = file_name[:-5] + '-pagination.txt' # name of file to store pagination record

    
    if not os.path.isfile(pagination_record):
        with open(pagination_record, mode='w') as f:
            f.write(str(page))      # create a file and append page 1 if no pagination file
    else:
        with open(pagination_record) as f:
            current = f.readlines()[-1]
            page = int(current) + 1     # read the file to get the last page

    # if the file contains required no. of articles return 
    if limit != None and page != 1:
        if limit == (page - 1):
            print('All required articles are collected in the file: ', str(file_name))
            return
                

    while True:
        try:
            print(page)
            if page == 1:
                url = 'https://bg.annapurnapost.com/api/search?{}'.format(search)
            else:
                url = 'https://bg.annapurnapost.com/api/search?title={}&page={}'.format(search, page)
            
            data = requests.get(url)
            json_data = data.json()
            items = json_data['data']['items']
            
            # dump the articles to the file
            if not os.path.isfile(file_name):
                with open(file_name, mode='w') as f:
                    f.write(json.dumps(items))
            else:
                with open(file_name) as f:
                    articles = json.load(f)
                
                # append new articles to the file
                new_articles = articles + items

                with open(file_name, mode='w') as f:
                    f.write(json.dumps(new_articles))
            
            #  append the pagination number to the file 
            if page != 1:
                with open(pagination_record, mode='a') as f:
                    f.write('\n')
                    f.write(str(page))

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
