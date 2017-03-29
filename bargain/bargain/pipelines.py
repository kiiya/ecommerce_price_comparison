
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
            item['product_discount'] = item['product_discount'].replace('-', '')
            item['product_discount'] = item['product_discount'] + ' OFF'
            return item
        else:
            raise DropItem("Missing product discount in %s" % item)


class KilimallPipeline(object):
    """Write crawl data to mongodb."""
    collection_name = 'kilimall'

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
        self.db[self.collection_name].insert(dict(item))
        return item


class UpdatePipeline():
    """Write crawl data to mongodb."""
    collection_name = 'update_crawl'

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
        # Select database based on running spider and perform comparison
        return item
