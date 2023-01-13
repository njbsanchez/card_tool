import pandas as pd
import numpy as np
import time
from datetime import date
import json
import os

def change_column_name(df, version):
    print(list(df.columns.values))

    df.rename(columns = {"url": f"url_{version}",
                        "param": "param",
                        "title": f"title_{version}",
                        "description": f"description_{version}",
                        "status": f"status_{version}",
                        "category": f"category_{version}",
                        "date": f"date_{version}",
                        "products": f"products_{version}",
                        "links": f"links_{version}",
                        }, 
              inplace = True)
    
    # print(list(df.columns.values))
    return df

def merge_both_reports(old, new):
    
    old = change_column_name(old, "old")
    new = change_column_name(new, "new")
    
    all_data = pd.merge(old, new, how='outer', on='param')
    
    # print(all_data)
    
    return all_data

def compare_report(all_data):
    
    all_data['changes'] = ''
    
    # np.where(condition, value if condition is true, value if condition is false)
    #df['col'].apply(lambda x: "{}{}".format('str', x))

    all_data['changes'] = np.where(all_data['title_new'] != all_data['title_old'], all_data['changes'] + 'title, ', all_data['changes'])
    all_data['changes'] = np.where(all_data['description_new'] != all_data['description_old'], all_data['changes'] + 'description, ',all_data['changes'])
    all_data['changes'] = np.where(all_data['status_new'] != all_data['status_old'], all_data['changes'] + 'status, ',all_data['changes'])
    all_data['changes'] = np.where(all_data['category_new'] != all_data['category_old'], all_data['changes'] + 'category, ',all_data['changes'])
    all_data['changes'] = np.where(all_data['date_new'] != all_data['date_old'], all_data['changes'] + 'date, ',all_data['changes'])
    all_data['changes'] = np.where(all_data['links_new'] != all_data['links_old'], all_data['changes'] + 'links, ',all_data['changes'])

    
    all_data['changes'] = np.where(all_data['title_old'].isnull(), 'new card', all_data['changes'])
    all_data['changes'] = np.where(all_data['title_new'].isnull(), 'deleted', all_data['changes'])

    print (all_data)
    
    return all_data

def create_report(df,roadmap,type):
    
    today = date.today()
    # print("Today's date:", today)
    
    path = f'/Users/nsanchez/Desktop/card_parser_tool/comparison_reports/{today}'

    isExist = os.path.exists(path)

    if not isExist:

        os.makedirs(path)
        print("The new directory is created!")
        
    else:
        file_name = f'{roadmap}_report_{type}_{today}'
        file = f'comparison_reports/{today}/{file_name}.csv'
        df.to_csv(file, index=False, header=True)
        
def run_report(old_report, new_report, type):
    
    old = pd.read_csv(old_report)
    # print(old)
    new = pd.read_csv(new_report)
    # print(new)
    
    report = merge_both_reports(old, new)
    
    results = compare_report(report)
    
    create_report(results, type, "compare_report")

if __name__ == "__main__":
    
    old_cloud = "csv_outputs/production/cloud_cards_2022-12-10.csv"
    new_cloud = "csv_outputs/production/cloud_cards_2022-12-15.csv"
    
    old_dc = "csv_outputs/production/dc_cards_2022-12-10.csv"
    new_dc = "csv_outputs/production/dc_cards_2022-12-13.csv"
    
    # run_report(old_dc, new_dc, "dc")
    run_report(old_cloud, new_cloud, "cloud")



