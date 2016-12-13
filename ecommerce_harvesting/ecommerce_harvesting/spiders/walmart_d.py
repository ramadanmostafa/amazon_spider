# -*- coding: utf-8 -*-
import scrapy
from ..items import Product


class WalmartDSpider(scrapy.Spider):
    name = "walmart_d"
    allowed_domains = ["walmart.com"]
    start_urls = (
            "https://www.walmart.com/search/?query=south%20shore%20dresser&cat_id=4044",
            "https://www.walmart.com/search/?query=south%20shore%20beds&cat_id=4044",
            "https://www.walmart.com/search/?query=south%20shore%20headboards&cat_id=4044",
            "https://www.walmart.com/search/?query=south%20shore%20night%20stand&cat_id=4044",
            "https://www.walmart.com/search/?query=south%20shore%20armoires&cat_id=4044",
            "https://www.walmart.com/search/?query=south%20shore%20bookcase&cat_id=4044",
            "https://www.walmart.com/search/?query=south%20shore%20desk&cat_id=4044",
            "https://www.walmart.com/search/?query=south%20shore%20tv%20stand&cat_id=4044",
            "https://www.walmart.com/search/?query=south%20shore%20baby%20dresser&cat_id=4044",
            "https://www.walmart.com/search/?query=south%20shore%20changing%20table&cat_id=4044",
            "https://www.walmart.com/search/?query=south%20shore%20kids%20dressers%20armoires&cat_id=4044",

    )

    def parse(self, response):
        num_items = len(response.xpath('//*[@id="tile-container"]/ul/li').extract())
        for i in range(num_items):
            product_url = response.xpath('//*[@id="tile-container"]/ul/li[' + str(i + 1) +']/div/a/@href').extract_first()
            product_url_colors = response.xpath('//*[@id="tile-container"]/ul/li[' + str(i + 1) +']/div/div/label/@data-product-url').extract()
            product_Rating = response.xpath('//*[@id="tile-container"]/ul/li[' + str(i + 1) +']/div/div/span/span/text()').extract_first()
            num_rating_tmp = response.xpath('//*[@id="tile-container"]/ul/li[' + str(i + 1) +']/div/div/span/span[2]/text()').extract_first()
            num_rating = ""
            if num_rating_tmp is not None:
                num_rating = num_rating_tmp.strip()[1:-1]
            product_url_colors.append(product_url)
            myitem = Product()
            myitem['SiteId'] = "1"
            myitem['product_DetailUrl'] = product_url_colors
            myitem['product_Rating'] = product_Rating
            myitem['product_NumberOfReviews'] = num_rating
            yield myitem
        #get next page url
        next_url = response.urljoin(response.xpath('//*[@id="paginator-container"]/div/a[2]/@href').extract_first())
        next_url2 = response.urljoin(response.xpath('//*[@id="paginator-container"]/div/a/@href').extract_first())
        if next_url is not None or next_url2 is not None:
            yield scrapy.Request(next_url, callback = self.parse)
            yield scrapy.Request(next_url2, callback = self.parse)
