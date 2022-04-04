import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['zarplata.ru']
    start_urls = ['https://ekb.zarplata.ru/vacancy?q=python']


    def parse(self, response:HtmlResponse):
        next_page = response.xpath('//a[contains(@class, "next")]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[contains(@class, 'vacancy-title')//@href]").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)


    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath('//h1[contains(@class, "header medium header")]/text()').getall()
        salary = response.xpath('//div[contains(@class, "salary")]/text()').getall()
        link = response.url
        item = JobparserItem(name=name, salary=salary, link=link)
        yield item
