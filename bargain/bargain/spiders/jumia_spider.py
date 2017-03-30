"""System crawlers are contained in this file."""
import scrapy
from bargain.items import JumiaItem


class JumiaSpider(scrapy.Spider):
    """Crawler for scraping jumia website."""
    name = 'jumia'

    start_urls = [
        'https://www.jumia.co.ke/mobile-phones/',
        'https://www.jumia.co.ke/computers/',
        'https://www.jumia.co.ke/video-audio/'
    ]

    custom_settings = {
        'ITEM_PIPELINES':
            {
                # 'bargain.pipelines.JumiaPipeline':700,
                # 'bargain.pipelines.NoramalizePipeline': 300,
                # 'scrapyelasticsearch.scrapyelasticsearch.ElasticSearchPipeline': 500
                # 'bargain.pipelines.JumiaOffCalcPipeline': 300,
                # 'bargain.pipelines.UpdatePipeline': 300
            }
    }

    def parse(self, response):
        item = JumiaItem()
        for product in response.css("div.sku"):
            item['name'] = ''.join(
                product.css("a.link h2.title span.name::text").extract())
            item['brand'] = ''.join(
                product.css("a.link h2.title span.brand::text").extract())
            item['product_url'] = ''.join(
                product.css("a::attr(href)").extract())
            item['product_image'] = ''.join(
                product.css("a.link \
                            div.image-wrapper img::attr(data-src)").extract())
            item['price'] = float(''.join(
                product.css("a.link \
                            span.price span::attr(data-price)").extract()[0]))
            item['product_discount'] = ''.join(
                product.css(".sale-flag-percent::text")
                .extract()).replace('-', '')
            item['store'] = 'jumia'
            yield item
        next_page = response.css(
            "li.item a::attr(href)"
        ).extract()[len(response.css("li.item a::attr(href)")) - 1]
        if next_page is not None:
            next_page = response.urljoin(next_page)
            print next_page
            yield scrapy.Request(next_page, callback=self.parse)
