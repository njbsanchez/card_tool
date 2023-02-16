import pandas as pd
import numpy as np
import time
from datetime import *
import json
import os
# from spellchecker import SpellChecker

def create_report(df,type,enviro):
    
    today = date.today()
    now = datetime.now()
    
    path_name = f"~/Downloads/card_parser_tool/{today}/{enviro}"
    
    path_name = path_name.replace(" ", "_")
    print(path_name)
    path = os.path.expanduser(path_name)

    isExist = os.path.exists(path)
    
    if not isExist:
    
        os.makedirs(path)
        print("The new directory is created!")

    file_name = f'{type}_qa_checker_{now}.csv'
    file = (f'{path}/{file_name}').replace(" ", "_")  
    df.to_csv(file, index=False, header=True)
    
    return file

######### DEFS ###########

def current_quarter():
    
    month = date.today().month
    
    if month in {1, 2, 3}:
        quarter = 0
    elif month in {4, 5, 6}:
        quarter = .25
    if month in {7, 8, 9}:
        quarter = .50
    if month in {10, 11, 12}:
        quarter = .75
    
    return quarter

def fix_hyphen_dates(x, x_tup):
    xx = tuple(x_tup[1].split(" "))[1]
    new_x = (str(x[0])+" "+str(xx))
    new_input = (str(new_x), str(x_tup[1]))
    comp_q = convert_date(new_input)
    
    return comp_q


def convert_date(x_tup):

    cur_year = date.today().year
    cur_month = date.today().month
    
    comp_q = float(0.0)
    
    x = tuple(x_tup[0].split(" "))
        
    if x[0] == 'none':
        return "Missing date"
    
    elif len(x) > 1:
        q = x[0].lstrip('Qa')
        # print(x[1])
        try:
            y = float(x[1])
            q = float(q)
        except ValueError:
            return "error"
                  
        if float(y) != float(cur_year):
            comp_q += (y-cur_year)
            
        if float(q) == 1:
            comp_q += .0
        elif float(q) == 2:
            comp_q += .25
        elif float(q) == 3:
            comp_q += .50
        elif float(q) == 4:
            comp_q += .75
        
        return comp_q

    elif len(x) == 1:
        
        if 'Q' in x[0]:
        
            comp_q = fix_hyphen_dates(x, x_tup)
        
            return comp_q
        
        y = float(x[0])
                  
        
        if float(y) > float(cur_year):
            
            comp_q += (y-cur_year)      
        else:
            comp_q = "date issue"  
        
        return comp_q
    
def compare_date(date):

    date_comp = str(date).split(' - ')
    date_comp = tuple(date_comp)
    card_num_scale = convert_date(date_comp)
    type(card_num_scale)
    this_q = 0.0
    if type(card_num_scale) == str:
        return "date issue"
    elif card_num_scale <= this_q:
        return "Released"
    
    diff = card_num_scale - this_q

    if diff <= .50:
        return "Coming soon"
    elif diff >= .50:
        return "Future"

######### WIP ############

# def pull_missing_info(data):
    
#     status_legend = pd.read_csv("legend.csv")

#     data_w_status = pd.merge(data, status_legend, how='outer', on='date')
#     incorrect_status_df = data_w_status.loc[(data_w_status['status'] != data_w_status['correct_status'])]
#     incorrect_status_df.dropna(inplace=True)
#     incorrect_status_df['error_status'] = 'incorrect status'
#     print(incorrect_status_df.head(5))
    
#     return incorrect_status_df
    
      
# def spellcheck(words):
#     spell = SpellChecker()
#     words_lst = list(words.split(" "))
#     misspelled = spell.unknown(words_lst)
    
#     isEmpty = (len(misspelled) == 0)
#     print (words + "......... : ")
#     for word in misspelled:
#         print (word + " : " + spell.correction(word))
#         print ("*****")
#     return misspelled

# def check_spelling(data):
    
#     print("************* spell check ****************")
     
#     data['spell_check'] = data['description'].apply(lambda x: spellcheck(x))
#     data['spell_check_2'] = data['title'].apply(lambda x: spellcheck(x))
    
   
#     print(data)
#     return

######### CHECKERS ###########

def pull_incorrect_status(data):
    """
    get todays quarter
    for each card
        compare if cards year is past, same, or future year
            if past: status = release
            if future
            if same or future: continue
        
        compare if card quarter
    """
    
    cur_year = date.today().year
    cur_month = date.today().month
    
    cur_year = 2022
    cur_month = 12
    
    current_q = current_quarter()
    status_check = data

    status_check['year_check'] = list(
    map(lambda x: compare_date(x), status_check['date']))
    
    status_check['status_issue'] = np.where(status_check['year_check'] != status_check['status'], "incorrect status", "")
    
    
    report = status_check[['param', 'status_issue', 'year_check']].copy()
    
    # print("~~~~~~~~~~~STATUS REPORT")
    # for col in report.columns:
    #     # print(col)
    
    return report

