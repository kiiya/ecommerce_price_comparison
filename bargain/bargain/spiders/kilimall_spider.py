"""Kilimall spider."""
import scrapy
import re
from bargain.items import KilimallItem


class KiliMallSpider(scrapy.Spider):
    """Spider entry point."""
    name = 'kilimall'

    start_urls = [
        'http://www.kilimall.co.ke/mobile-phones/'
    ]

    custom_settings = {
        'ITEM_PIPELINES':
            {
                # 'bargain.pipelines.KilimallPipeline':700,
                # 'bargain.pipelines.NoramalizePipeline': 300
                # 'bargain.pipelines.ConvertToInt': 300
                # 'scrapyelasticsearch.scrapyelasticsearch.ElasticSearchPipeline': 500
            }
    }

    def parse_brand(self, response, selector):
        for item in selector:


    def parse(self, response):
        item = KilimallItem()
        for prod in response.css("li.item"):
            item['name'] = ''.join(prod.css("div.goods-content h3.goods-name a::text").extract())
            item['brand'] = self.parse_brand(response, prod.css("div.goods-content h3.goods-name a::attr(href)"))
            item['product_url'] = ''.join(prod.css("div.goods-content h3.goods-name a::attr(href)").extract())
            item['product_image'] = ''.join(prod.css("div.goods-content div.goods-pic a img::attr(data-src)").extract())
            item['price'] = float(''.join(prod.css("div.goods-content div.goods-info div.goods-price em.sale-price::text").extract()).replace(" ", "").replace(",","").replace("KSh",""))
            item['product_discount'] = ''.join(prod.css("div.goods-content div.goods-info div.goods-discount::text").extract()).replace('OFF','')
            item['store'] = 'kilimall'
            yield item

        next_page = ''.join(response.xpath("//*[text()='Next']/parent::*/@href").extract())
        if next_page is not None:
            next_page = response.urljoin(next_page)
            print next_page
            yield scrapy.Request(next_page, callback=self.parse)
