# -*- coding: utf-8 -*-
import scrapy
from ..items import Product
import json


class HayneedleTSpider(scrapy.Spider):
    name = "hayneedle_d"
    allowed_domains = ["hayneedle.com"]
    start_urls = (
        'http://search.hayneedle.com/search/index.cfm?categoryId=0&selectedFacets=Brand%7CSouth%2520Shore~%5E&page=1&sortBy=preferred&checkCache=true&pageType=SEARCH&view=48&Ntt=south%20shore',
    )

    def parse(self, response):
        jsonresponse = json.loads(response.xpath('//*[@id="main_content_inner_div"]/script[2]/text()').extract_first().strip()[21:-1])
        if len(jsonresponse['products']) > 0:
            for item_data in jsonresponse['products']:
                myitem = Product()
                myitem['SiteId'] = "2"
                myitem['product_DetailUrl'] = item_data['url']
                myitem['product_Rating'] = item_data["reviews"]["reviewAverage"]
                myitem['product_NumberOfReviews'] = item_data["reviews"]['reviewCount']
                yield myitem
            #next page
            for next_url in response.xpath('//*[@id="main_content_inner_div"]/div[1]/div/div[2]/div/div[2]/div[3]/div[1]/a/@href').extract():
                yield scrapy.Request(next_url, callback = self.parse)
