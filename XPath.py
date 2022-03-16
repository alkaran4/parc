import requests
from lxml import html
import re
from pymongo import MongoClient


header = {'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
url = 'https://lenta.ru'

response = requests.get(url, headers=header)
dom = html.fromstring(response.text)

news_list = []
news = dom.xpath('//main//section//span[contains(@class, "card-mini__title")]')
for i in news:
    news_dict = {}

    news_dict['news_title'] = i.xpath('./text()')[0]

    if i.xpath('./../../@href')[0].startswith('/news'):
        news_dict['link'] = url + i.xpath('./../../@href')[0]
        news_dict['date'] = re.findall(r"\d{4}/\d\d/\d\d", i.xpath('./../../@href')[0])[0]
    elif i.xpath('./../../@href')[0].startswith('https'):
        news_dict['link'] = i.xpath('./../../@href')[0]
        news_dict['date'] = re.findall(r"\d\d-\d\d-\d{4}", i.xpath('./../../@href')[0])[0]

    news_dict['Источник'] = 'Лента'

    news_list.append(news_dict)

client = MongoClient('localhost', 27017)
db = client['data_base_2']
news_db = db.news

news_db.insert_many(news_list)