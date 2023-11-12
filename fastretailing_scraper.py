import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import datetime
from datetime import time
import pytz
import re
import csv

# ニュースを日付と本文のリストで取得する
news_src = 'https://www.fastretailing.com/jp/about/news/2023.html'
response = requests.get(news_src)
soup = BeautifulSoup(response.content, 'lxml')
elem = soup.find('dl',class_ = 'about-newsrelease pkg')

date_elems = elem.find_all('dt')
date_list = []
for date_elem in date_elems:
    stock_date = date_elem.get_text().replace('.','/')[2:]
    date_list.append(stock_date)

url_elems = elem.find_all('a')
url_list = []
for url_elem in url_elems:
    url_list.append('https://www.fastretailing.com' + url_elem.attrs['href'])

text_list = []
for url in url_list:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    elem = soup.find('div',class_ = 'entry-content pkg')
    text_list.append(elem.getText().replace('\n',''))


# 株価のcsvを読み込んでニュースの日付から当日の株価を検索。無い場合それより先の直近の株価を返す

def isValidDate(list,stock_date): 
    if(stock_date in stock_date_list):
        return True
    else:
        return False
    
# yy/mm/ddの形で返す
# 株価の日時リストにニュースの日時が無い場合、直近の株価日時を返す
def findNextValidDate(stock_date,stock_date_list):
    current_date = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
    t = stockDateToDateObject(stock_date)
    tDatetime = dateToDatetime(t)
    while(current_date >= tDatetime):
        t1 = t + datetime.timedelta(days=1)
        t1ft = t1.strftime('%y/%m/%d')
        if(isValidDate(stock_date_list,t1ft)):
            return t1ft
        else:
            t = t1
            tDatetime = dateToDatetime(t)
    # print(current_date,tDatetime)
    return current_date #株価リストにまだ日時が登録されていない事を表したい

# yy/mm/ddの形で渡してdateオブジェクトを返す
def stockDateToDateObject(stock_date):
    y = stock_date[0:2]
    year = int(f"20{y}")
    month = int(stock_date[3:5])
    day = int(stock_date[6:8])
    return datetime.date(year,month,day)

def dateToDatetime(dateObject):
    dt_native = datetime.datetime.combine(dateObject, time())
    return pytz.timezone('Asia/Tokyo').localize(dt_native)

df = pd.read_csv('fastretailing_stock20231109.csv')
stock_date_list = df['日付'].tolist()
stock_list = df.values.tolist() #csvの二次元配列
news_list = list(zip(date_list,text_list))

# print(stock_list)

# print(news_list)

# pandasを使わず二次元配列の総当たりで検索している
result_list = [] 
for news in news_list:
    stock_date = news[0]
    if(isValidDate(stock_date_list,stock_date)):
        for stock in stock_list:
            if stock[0] == stock_date:
                result_list.append(stock)
            else:
                continue
    else:
        stock_date = findNextValidDate(stock_date,stock_date_list)
        for stock in stock_list:
            if stock[0] == stock_date:
                result_list.append(stock)
            else:
                continue
# print(result_list)
# for news in news_list:
# print(type(news_list[0]))
# print(type(result_list[0]))

# この2つの二次元配列から必要な箇所をピックしてcsvにまとめる

i = 0
output = []
while i < len(news_list):
    row = []
    row.append(news_list[i][0])
    row.append(news_list[i][1])
    row.append(result_list[i][0])
    row.append(result_list[i][1])
    row.append(result_list[i][4])
    if(int(result_list[i][1]) > int(result_list[i][4])):
        row.append(1)
    elif(int(result_list[i][1]) == int(result_list[i][4])):
        row.append(0)
    else:
        row.append(2)
    output.append(row)
    i += 1

dt_now = datetime.datetime.now().strftime('%Y%m%d')
file_name = 'fastRetailing_' + dt_now + '.csv'

with open(file_name,'w') as csv_file:
    fieldnames = ['newsDate','content','stockDate','start','end','flag']
    writer = csv.writer(csv_file)
    writer.writerow(fieldnames)
    writer.writerows(output)