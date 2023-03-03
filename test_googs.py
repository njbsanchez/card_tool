
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from lxml.html.soupparser import fromstring

import pandas as pd

from bs4 import BeautifulSoup
import json
import requests


scopes = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

credentials = Credentials.from_service_account_file('credentialss.json', scopes=scopes)

gc = gspread.authorize(credentials)

gauth = GoogleAuth()
drive = GoogleDrive(gauth)

ss_key = "1Sjyps-nVTx6HlzMqywVKr90m5CACRtqMSIcPt6MPSZI"
# open a google sheet
gs = gc.open_by_key(ss_key)
# select a work sheet from its name
# worksheet1 = gs.worksheet('Sheet3')

# # dataframe (create or import it)
# df = pd.DataFrame({'a': ['apple','airplane','alligator'], 'b': ['banana', 'ball', 'butterfly'], 'c': ['cantaloupe', 'crane', 'cat']})
# # write to dataframed
# worksheet1.clear()
# set_with_dataframe(worksheet=worksheet1, dataframe=df, include_index=False,
# include_column_header=True, resize=True)


URL = "https://atlassian.com/roadmap/cloud"
page = requests.get(URL)

soup = BeautifulSoup(page.text, 'lxml')
print(soup)
item_link = soup.find_all(class_="item-link")  

print(item_link)
    
