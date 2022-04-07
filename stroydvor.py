import scrapy
from scrapy.http import HtmlResponse
from Stroydvor.items import StroydvorItem
from scrapy.loader import ItemLoader



class StroydvorSpider(scrapy.Spider):
    name = 'stroydvor'
    allowed_domains = ['sdvor.com']
    start_urls = ['https://www.sdvor.com/moscow/search/плитка']


    def parse(self, response: HtmlResponse):
        links = response.xpath('//sd-product-grid-item/@href').extract()
        for link in links:
            yield response.follow(link, callback=self.parse_ads)


    def parse_ads(self, response: HtmlResponse):
        name = response.xpath('//sd-product-intro//h1/@text()').getall()
        link = response.url
        photo = response.xpath('//sd-product-images//img/@src()').getall()
        price = response.xpath('//sd-available-price//span/@text()').getall()
        unit = response.xpath('//sd-product-unit//option/@text()').getall()
        item = StroydvorItem(name=name, link=link, photo=photo, price=price, unit=unit)
        yield item
