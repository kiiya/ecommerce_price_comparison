# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JumiaItem(scrapy.Item):
    name = scrapy.Field()
    brand = scrapy.Field()
    product_url = scrapy.Field()
    product_image = scrapy.Field()
    price = scrapy.Field()
    product_discount = scrapy.Field()
    store = scrapy.Field()


class KilimallItem(scrapy.Item):
    name = scrapy.Field()
    brand = scrapy.Field()
    product_url = scrapy.Field()
    product_image = scrapy.Field()
    price = scrapy.Field()
    product_discount = scrapy.Field()
    store = scrapy.Field()
