"""Kilimall spider."""
import scrapy


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
                'scrapyelasticsearch.scrapyelasticsearch.ElasticSearchPipeline': 500
            }
    }

    def parse(self, response):
        for item in response.css("li.item"):
            yield {
                'name': ''.join(item.css("div.goods-content h3.goods-name a::text").extract()),
                'product_image': ''.join(item.css("div.goods-content div.goods-pic a img::attr(data-src)").extract()),
                'product_url': ''.join(item.css("div.goods-content h3.goods-name a::attr(href)").extract()),
                'price': ''.join(item.css("div.goods-content div.goods-info div.goods-price em.sale-price::text").extract()),
                'product_discount': ''.join(item.css("div.goods-content div.goods-info div.goods-discount::text").extract()),
                'store': 'kilimall'
            }

        next_page = ''.join(response.xpath("//*[text()='Next']/parent::*/@href").extract())
        if next_page is not None:
            next_page = response.urljoin(next_page)
            print next_page
            yield scrapy.Request(next_page, callback=self.parse)

