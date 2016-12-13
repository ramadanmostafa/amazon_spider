# -*- coding: utf-8 -*-
import scrapy
from ..items import Product


class AmazonDSpider(scrapy.Spider):
    name = "amazon_d"
    allowed_domains = ["amazon.com"]
    start_urls = (
        'https://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias%3Dgarden&field-keywords=south+shore+furniture',
    )

    def __init__(self):
        self.total_products_num = 0

    def parse(self, response):
        if response.status == 301:
            url = response.headers['Location']
            yield scrapy.Request(url, callback = self.parse)
        else:
            num_items = len(response.xpath('//div/div[3]/div[1]/a/@href').extract())
            for i in range(num_items):
                product_url = response.xpath('//*[@id="result_' + str(i + self.total_products_num) + '"]/div/div/div/a/@href').extract_first()
                product_Rating = response.xpath('//*[@id="result_' + str(i + self.total_products_num) + '"]/div/div/span/span/a/i/span/text()').extract_first()
                if product_Rating is None:
                    product_Rating = ""
                else:
                    product_Rating = product_Rating.split(' ')[0]
                num_rating_tmp = response.xpath('//*[@id="result_' + str(i + self.total_products_num) + '"]/div/div/a/text()').extract()
                num_rating = ''
                if num_rating_tmp is not None:
                    for i in num_rating_tmp:
                        try:
                            x = int(i)
                            num_rating = i
                            break
                        except:
                            continue
                myitem = Product()
                myitem['SiteId'] = "4"
                myitem['product_DetailUrl'] = product_url
                myitem['product_Rating'] = product_Rating
                myitem['product_NumberOfReviews'] = num_rating
                yield myitem

            self.total_products_num += num_items
            #get next page url
            next_url = response.urljoin(response.xpath('//*[@id="pagnNextLink"]/@href').extract_first())
            if next_url is not None:
                yield scrapy.Request(next_url, callback = self.parse)
