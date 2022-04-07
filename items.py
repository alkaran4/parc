# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StroydvorItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    link = scrapy.Field()
    photo = scrapy.Field()
    price = scrapy.Field()
    unit = scrapy.Field()
    cur = scrapy.Field()
