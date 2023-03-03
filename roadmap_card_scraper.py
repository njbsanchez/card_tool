
import pandas as pd
import time
from datetime import datetime, date
import os
import requests
import pygsheets


from bs4 import BeautifulSoup
import json

import os.path

# import gspread
# from gspread_dataframe import set_with_dataframe
# from google.oauth2.service_account import Credentials
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive

# scopes = ['https://www.googleapis.com/auth/spreadsheets',
#           'https://www.googleapis.com/auth/drive']

# credentials = Credentials.from_service_account_file('credentials', scopes=scopes)

# gc = gspread.authorize(credentials)

# gauth = GoogleAuth()
# drive = GoogleDrive(gauth)

# # open a google sheet
# gs = gc.open_by_key(your_sheet_key)
# # select a work sheet from its name
# worksheet1 = gs.worksheet('Sheet1')

def parse_main_page(url):
    """
    takes in url of page, returns page source
    """
    
    page = requests.get(url)
    page.status_code
    
    # driver.get(url)
    # soup = BeautifulSoup(driver.page_source, 'lxml')
    
    soup = BeautifulSoup(page, 'lxml')
    item_link = soup.find_all(class_="item-link")  
    
    
    # driver.get(url)
    # item_link = driver.find_elements(By.CLASS_NAME, value="item-link")
    
    cards_dictionary = {}
    counter = 0
    
    for link in item_link:
        
        if link.is_displayed():
            driver.execute_script("arguments[0].click();", link)
            time.sleep(1)
            current_url = driver.current_url
            print(current_url)
            
        try:
            param = current_url.split("?&p=",1)[1]
            print(param)
            counter += 1
            
        except:
            param = str("none")
            
        cards_dictionary[param]={'url':current_url}
        
        print("card dictionary url is ", cards_dictionary[param])
        
    print("# of cards: " + str(counter))
    print("# of cards in dictionary: " + str(len(cards_dictionary)))
        
    return cards_dictionary 

def add_to_dictionary(cards_dictionary):
    
    for param in cards_dictionary.keys():
        
        url = cards_dictionary[param]['url']
        page = requests.get(url)
        page.status_code
        
        # driver.get(url)
        # soup = BeautifulSoup(driver.page_source, 'lxml')
        
        soup = BeautifulSoup(page, 'lxml')
        print(soup)
        content = soup.find_all(class_="modal-inner")  

        for i,card in enumerate(content,start=1):
        
            try:
                title = str(card.h4.string)
            except:
                title = 'none'
            try:
                desc = 'N/A' if card.find(class_="description").p is None else str(((card.find(class_="description")).p.contents)[0])
            except:
                desc = 'none'
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
            
            try:
                products = []
                for product in card.find(class_="custom-product").contents:
                    products.append(str(product.string))
            except:
                products = ["none"]
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
        
            cards_dictionary[param].update({
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
            print(cards_dictionary[param])
            print("*********************------**********************")
    
    return cards_dictionary
        
    
def get_data(url):
    
    
    cards_dictionary = parse_main_page(url)
    add_to_dictionary(cards_dictionary)
    
    return cards_dictionary


def create_report(cards_dictionary, type, environment):
    
    today = date.today()
    now = datetime.now()
    
    path_name = f"~/Downloads/card_parser_tool/{today}/{environment}"
    path = os.path.expanduser(path_name)

    isExist = os.path.exists(path)

    if not isExist:

        os.makedirs(path)
        print("The new directory is created!")

    file_name = f'{type}_cards_{now}'
        
    with open(f'{path}/{file_name}.json', 'w') as outfile:
        json.dump(cards_dictionary, outfile)
    
    y=json.dumps(cards_dictionary)
    
    df = (pd.DataFrame.from_dict(cards_dictionary)).T
    file = f'{path}/{file_name}.csv'
    df.to_csv (file, index = False, header=True)
    
    return file
  
  
def parse_roadmap(roadmap_type, enviro, product_area="none"):
    
    if roadmap_type == "cloud":
        route = "cloud"    
    elif str(roadmap_type) in  {"data-center", "dc", "DC"}:
        route = "data-center"
    else:
        return KeyError
    
    if enviro in {"prod", "production"}:
        url = f"https://atlassian.com/roadmap/{route}"
    elif enviro in {"author", "proof", "truth"}:
        url = f"https://{enviro}.marketing.internal.atlassian.com/wac/roadmap/{route}"
        
    cards_dictionary = get_data(url)
    
    filename = create_report(cards_dictionary, roadmap_type, enviro)
    
    return filename

def what_product_area(product_area):
    """ 
    if product_area is Enterprise & Platform
        return link with....

    if product_area is Agile & DevOps
        return link with....

    if product_area is IT Solutions
        return link with....

    if product_area is Work Management
        return link with....

    if product_area is Enterprise & Platform 
        return link with....

    if product_area is DC Products
        return link with....
    """
    return product_area

if __name__ == "__main__":
    parse_roadmap("cloud", "prod")