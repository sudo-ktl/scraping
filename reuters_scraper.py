import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()
header = {'user-agent': ua.chrome}

src = 'https://jp.reuters.com/news/archive/LunchtimeComment?view=page&page=2&pageSize=10'

response = requests.get(src,headers=header)

soup = BeautifulSoup(response.text, 'html.parser')

elems = soup.find_all('div', class_ = 'story-content')

links = []

for elem in elems:
    links.append('https://jp.reuters.com/' + elem.find('a').attrs['href'])

# print(links)

for link in links:
    response = requests.get(link,headers=header)
    soup = BeautifulSoup(response.text,'html.parser')
    title = soup.find('h1', class_ = 'Headline-headline-2FXIq Headline-black-OogpV ArticleHeader-headline-NlAqj').contents[0]
    body = soup.find('p',class_ = 'Paragraph-paragraph-2Bgue ArticleBody-para-TD_9x')
    print(title)
    print(link)
    print(body.text if hasattr(body,"text") else '', end='\n\n\n\n')