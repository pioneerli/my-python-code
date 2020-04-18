# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyDoutulaiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 定义图片url和name
    img_url = scrapy.Field()
    img_name = scrapy.Field()

