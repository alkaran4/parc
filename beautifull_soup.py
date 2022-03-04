from bs4 import BeautifulSoup as BS
import requests
import pandas as pd
import json


url = 'https://russia.superjob.ru'
suffix = '/vacancy/search'
param = {'keywords': 'Python', 'page': 1}
header = {
    'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.174 YaBrowser/22.1.3.850 Yowser/2.5 Safari/537.36'}

vacanc_list = []
response = requests.get(url + suffix, params=param, headers=header)
dom = BS(response.text, 'html.parser')
dom_page = dom.find_all('a', {'rel': 'next'})


def parser_job():
    for i in dom_sort:
        vacancy_data = {}

        link = url + i.find('a').get('href')
        vacanc = i.find('span').text
        salary = i.find('span', {'class': '_1OuF_ _1qw9T f-test-text-company-item-salary'}).find('span')
        salary = salary.text.replace('\xa0', ' ').split(' ')

        vacancy_data['Вакансия'] = vacanc
        vacancy_data['Ссылка'] = link

        if salary[0].startswith('от'):
            vacancy_data['От'] = salary[1] + salary[2]
            vacancy_data['До'] = 'Nan'
            vacancy_data['Валюта'] = salary[3]
        elif salary[0].startswith('до'):
            vacancy_data['От'] = 'Nan'
            vacancy_data['До'] = salary[1] + salary[2]
            vacancy_data['Валюта'] = salary[3]
        elif salary[0].lower() == 'по':
            pass
        elif salary[2] == '—':
            vacancy_data['От'] = salary[0] + salary[1]
            vacancy_data['До'] = salary[3] + salary[4]
            vacancy_data['Валюта'] = salary[5]

        vacanc_list.append(vacancy_data)


while dom_page:
    response = requests.get(url + suffix, params=param, headers=header)
    dom = BS(response.text, 'html.parser')
    dom_sort = dom.find_all('div', {'class': 'jNMYr GPKTZ _1tH7S'})

    parser_job()

    print(param['page'])

    param = {'keywords': 'Python', 'page': param['page'] + 1}
    dom_page = dom.find_all('a', {'rel': 'next'})

Data = pd.DataFrame(vacanc_list)


with open('super_job_parser.json', 'w') as f:
    json.dump(vacanc_list, f, indent=3)
