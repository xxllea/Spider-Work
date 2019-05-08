# -*- coding: utf-8 -*-
import scrapy
from dangdang.items import DangdangItem


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-recent30-0-0-1-{}'.format(i) for i in range(1, 26)]

    def parse(self, response):
        li_list = response.xpath("//ul[@class='bang_list clearfix bang_list_mode']/li")
        for li in li_list:
            item =DangdangItem()
            item["index"] = li.xpath(".//div[contains(@class,'list_num')]/text()").extract_first().replace(".", "")
            item["title"] = li.xpath(".//div[@class='name']/a/@title").extract_first()
            item["author"] = li.xpath(".//div[@class='publisher_info'][1]/a[1]/@title").extract_first()
            item["publisher"] = li.xpath(".//div[@class='publisher_info'][2]/a/text()").extract_first()
            item["date"] = li.xpath(".//div[@class='publisher_info']/span/text()").extract_first()
            item["price"] = li.xpath(".//div[@class='price']/p[1]/span[@class='price_n']/text()").extract_first()
            item["comments"] = li.xpath(".//div[@class='star']/a/text()").extract_first().replace("条评论", "")
            href = li.xpath(".//div[@class='name']/a/@href").extract_first()

            yield scrapy.Request(
                href,
                callback=self.parse_detail,
                meta={"item": item}
            )


    def parse_detail(self, response):
        item = response.meta["item"]
        item["type"] = '/'.join(response.xpath(".//div[@id='breadcrumb']//a//text()").extract()[1:3]).replace("\\", "/")
        yield item
