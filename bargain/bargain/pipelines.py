# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from __future__ import division
import pymongo
from scrapy.exceptions import DropItem
import string
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from pyvirtualdisplay import Display
from selenium.webdriver.chrome.options import Options


class JumiaPipeline(object):
    """Write crawl data to mongodb."""
    collection_name = 'jumia'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        """Mongodb connection setup."""
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'bargain')
        )

    def open_spider(self, spider):
        """Start up."""
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        """Tear down."""
        self.client.close()

    def process_item(self, item, spider):
        """Save to db."""
        self.db[self.collection_name].insert(dict(item))
        return item


class NoramalizePipeline(object):
    def process_item(self, item, spider):
        if item['name']:
            item['name'] = item['name'].lower()
            return item
        else:
            raise DropItem("Missing name in %s" % item)


class FixKilimallBrand(object):
    def process_item(self, item, spider):
        if item['brand']:
            details = item['brand']
            r = re.compile(".*Brand:")
            new_list = filter(r.match, details)
            brand = ''.join(new_list).replace("Brand: ", "")
            item['brand'] = brand
            if item['brand'] == "":
                item['brand'] = 'Generic'
            return item
        else:
            raise DropItem("Error fixing %s brand" % item)


class JumiaOffCalcPipeline(object):
    def process_item(self, item, spider):
        if item['product_discount']:
            item['product_discount'] = item['product_discount'].replace('-',
                                                                        '')
            item['product_discount'] = item['product_discount'] + ' OFF'
            return item
        else:
            raise DropItem("Missing product discount in %s" % item)


class JumiaAffiliatePipeline(object):
    def process_item(self, item, spider):
        if item['product_url']:

            options = webdriver.ChromeOptions()
            options.add_argument("user-data-dir=/home/kiiya/.config/google-chrome/Default")
            browser = webdriver.Chrome(chrome_options=options)
            browser.get('https://www.jumia.com/affiliate-program/sign-in.php')

            # username_input = browser.find_element_by_id('username')
            # pass_input = browser.find_element_by_id('password')

            # username_input.clear()
            # username_input.send_keys('kiiyaerick@gmail.com')

            # pass_input.clear()
            # pass_input.send_keys('16221992Jumia')

            browser.find_element_by_xpath("//*[@id='sbmt-btn']").click();
            browser.get('https://www.jumia.com/affiliate-program/home.php?page=deeplink_generator')

            # Get dropdown
            offer_select = Select(browser.find_element_by_id('offer'))
            offer_select.select_by_visible_text('Jumia Kenya')

            # get url field
            url_input = browser.find_element_by_id('url')
            url_input.clear()
            url_input.send_keys('https://www.jumia.co.ke/my-leadder-ld40t01-40-led-tv-black-274352.html')

            # Get final url
            final_url_element = browser.find_element_by_id('final-url')
            url = final_url_element.get_attribute("value")
            item['product_url'] = url
            return item
        else:
            raise DropItem("I cannot find that field in item %s" % item)

