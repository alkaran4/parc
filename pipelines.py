# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacansy_new


    def process_item(self, item, spider):
        collection = self.mongobase[spider.name]
        if spider.name == 'hhru':
            item['min'], item['max'], item['cur'] = self.procces_salary_hhru(item['salary'])
            item['name'] = item['name'][0]
        elif spider.name == 'sjru':
            item['min'], item['max'], item['cur'] = self.process_salary_sjru(item['salary'])
        del item['salary']
        collection.insert_one(item)
        return item


    def procces_salary_hhru(self, salary):
        if salary[0] == 'з/п не указана':
            salary_min = None
            salary_max = None
            cur = None
        elif salary[0] == 'от ' and salary[2] == ' до ':
            salary_min = salary[1].replace('\xa0', ' ')
            salary_max = salary[3].replace('\xa0', ' ')
            cur = salary[-2]
        elif salary[0] == 'от ':
            salary_min = salary[1].replace('\xa0', ' ')
            salary_max = None
            cur = salary[-2]
        elif salary[0] == 'до ':
            salary_min = None
            salary_max = salary[1].replace('\xa0', ' ')
            cur = salary[-2]
        return salary_min, salary_max, cur


    def process_salary_sjru(self, salary):
        # if salary[0].startswith('от'):
        #     salary_min = salary[1] + salary[2]
        #     salary_max = None
        #     cur = salary[3]
        # elif salary[0].startswith('до'):
        #     salary_min = None
        #     salary_max = salary[1] + salary[2]
        #     cur = salary[3]
        # elif salary[2] == '—':
        #     salary_min = salary[0] + salary[1]
        #     salary_max = salary[3] + salary[4]
        #     cur = salary[5]
        return salary_min, salary_max, cur