# -*- coding: utf-8 -*-
import scrapy
from ..items import WalmartSellersDetails
from selenium import webdriver
import lxml.html
import time


class WalmartSellersSpider(scrapy.Spider):
    """
    scrapy spider to crawl single walmart sellers page
    input:inputSellersUrl
    you can run it using something like that
    scrapy crawl walmart_sellers -o output_file.json -a category='product/3921879/sellers'
    category attribute will be concatenated to 'https://www.walmart.com/' to build the start_urls list
    """
    name = "walmart_sellers"
    allowed_domains = ["walmart.com"]

    def __init__(self, category='', domain=None, *args, **kwargs):
        """walmart spider constructor, build the start_urls list from category attribute"""
        super(WalmartSellersSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://www.walmart.com/%s' % category]

    def parse(self, response):
        """
        in this function, the spider parse the crawled sellers page and build the walmart sellers item
        it also uses selenium to simulate the add to cart action, sleep for 5 seconds to make sure the
        item is added to the cart, go to cart page, get the total price, press remove button to empty
        the cart, then close the selenium driver.
        """
        #init some useful xpath variables and urls
        xpath_price = "/html/body/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[4]/span[2]/span/span[%s]/text()"
        xpath_seller_name = '/html/body/div/div/div/div/div[2]/div/div/div[4]/div/div[3]/div/div[1]/div[1]/a/text()'
        xpath_seller_url = '/html/body/div/div/div/div/div[2]/div/div/div[4]/div/div[3]/div/div[1]/div[1]/a/@href'
        xpath_remove_button = '/html/body/div/div/div[1]/div[1]/div/div/div[1]/div[1]/div/div[3]/div[1]/div/div[2]/div/div/div/div/div[6]/div/div/button[2]'
        xpath_add_to_cart_button = '/html/body/div/div/div/div/div[2]/div/div/div[4]/div[%s]/div[3]/div/div[2]/div[1]/div[2]/div/button'
        cart_url = "https://www.walmart.com/cart"
        ##################################################################################
        #init item
        walmart_sellers = WalmartSellersDetails()
        walmart_sellers["seller_name"] = ""
        walmart_sellers["seller_url"] = ""
        walmart_sellers["product_shoppingcartprice"] = []
        ###################################################
        walmart_sellers["seller_name"] = response.xpath(xpath_seller_name).extract()
        walmart_sellers["seller_url"] = response.xpath(xpath_seller_url).extract()
        #get product_shoppingcart_price
        num_sellers = len(walmart_sellers["seller_url"])
        for i in range(num_sellers):
            driver = webdriver.Chrome()
            driver.get(response.url)
            driver.find_element_by_xpath(xpath_add_to_cart_button % str(i + 2)).click()
            time.sleep(5) # delays for 5 seconds
            driver.get(cart_url)
            dom = lxml.html.fromstring(driver.page_source)
            driver.find_element_by_xpath(xpath_remove_button).click()
            driver.close()
            price = dom.xpath(xpath_price % '2')[0] + dom.xpath(xpath_price % '3')[0] + dom.xpath(xpath_price % '4')[0] + dom.xpath(xpath_price % '5')[0]
            walmart_sellers["product_shoppingcartprice"].append(price)
        yield walmart_sellers
