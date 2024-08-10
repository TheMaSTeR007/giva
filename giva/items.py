# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductRawItem(scrapy.Item):
    # define the fields for your item here like:
    product_name = scrapy.Field()
    product_url = scrapy.Field()


class ProductDataItem(scrapy.Item):
    # Data available in Json
    product_name = scrapy.Field()
    product_url = scrapy.Field()
    product_image_url = scrapy.Field()
    product_description = scrapy.Field()
    product_sku = scrapy.Field()
    product_brand = scrapy.Field()
    product_offer_price = scrapy.Field()
    product_currency = scrapy.Field()
    product_variant_url = scrapy.Field()
    product_rating_value = scrapy.Field()
    product_review_count = scrapy.Field()

    # Data available in html
    shipping_data = scrapy.Field()

    # Data coming from Delivery Time API with respect to pincode
    pincode = scrapy.Field()
    delivery_time_message = scrapy.Field()
