# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import Product


class SearsSpiderSpider(scrapy.Spider):
    name = "sears_d"
    allowed_domains = ["sears.com"]
    start_urls = (
        "http://www.sears.com/service/search/v2/productSearch?catalogId=12605&keyword=south+shore+furniture+bed&pageNum=1",
        "http://www.sears.com/service/search/v2/productSearch?catalogId=12605&keyword=south+shore+furniture+headboard&pageNum=1",
    )

    def parse(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        if len(jsonresponse['data']['products']) > 0:
            for item_data in jsonresponse['data']['products']:
                myitem = Product()
                myitem['SiteId'] = "3"
                myitem['product_DetailUrl'] = item_data['url']
                myitem['product_Rating'] = item_data['rating']
                myitem['product_NumberOfReviews'] = item_data['reviewCount']
                yield myitem
            #next page
            tmp = response.url.split('=')
            next_url = ""
            for x in tmp[:-1]:
                next_url += x + '='
            next_url += str(int(tmp[-1]) + 1)
            yield scrapy.Request(next_url, callback = self.parse)
