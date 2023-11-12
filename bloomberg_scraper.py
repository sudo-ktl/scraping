import requests
from bs4 import BeautifulSoup
import datetime
import re
import csv

src_list = ['https://assets.wor.jp/rss/rdf/bloomberg/top.rdf','https://assets.wor.jp/rss/rdf/bloomberg/markets.rdf','https://assets.wor.jp/rss/rdf/bloomberg/overseas.rdf']
url_list = []

for src in src_list:
    response = requests.get(src)
    soup = BeautifulSoup(response.content, 'lxml')
    elems = soup.find_all("rdf:li")
    for elem in elems:
        url_list.append(elem.attrs['rdf:resource'])

url_set = set(url_list)
text_list = []

for url in url_set:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    article_body = soup.find('div', class_='body-copy')
    text_list.append(article_body.get_text().replace('\n',''))

dt_now = datetime.datetime.now().strftime('%Y%m%d')
file_name = 'bloomberg_' + dt_now + '.csv'

with open(file_name,'w') as csv_file:
    fieldnames = ['newsdate','content','tag']
    writer = csv.DictWriter(csv_file, fieldnames)
    writer.writeheader()
    for text in text_list:
        writer.writerow({'newsdate': dt_now, 'content': text, 'tag': 'bloomberg'})