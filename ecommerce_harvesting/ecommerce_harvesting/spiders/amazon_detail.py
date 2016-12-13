# -*- coding: utf-8 -*-
import scrapy
from ..items import ProductDetails
from datetime import datetime
from w3lib.html import remove_tags
import json


class AmazonDetailSpider(scrapy.Spider):
    name = "amazon_detail"
    allowed_domains = ["amazon.com"]

    def __init__(self, category='', domain=None, *args, **kwargs):
        super(AmazonDetailSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://www.amazon.com/%s' % category]

    def get_specifications(self, response):
        keys1 = map(unicode.strip, response.xpath('//*[@id="productDetails_techSpec_section_1"]/tr/th/text()').extract())
        keys2 = map(unicode.strip, response.xpath('//*[@id="productDetails_detailBullets_sections1"]/tr/th/text()').extract())
        values1 = map(unicode.strip, response.xpath('//*[@id="productDetails_techSpec_section_1"]/tr/td/text()').extract())
        values2 = map(unicode.strip, map(remove_tags, response.xpath('//*[@id="productDetails_detailBullets_sections1"]/tr/td').extract()))
        for i in range(len(values2)):
            if len(values2[i]) > 1500:
                tmp =  map(unicode.strip, response.xpath('//*[@id="productDetails_detailBullets_sections1"]/tr[' + str(i + 1) + ']/td/text()').extract())
                values2[i] = filter(None, tmp)[0]

        result = {}
        for i in range(len(keys1)):
            result[keys1[i]] = values1[i]
        for i in range(len(keys2)):
            result[keys2[i]] = values2[i]

        return result

    def get_image_url(self, response):
        target_script = ""
        for script in response.xpath('//*[@id="dp-container"]/script/text()').extract():
            if 'data["colorImages"] = ' in script:
                target_script = script
                break

        index1 = target_script.index('data["colorImages"] = ') + 22
        index2 = target_script[index1:].index(';') + index1
        first_key = target_script[index1 + 2: index1 + target_script[index1:].index(':') - 1]
        jsonresponse = json.loads(target_script[index1:index2])
        result = jsonresponse[first_key][0]['large']
        return result

    def parse(self, response):
        if response.status == 301:
            url = response.headers['Location']
            yield scrapy.Request(url, callback = self.parse)
        else:
            #navigation colors
            colors_url = response.xpath('//*[@id="variation_color_name"]/ul/li/@data-dp-url').extract()
            for color_url in colors_url:
                if color_url != '':
                    yield scrapy.Request(response.urljoin(color_url), callback = self.parse)
            ##################################################################
            #parse item
            specification = self.get_specifications(response)
            amazon_item = ProductDetails()
            amazon_item["site_name"] = "amazon"
            amazon_item["harvest_date"] = str(datetime.now())
            amazon_item["product_name"] = response.xpath('//*[@id="productTitle"]/text()').extract_first().strip()
            amazon_item["product_list_price"] = response.xpath('//*[@id="price"]/table/tr[1]/td[2]/span/text()').extract_first()
            amazon_item["product_sale_price"] = ""
            amazon_item["product_online_price"] = response.xpath('//*[@id="price"]/table/tr[2]/td[2]/span/text()').extract_first()

            amazon_item["product_url"] = response.url
            #
            amazon_item["manufacturer_sku"] = ""
            if "Item model number" in specification:
                amazon_item["manufacturer_sku"] = specification["Item model number"]

            #ASIN
            amazon_item["site_sku"] = ""
            if "ASIN" in specification:
                amazon_item["site_sku"] = specification["ASIN"]
            #

            amazon_item["product_description"] =  response.xpath('//*[@id="productDescription"]/p/text()').extract_first().strip()
            amazon_item["product_specifications"] = str(specification)
            amazon_item["product_inStock_flag"] = response.xpath('//*[@id="availability"]/span/text()').extract_first().strip()
            #UPC
            amazon_item["product_upc"] = ""
            if "UPC" in specification:
                amazon_item["product_upc"] = specification["UPC"]
            #
            amazon_item["product_available"] = None
            #Product Dimensions
            amazon_item["product_dimensions"] = ""
            if "Product Dimensions" in specification:
                amazon_item["product_dimensions"] = specification["Product Dimensions"]
            #
            amazon_item["product_shipping_dimensions"] = ""
            #Item Weight
            amazon_item["product_weight"] = ""
            if "Item Weight" in specification:
                amazon_item["product_weight"] = specification["Item Weight"]

            amazon_item["product_shipping_weight"] = ""
            if "Shipping Weight" in specification:
                amazon_item["product_shipping_weight"] = specification["Shipping Weight"]


            amazon_item["product_online_descriptor"] = ""
            amazon_item["product_color"] = response.xpath('//*[@id="prodDetails"]/span/strong/text()').extract_first()
            ################################################################
            amazon_item["product_rating"] = response.xpath('//*[@id="reviewStarsLinkedCustomerReviews"]/i/span/text()').extract_first()
            amazon_item["product_review_count"] = response.xpath('//*[@id="acrCustomerReviewText"]/text()').extract_first()
            amazon_item["product_image_url"] = self.get_image_url(response)
            amazon_item["product_image_count"] = len(response.xpath('//*[@id="altImages"]/ul/li').extract())
            ####################################################################
            amazon_item["product_shoppingcart_price"] = ""
            amazon_item["product_shipping_cost"] = ""
            amazon_item["seller_name"] = ""
            amazon_item["seller_url"] = ""
            amazon_item["product_screenshot_url"] = ""
            amazon_item["product_marketplace_price"] = ""
            ##################################################################
            #navigation sellers page
            #response.xpath('//*[@id="olp_feature_div"]/div/div[1]/span[1]/a/@href').extract_first()
            sellers_page_url = response.xpath('//*[@id="olp_feature_div"]/div/span/a/@href').extract_first()
            if sellers_page_url is None:
                sellers_page_url = response.xpath('//*[@id="olp_feature_div"]/div/div[1]/span[1]/a/@href').extract_first()
            print "sellers_page_url ", sellers_page_url
            if sellers_page_url == None:
                yield amazon_item
            else:
                yield scrapy.Request(response.urljoin(sellers_page_url), meta={'item':amazon_item}, callback = self.parse_sellers_page)

    def get_product_shoppingcart_price(self, page_url, item_index):
        #//*[@id="olpOfferList"]/div/div/div[2]
        #//*[@id="olpOfferList"]/div/div/div[2]/div[5]/div/form
        #response.xpath('//*[@id="olpOfferList"]/div/div/div/div[5]/div/form/span/span/span/input')
        from selenium import webdriver
        import lxml.html
        driver = webdriver.Chrome()
        driver.get(page_url)
        #driver.find_element_by_xpath('//*[@id="a-autoid-' + str(item_index + 4) + '"]/span/input').click()
        driver.find_element_by_xpath('//*[@id="olpOfferList"]/div/div/div[' + str(item_index + 2) + ']/div[5]/div/form/span/span/span/input').click()
        driver.find_element_by_id('hlb-view-cart-announce').click()
        dom =  lxml.html.fromstring(driver.page_source)
        price = dom.xpath('//*[@id="activeCartViewForm"]/div[2]/div/div[4]/div[2]/div[2]/p[1]/span/text()')

        driver.find_element_by_xpath('//*[@id="activeCartViewForm"]/div[2]/div/div[4]/div[2]/div[1]/div/div/div[2]/div/span[1]/span/input').click()
        driver.close()

        return price[0]

    def parse_sellers_page(self, response):
        amazon_item = response.meta['item']
        #############################################################
        lst = map(unicode.strip, map(remove_tags, response.xpath('//*[@id="olpOfferList"]/div/div/div/div[1]/p/span').extract()))
        num_sellers = len(lst)

        clean_lst = []
        for item in lst:
            if "FREE" in item:
                clean_lst.append("FREE")
            else:
                for tmp in item.split():
                    if "$" in tmp:
                        clean_lst.append(tmp)
        amazon_item["product_shipping_cost"] = clean_lst
        #####################################################################
        amazon_item["product_marketplace_price"] = [elem for elem in map(unicode.strip, response.xpath('//*[@id="olpOfferList"]/div/div/div/div[1]/span[1]/text()').extract()) if '$' in elem]
        amazon_item["seller_name"] = response.xpath('//*[@id="olpOfferList"]/div/div/div/div/h3/img/@alt').extract() + response.xpath('//*[@id="olpOfferList"]/div/div/div/div[4]/h3/span/a/text()').extract()
        amazon_item["seller_url"] = map(response.urljoin, response.xpath('//*[@id="olpOfferList"]/div/div/div/div/h3/img/@alt').extract() + response.xpath('//*[@id="olpOfferList"]/div/div/div/div[4]/h3/span/a/@href').extract())
        #############################################################
        for i in range(num_sellers):
            item_seller = amazon_item.copy()
            item_seller["product_shipping_cost"] = amazon_item["product_shipping_cost"][i]
            item_seller["product_marketplace_price"] = amazon_item["product_marketplace_price"][i]
            item_seller["seller_name"] = amazon_item["seller_name"][i]
            item_seller["seller_url"] = amazon_item["seller_url"][i]
            item_seller["product_shoppingcart_price"] = self.get_product_shoppingcart_price(response.url, i)
            yield item_seller

        next_sellers_page = response.xpath('//*[@id="olpOfferListColumn"]/div[2]/ul/li[4]/a/@href').extract_first()
        if next_sellers_page is not None:
            yield scrapy.Request(response.urljoin(next_sellers_page), meta={'item':amazon_item}, callback = self.parse_sellers_page)
