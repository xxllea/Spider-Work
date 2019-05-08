# -*- coding: utf-8 -*-
import scrapy
from jiandan.items import JiandanItem


class ArticleSpider(scrapy.Spider):
    name = 'article'
    allowed_domain = 'i.jandan.net'
    start_urls = ['http://i.jandan.net/']

    def parse(self, response):
        url_list = response.xpath("//h2[@class='thetitle']/a/@href").extract()
        for url in url_list:
            yield scrapy.Request(url, callback=self.parse_detail)

        next_url = response.xpath("//div[@class='wp-pagenavi']/a[last()]/@href").extract_first()
        if next_url is not None:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_detail(self, response):
        item = JiandanItem()
        item["title"] = response.xpath("//h1[@class='thetitle']/a/text()").extract_first()
        item["name"] = response.xpath("//div[@class='postinfo']/text()").extract()[-1].split("@")[0].strip()
        item["date"] = response.xpath("//div[@class='postinfo']/text()").extract()[-1].split("@")[1].strip()
        item["content"] = ''.join(response.xpath("//div[@class='entry']/p/text()").extract()).replace("\n", "").strip()
        if '无聊图' in item["title"]:
            item["content"] = ';'.join(response.xpath("//div[@class='entry']/p/img/@data-original").extract())
        print(item)
        yield item
