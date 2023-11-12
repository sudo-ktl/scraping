import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import re
import csv

stock_src = 'https://kabutan.jp/stock/kabuka?code=9983&ashi=day&page='

dfs_main = pd.read_html(f'{stock_src}1')[5]

page_number = 2;
while page_number <= 10:
    stock_src = f'https://kabutan.jp/stock/kabuka?code=9983&ashi=day&page={page_number}'
    page_number += 1;
    dfs = pd.read_html(stock_src)[5]
    dfs_main = pd.concat([dfs_main,dfs])

dfs_i = dfs_main.set_index('日付')
print(dfs_i)

dt_now = datetime.datetime.now().strftime('%Y%m%d')
file_name = 'fastretailing_stock' + dt_now + '.csv'

dfs_i.to_csv(file_name)