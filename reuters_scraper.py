import requests
from bs4 import BeautifulSoup
import datetime
import re
import csv

src = 'https://jp.reuters.com/markets/'

response = requests.get(src)

soup = BeautifulSoup(response.content, 'lxml')

links = []

# 対象ページ最新ニュースの見出し
targetUrl = ['/business/','/markets/','/world/','/economy/','/opinion/','/life/']
for url in targetUrl:
    elems = soup.find_all(attrs={'data-testid':'Heading'},href=re.compile(url))
    for elem in elems:
        links.append('https://jp.reuters.com' + elem.attrs['href'])

# 対象ページ中の日本株〜投資信託の見出し
elems = soup.find_all('h3')
articles = elems[4:-3]
for article in articles:
    a = article.find('a')
    # print(a.contents[0])
    # print('https://jp.reuters.com' + a.attrs['href'])
    links.append('https://jp.reuters.com' + a.attrs['href'])

article_set = set(links)

# 各見出しの記事本文を取得
text_list = []
for article in article_set:
    response = requests.get(article)
    soup = BeautifulSoup(response.content, 'lxml')
    article_body = soup.find('div', class_='article-body__content__17Yit')
    text_list.append(article_body.get_text())

dt_now = datetime.datetime.now().strftime('%Y%m%d')
file_name = 'reuters_' + dt_now + '.csv'

with open(file_name,'w') as csv_file:
    fieldnames = ['newsdate','content','tag']
    writer = csv.DictWriter(csv_file, fieldnames)
    writer.writeheader()
    for text in text_list:
        writer.writerow({'newsdate': dt_now, 'content': text, 'tag': 'reuters'})