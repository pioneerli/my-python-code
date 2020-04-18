# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from urllib import urlretrieve
from scrapy_doutulai.settings import DOWNLOAD_DIR

class ScrapyDoutulaiPipeline(object):
    def __init__(self):
        """
        判断下载目录是否存在
        """
        if not os.path.exists(DOWNLOAD_DIR):
            os.makedirs(DOWNLOAD_DIR)

    def process_item(self, item, spider):
        """
        下载图片
        :param item:
        :param spider:
        :return:
        """
        try:
            filename = os.path.join(DOWNLOAD_DIR,item['img_name'])
            print(filename)
            urlretrieve(item['img_url'],filename)
        except Exception as e:
            pass