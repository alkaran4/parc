import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = [
        'https://ekaterinburg.hh.ru/search/vacancy?area=3&fromSearchLine=true&text=python',
        'https://ekaterinburg.hh.ru/search/vacancy?area=1261&search_field=name&search_field=company_name&search_field=description&text=python']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@data-qa="pager-next"]/@href').get() # сохраняем в переменую next_page результат работы response, вызываем у него метод css, куда указываем праметры для перелистывания страниц
        if next_page:
            yield response.follow(next_page, callback=self.parse) # разделяем response на два потока: первый идет дальше по сатй и собирает даные, второй их обрабатывает
        links = response.xpath('//a[@data-qa="vacancy-serp__vacancy-title"]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)


    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath('//h1//text()').getall()
        salary = response.xpath('//div[@data-qa="vacancy-salary"]//text()').getall()
        link = response.url
        item = JobparserItem(name=name, salary=salary, link=link)
        yield item