def pull_learn_more(data):
    
    data['links'] = data['links'].astype(str)
    contains_learn_more = data.loc[data['links'].str.contains('Learn more')]
    contains_learn_more['error_learn'] = 'change learn more'
    
    report = contains_learn_more[['param', 'error_learn']].copy()
    
    # print("~~~~~~~~~~~LEARN MORE REPORT")
    # for col in report.columns:
    #     print(col)
        
    return report

def pull_arrow_error(data):
    
    data['links'] = data['links'].astype(str)
    needs_arrow = data.loc[data['links'].str.contains('missing arrow')]
    needs_arrow['error_arrow'] = 'missing arrow'
    
    report = needs_arrow[['param', 'error_arrow']].copy()
    
    # print("~~~~~~~~~~~ARROW  REPORT")
    # for col in report.columns:
    #     print(col)
        
    return report

def check_fullstop(data):
    
    needs_fullstop = data
    needs_fullstop['full_stop'] = list(
    map( lambda x: str(x).endswith('.'), data['description']))
    needs_fullstop = data.loc[data['full_stop'] == False]
    needs_fullstop['missing_fullstop'] = np.where(needs_fullstop['full_stop'] == False, "missing fullstop", "")
    needs_fullstop.drop(['full_stop'], axis=1, inplace=True)
        
    report = needs_fullstop[['param', 'missing_fullstop']].copy()
    
    # print("~~~~~~~~~~~FULLSTOP REPORT")
    # for col in report.columns:
    #     print(col)
        
    return report

def check_uppercase(data):
    
    uppercase_check = data
    uppercase_check['uppercase'] = list(
    map(lambda x: print(str(x).isupper()), uppercase_check['description']))
    
    uppercase_check['needs_uppercase'] = np.where(uppercase_check['uppercase'] == False, "missing uppercase", "")
    
    uppercase_check.drop(['uppercase'], axis=1, inplace=True)
    
    report = uppercase_check[['param', 'needs_uppercase']].copy()
    
    # print("~~~~~~~~~~~UPPERCASE  REPORT")
    # for col in report.columns:
    #     print(col)
        
    return report

 
######### RUN IT ###########

def analyze_scrape(csv_file_path, roadmap_type, enviro):
    """ 
    - identify 'learn more' links
    - check if status is not correct
    - check if learn more link has no arrow
    """
    data = pd.read_csv(csv_file_path)
    
    status_check = pull_incorrect_status(data)
  
    contains_learn_more = pull_learn_more(data)
    
    needs_arrow = pull_arrow_error(data)
    
    full_stop = check_fullstop(data)
    
    uppercase = check_uppercase(data)
   
   
    # spell_check = check_spelling(data)

    
    two_errors = pd.merge(status_check, contains_learn_more, how='outer', on='param')
    other_two_errors = pd.merge(needs_arrow, full_stop, how='outer', on='param')
    another_errors = pd.merge(other_two_errors, uppercase, how='outer', on='param')
    all_errors = pd.merge(two_errors, another_errors, how='outer', on='param')


        
    only_errors = all_errors[['param', 'status_issue', 'error_learn', 'error_arrow', 'missing_fullstop', 'needs_uppercase']].copy()
    
    only_errors["errors"] = only_errors["error_learn"].astype(str)
    only_errors["errors"] = only_errors['errors'].astype(str) +", "+ only_errors["error_arrow"].astype(str)
    only_errors["errors"] = only_errors['errors'].astype(str) +", "+ only_errors["missing_fullstop"].astype(str)
    only_errors["errors"] = only_errors['errors'].astype(str) +", "+ only_errors["needs_uppercase"].astype(str)
    only_errors["errors"] = only_errors['errors'].astype(str) +", "+ only_errors["status_issue"].astype(str)

    only_errors["errors"] = only_errors["errors"].str.replace(r'nan, ', '')
    only_errors["errors"] = only_errors["errors"].map(lambda x: str(x).rstrip(', '))
    only_errors["errors"] = only_errors["errors"].map(lambda x: str(x).lstrip(', '))
    
    only_errors = only_errors[['param', 'errors']].copy()
    
    all_data = pd.merge(data, only_errors, how='outer', on='param')
    
    all_data.drop(['needs_uppercase', 'full_stop', 'year_check', 'status_issue'], axis=1, inplace=True)



    file_name = create_report(all_data, roadmap_type, enviro)

    print("**********************--**************************")
    ""
    
    return file_name


if __name__ == "__main__":
    file = "/Users/nsanchez/Downloads/card_parser_tool/2023-01-09/production/cloud_cards_2023-01-09 13:24:30.306658.csv"
    # dc = "csv_outputs/dc_cards_2022-12-09_revised.csv"
    # analyze_scrape(cloud, "cloud", "staging")
    analyze_scrape(file, "cloud", "production")