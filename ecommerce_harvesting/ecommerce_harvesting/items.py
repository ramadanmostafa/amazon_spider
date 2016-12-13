# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Product(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    SiteId = scrapy.Field()
    product_DetailUrl = scrapy.Field()
    product_Rating = scrapy.Field()
    product_NumberOfReviews = scrapy.Field()

class ProductDetails(scrapy.Item):
    site_name = scrapy.Field()
    harvest_date = scrapy.Field()
    product_name = scrapy.Field()
    product_list_price = scrapy.Field()
    product_sale_price = scrapy.Field()
    product_online_price = scrapy.Field()
    product_shoppingcart_price = scrapy.Field()
    product_shipping_cost = scrapy.Field()
    product_url = scrapy.Field()
    manufacturer_sku = scrapy.Field()
    site_sku = scrapy.Field()
    product_rating = scrapy.Field()
    product_review_count = scrapy.Field()
    product_image_count = scrapy.Field()
    product_description = scrapy.Field()
    product_specifications = scrapy.Field()
    product_inStock_flag = scrapy.Field()
    product_upc = scrapy.Field()
    product_available = scrapy.Field()
    product_dimensions = scrapy.Field()
    product_shipping_dimensions = scrapy.Field()
    product_weight = scrapy.Field()
    seller_name = scrapy.Field()
    seller_url = scrapy.Field()
    product_screenshot_url = scrapy.Field()
    product_online_descriptor = scrapy.Field()
    product_color = scrapy.Field()
    product_shipping_weight = scrapy.Field()
    product_image_url = scrapy.Field()
    product_marketplace_price = scrapy.Field()

class WalmartProductDetails(scrapy.Item):
    """
    a class to define the crawled item attributes
    """
    product_name = scrapy.Field()
    product_url = scrapy.Field()
    manufacturer_sku = scrapy.Field()
    site_sku = scrapy.Field()
    product_manufacturer = scrapy.Field()
    product_image_count = scrapy.Field()
    product_image_url = scrapy.Field()
    product_description = scrapy.Field()
    product_specifications = scrapy.Field()
    product_inStock_flag = scrapy.Field()
    product_upc = scrapy.Field()
    product_available = scrapy.Field()
    seller_name = scrapy.Field()
    seller_url = scrapy.Field()
    product_onlinePrice = scrapy.Field()
    product_online_descriptor = scrapy.Field()
    product_color = scrapy.Field()

class WalmartSellersDetails(scrapy.Item):
    
    seller_name = scrapy.Field()
    seller_url = scrapy.Field()
    product_shoppingcartprice = scrapy.Field()
