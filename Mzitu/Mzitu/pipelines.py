# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
# from scrapy.exceptions import DropItem
# import re

class MzituPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield Request(item["image_url"], meta={"item": item["image_name"]})

    def file_path(self, request, response=None, info=None):
        name = request.meta["item"]
        # name = re.sub(r'[？\\*|“<>:/()0123456789]', '', name)
        image_guid = request.url.split("/")[-1]
        file_name = u'/{0}/{1}'.format(name, image_guid)
        return file_name












