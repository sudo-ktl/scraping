import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import csv

ua = UserAgent()
header = {'user-agent': ua.chrome}

src = 'https://www.fidelity.jp/market-info/market-report/?p=1&c=100'

response = requests.get(src,headers=header)

soup = BeautifulSoup(response.text, 'html.parser')

elems = soup.find_all('li', class_ = 'list-item external-link')

article_lists = []

# スクレイピングの時点でかなり重複してしまうので、重複チェックしながらリストに格納する
for elem in elems:
    # article_listsの中身が空の最初だけ
    if(len(article_lists) == 0):
        article_lists.append({'date':str(elem.find('span').contents[0]),'title':str(elem.find('a').contents[0]),'url':elem.find('a').attrs['href']})
    else:
        i = 0
        for article in article_lists:
            if(article.get('title') == str(elem.find('a').contents[0])):
                continue
            else:
                i = i + 1
        # 全てチェックして重複がなければiとarticle_listsの要素数は同じなので
        if(i == len(article_lists)):
            article_lists.append({'date':str(elem.find('span').contents[0]),'title':str(elem.find('a').contents[0]),'url':elem.find('a').attrs['href']})

with open('fidelity-market-info.csv','w') as csv_file:
    fieldnames = ['date','title','url']
    writer = csv.DictWriter(csv_file, fieldnames)
    writer.writeheader()
    for article in article_lists:
        writer.writerow({'date': article.get('date'), 'title': article.get('title'), 'url': article.get('url')})