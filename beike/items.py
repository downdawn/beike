# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BeikeItem(scrapy.Item):
    # define the fields for your item here like:
    collection = 'BJ'
    url = scrapy.Field()
    apartment_name = scrapy.Field()
    apartment_price = scrapy.Field()
    apartment_mode = scrapy.Field()
    apartment_master = scrapy.Field()
    apartment_phone = scrapy.Field()
    apartment_facility = scrapy.Field()
    apartment_renting = scrapy.Field()
    zufang_name = scrapy.Field()
    zufang_time = scrapy.Field()
    zufang_house_codes = scrapy.Field()
    zufang_price = scrapy.Field()
    zufang_mode = scrapy.Field()
    zufang_tags = scrapy.Field()
    zufang_article = scrapy.Field()
    zufang_master = scrapy.Field()
    zufang_phone = scrapy.Field()
    zufang_info = scrapy.Field()
    zufang_ucid = scrapy.Field()
    this_url = scrapy.Field()


