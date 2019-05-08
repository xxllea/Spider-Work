# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JiandanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    name = scrapy.Field()
    date = scrapy.Field()
    content = scrapy.Field()
    # image_links = scrapy.Field()
    # image_path = scrapy.Field()
    pass
