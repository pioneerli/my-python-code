# -*- coding: utf-8 -*-
import scrapy

from scrapy_doutulai.items import ScrapyDoutulaiItem

class DoutulaiSpiderSpider(scrapy.Spider):
    name = 'doutulai_spider'
    allowed_domains = ['www.doutula.com']
    start_urls = ['https://www.doutula.com/photo/list/']
    page = 1

    def parse(self, response):
        content_items = ScrapyDoutulaiItem()
        # 解析img_url列表，拿到图片的url和，图片名称
        img_url_list = response.xpath('//img[@class="img-responsive lazy image_dta"]')
        # page_number = response.xpath('//*[@id="pic-detail"]/div/div[3]/div[3]/ul/li[12]/a/text()').extract_first()
        page_number = response.xpath('//a[@class="page-link"][last()]/text()').extract_first()

        for img_content in img_url_list:
            content_items['img_url'] = img_content.xpath('./@data-original').extract_first()
            content_items['img_name'] = img_content.xpath('./@data-original').extract_first().split('/')[-1]
            print(content_items)
            yield content_items
        # 不断爬取新页面
        if self.page <= page_number:
            self.page += 1
            next_url = self.start_urls[0] + '?page=' + str(self.page)
            yield scrapy.Request(next_url)