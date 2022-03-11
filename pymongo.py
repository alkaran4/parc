import json
import pymongo
from pprint import pprint
from pymongo.errors import *

client = pymongo.MongoClient('127.0.0.1', 27017)

db = client['db01']
vacanc = db.vacanc

with open('super_job_parser.json', 'r', encoding='utf-8') as g:
    base = json.load(g)

for i in base:
    vacanc.insert_one(i)

new_data = (
    {'Вакансия': 'PHP Backend разработчик (Middle/Senior)', 'Ссылка': 'https://russia.superjob.ru/vakansii/programmist-matematik-4172263.html'},
    {'Вакансия': 'PHP Backend разработчик (Middle/Senior)', 'Ссылка': 'https://russia.superjob.ru/vakansii/php-backend-razrabotchik-41737371.html'},
    {'Вакансия': 'PHP Backend разработчик (Middle/Senior)', 'Ссылка': 'https://russia.superjob.ru/vakansii/programmist-matematik-417226.html'})

def add_vacanc(data_base, new_d):
    vacanc_list = []
    for i in data_base.find({}):
        vacanc_list.append(i)
    for a in new_d:
        for i in range(len(vacanc_list)):
            if vacanc_list[i]['Ссылка'] == a['Ссылка']:
                print("Вакансия уже есть в базе данных")
                break
            elif i == len(vacanc_list)-1:
                data_base.insert_one(a)
                print('Вакансия добавлена')


def salary_find(size_of):
    for i in vacanc.find({ '$or': [ {'От': {'$gt' : str(size_of)} }, {'До' : { '$gt' : str(size_of)} } ] } ):
        print(i)

add_vacanc(vacanc, new_data)

salary_find(1000)