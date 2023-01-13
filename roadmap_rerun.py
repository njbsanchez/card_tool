from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time
from datetime import date

from bs4 import BeautifulSoup
import json

options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def read_json_file(json_file):
    """
    takes in url of page, returns page source
    """
    file = open(json_file, 'r')
 
    # Convert the JSON data into Python object
    # Here it is a dictionary
    json_data = json.load(file)
    print(type(json_data))
    
    
    return json_data 


def add_to_dictionary(card_json):
    
    # json_data = read_json_file("json_outputs/cloud.json")
    
    cards_dictionary = read_json_file(card_json)
    print (cards_dictionary)
    
    for param in cards_dictionary.keys():
        
        
        print("param: " + param)
        print(cards_dictionary[param])
        
        try:
            print (str(cards_dictionary[param]['title']) + " has been skipped")
        
        except:
                url = cards_dictionary[param]['url']
                driver.get(url)
                soup = BeautifulSoup(driver.page_source, 'lxml')
                content = soup.find_all(class_="modal-inner")  
                
                dict_card = cards_dictionary[param]

                for i,card in enumerate(content,start=1):
                
                    title = str(card.h4.string)
                    desc = 'N/A' if card.find(class_="description").p is None else str(((card.find(class_="description")).p.contents)[0])
                    try:
                        status = str(card.find(class_="custom-category").contents[0])
                    except:
                        category = str("missing")
                    try:
                        category = str(card.find(class_="custom-category2").contents[0])
                    except:
                        category = str("none")
                    try:
                        date = str(card.find(class_="custom-field-1").contents[0])
                    except:
                        date = str("none")
                    products = []
                    try:
                        for product in card.find(class_="custom-product").contents:
                            products.append(str(product.string))
                    except:
                        pass
                    try:
                        for product in card.find(class_="custom-productVersion").contents:
                                products.append(str(product.string))
                    except:
                        pass
                    links={}
                    try:
                        for i, a in enumerate(card.find_all('a', href=True), start=1):
                            print("LINK HERE:", a["href"])
                            if "link-arrow" in a["class"]:
                                class_bool = "ok"
                            else:
                                class_bool = "needs arrow"
                            links[i]={
                                "title":a.get_text(),
                                "url":a["href"],
                                "arrow":class_bool
                            }
                            # links.append(str(a['href']))
                    except:
                        pass
                
                    dict_card.update({
                        'param':param,
                        'title':title,
                        'description':desc,
                        'status':status,
                        'category':category,
                        'date':date,
                        'products':products,
                        'links':links
                        })
                    
                    print("CARD DICTIONARY ITEM:")
                    print(dict_card)
                    print("*********************------**********************")
            
    return cards_dictionary
        

def create_report(cards_dictionary, type):
    
    today = date.today()

    if type == "cloud":
        file_name = f'cloud_cards_{today}_revised'
    elif type == "dc":
        file_name = f'dc_cards_{today}_revised'
    else:
        file_name = f'undefined_{today}_revised'
        
    with open(f'json_outputs/{file_name}.json', 'w') as outfile:
        json.dump(cards_dictionary, outfile)
    
    y=json.dumps(cards_dictionary)
    
    df = (pd.DataFrame.from_dict(cards_dictionary)).T
    file = f'csv_outputs/revisions/{file_name}.csv'
    df.to_csv (file, index = False, header=True)
  
def run_that_shit(json_file_name, roadmap_type):
        
    cards_dictionary = add_to_dictionary(json_file_name)
    create_report(cards_dictionary, roadmap_type)


if __name__ == "__main__":
    cloud_json = 'json_outputs/cloud_cards_2022-12-15.json'

    # parse_roadmap(dc_url, "dc")
    run_that_shit(cloud_json, "cloud")
    
    