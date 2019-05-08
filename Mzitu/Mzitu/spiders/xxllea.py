# -*- coding: utf-8 -*-
import scrapy
from Mzitu.items import MzituItem


class XxlleaSpider(scrapy.Spider):
    name = 'xxllea'
    allowed_domains = ['mzitu.com']
    start_urls = ['https://www.mzitu.com/']

    def parse(self, response):
        # 分组
        li_list = response.xpath("//ul[@id='pins']/li")
        for li in li_list:
            href = li.xpath(".//span/a/@href").extract_first()
            yield scrapy.Request(href, callback=self.parse_detail)
        # 翻页
        next_page = response.xpath("//a[contains(text(),'下一页')]/@href").extract_first()
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_detail(self, response):
        item = MzituItem()
        item["image_url"] = response.xpath("//div[@class='main-image']//img/@src").extract_first()
        item["image_name"] = response.xpath("//div[@class='main-image']//img/@alt").extract_first()
        yield item
        # 翻页
        next_page = response.xpath("//span[contains(text(),'下一页')]/parent::a/@href").extract_first()
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse_detail)

