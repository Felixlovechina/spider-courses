# -*- coding: utf-8 -*-
import scrapy
# from mfw_pic_sample.items import MfwPicSampleItem

class MfwSpider(scrapy.Spider):
    name = "mfw"
    allowed_domains = ["mafengwo.cn"]
    start_urls = ['http://www.mafengwo.cn/i/1082510.html']

    def parse(self, response):
        # item = MfwPicSampleItem()
        # image_urls = []
        for image_item in response.xpath('//img'):
            # image_urls.append(image_item.xpath('./@src').extract())
            yield {'image_urls': image_item.xpath('./@data-src').extract() }
        # item['image_urls'] = image_urls
        # return item
