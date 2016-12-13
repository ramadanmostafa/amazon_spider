# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import WalmartProductDetails


class WalmartDetailSpider(scrapy.Spider):
    """
    scrapy spider to crawl single walmart detail page using walmart products api
    input:inputDetailUrl
    you can run it using something like that
    scrapy crawl walmart_detail -o output_file.json -a category='product/api/12480393?selected=true'
    category attribute will be concatenated to 'https://www.walmart.com/' to build the start_urls list
    """
    name = "walmart_detail"
    allowed_domains = ["walmart.com"]

    def __init__(self, category='', domain=None, *args, **kwargs):
        """walmart spider constructor, build the start_urls list from category attribute"""
        super(WalmartDetailSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://www.walmart.com/%s' % category]

    def parse(self, response):
        """
        in this function, the spider parse the crawled pages and build the walmart item
        """
        walmart_item = WalmartProductDetails()
        #init walmart_item
        walmart_item['product_name'] = ""
        walmart_item['product_url'] = ""
        walmart_item['manufacturer_sku'] = ""
        walmart_item['product_image_url'] = ""
        walmart_item['product_description'] = ""
        walmart_item['product_image_count'] = ""
        walmart_item['product_color'] = ""
        walmart_item['site_sku'] = ""
        walmart_item['product_manufacturer'] = ""
        walmart_item['product_inStock_flag'] = ""
        walmart_item['product_upc'] = ""
        walmart_item['product_available'] = ""
        walmart_item['seller_name'] = ""
        walmart_item['seller_url'] = ""
        walmart_item['product_onlinePrice'] = ""
        walmart_item['product_specifications'] = ""
        walmart_item['product_online_descriptor'] = ""
        ######################################################################################
        jsonresponse = json.loads(response.body_as_unicode())
        if "product" in jsonresponse:
            if "productName" in jsonresponse["product"]:
                walmart_item['product_name'] = jsonresponse["product"]["productName"]
            if "canonicalUrl" in jsonresponse["product"]:
                walmart_item['product_url'] = jsonresponse['product']['canonicalUrl']
            if "manufacturerProductId" in jsonresponse["product"]:
                walmart_item['manufacturer_sku'] = jsonresponse['product']['manufacturerProductId']
            if "primaryImageUrl" in jsonresponse["product"]:
                walmart_item['product_image_url'] = jsonresponse["product"]["primaryImageUrl"]
            if "longDescription" in jsonresponse["product"]:
                walmart_item['product_description'] = jsonresponse["product"]["longDescription"]
            if "imageAssets" in jsonresponse["product"]:
                walmart_item['product_image_count'] = len(jsonresponse["product"]["imageAssets"])
            if "variantInformation" in jsonresponse["product"] and "variantTypes" in jsonresponse["product"]["variantInformation"]:
                walmart_item['product_color'] = self.get_color(jsonresponse["product"]["variantInformation"]["variantTypes"])
        if "analyticsData" in jsonresponse:
            if "productId" in jsonresponse['analyticsData']:
                walmart_item['site_sku'] = jsonresponse['analyticsData']['productId']
            if "brand" in jsonresponse['analyticsData']:
                walmart_item['product_manufacturer'] = jsonresponse['analyticsData']['brand']
            if "inStock" in jsonresponse['analyticsData']:
                walmart_item['product_inStock_flag'] = jsonresponse["analyticsData"]["inStock"]
            if "upc" in jsonresponse['analyticsData']:
                walmart_item['product_upc'] = jsonresponse["analyticsData"]["upc"]
            if "productSellersMap" in jsonresponse['analyticsData']:
                sellers = jsonresponse["analyticsData"]["productSellersMap"]
                walmart_item['product_available'] = self.get_product_available_sellers(sellers)
                walmart_item['seller_name'] = self.get_sellers_names(sellers)
                #walmart_item['seller_url'] = self.get_sellers_urls(sellers)
                walmart_item['product_onlinePrice'] = self.get_product_onlinePrices(sellers)
            ##########################################################################################################
        if "idml" in jsonresponse and "specifications" in jsonresponse["idml"] and "specAttributes" in jsonresponse["idml"]["specifications"]:
            walmart_item['product_specifications'] = self.get_specifications(jsonresponse["idml"]["specifications"]["specAttributes"])

        yield walmart_item

    def get_specifications(self, specAttributes):
        """
        build a dictionary of displayName:displayValue for each item in specAttributes list
        return type: string representation of the result dictionary
        """
        result = {}
        for attribute in specAttributes:
            result[attribute["displayName"]] = attribute["displayValue"]

        return str(result)

    def get_color(self, variantTypes):
        """
        return a list of available colors for the crawled item
        """
        result = []
        for item_type in variantTypes:
            result.append(item_type["selectedValue"])

        return result

    def get_product_available_sellers(self, sellers):
        """
        return a list of available sellers for the crawled item
        """
        result = []
        for seller in sellers:
            result.append(seller["isAvail"])
        return result

    def get_sellers_names(self, sellers):
        """
        return a list of sellers names and offerId for the crawled item
        """
        result = []
        for seller in sellers:
            result.append(seller["sellerName"] + "_" + seller["offerId"])
        return result

    def get_sellers_urls(self, sellers):
        """
        return a list of sellers URLs for the crawled item
        """
        result = []
        for seller in sellers:
            result.append(seller["sellerId"])
        return result

    def get_product_onlinePrices(self, sellers):
        """
        return a list of available prices for the crawled item
        """
        result = []
        for seller in sellers:
            result.append(seller["price"])
        return result
