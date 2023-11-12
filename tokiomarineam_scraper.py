import requests
from bs4 import BeautifulSoup
# from fake_useragent import UserAgent
import csv
import re

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
header = {'user-agent': user_agent}

src = 'https://www.tokiomarineam.co.jp/market/market_report/2023/index.html'

response = requests.get(src,headers=header)

soup = BeautifulSoup(response.content, 'html.parser')

print(soup)

# 2023年から2020年の各ページのURLを取得
links = []
elem = soup.find(id='news_past')
elems = elem.find_all(href=re.compile('/market/market_report/'))
for elem in elems:
    links.append('https://www.tokiomarineam.co.jp' + elem.attrs['href'])

result_list = []
# 各年のページをスクレイピングしていく
for link in links:
    response = requests.get(link, headers=header)
    soup = BeautifulSoup(response.content, 'html.parser')
    elem = soup.find(id='news')
    dates = elem.find_all('dt')
    # 年月日の表示形式を変更してリストに格納
    dates_list = []
    for date in dates:
        day = str(date.contents[0])
        dates_list.append(day.replace('年','/').replace('月', '/').replace('日', ''))
    # 記事タイトルとurl情報を取得
    title_and_urls = elem.find_all(href=re.compile('/pdf/web/viewer.html\?file=/market/market_report/'))
    # タイトルとurlを格納した辞書のリスト
    article_list = []
    for title_and_url in title_and_urls:
        article_list.append({'title': str(title_and_url.find('span').contents[0]), 'url': 'https://www.tokiomarineam.co.jp' + title_and_url.attrs['href']})
    #  タイトルとurl情報を格納した辞書のリストに対応する日付を追加した後にresultに入れる
    i = 0
    for article in article_list:
        article['date'] = dates_list[i]
        i = i + 1    
        result_list.append(article)

with open('tokiomarineam.csv','w') as csv_file:
    fieldnames = ['date','title','url']
    writer = csv.DictWriter(csv_file, fieldnames)
    writer.writeheader()
    for result in result_list:
        writer.writerow({'date': result.get('date'), 'title': result.get('title'), 'url': result.get('url')})