# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import os,urllib.parse
from urllib.parse import urlparse
from os.path import basename, dirname, join
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings

# class JiandanPipeline(object):
#     def process_item(self, item, spider):
#         pass
#         return item


# class ImagePipeline(ImagesPipeline):
#     IMAGE_STORE = get_project_settings().get("IMAGE_STORE")
#
#     def get_media_requests(self, item, info):
#         image_urls = item["image_links"]
#         for image_url in image_urls:
#             # Global image_name = basename(urlparse(image_url).path)
#             yield scrapy.Request(image_url)
#
#     def item_completed(self, results, item, info):
#         image_path = [x["path"] for ok, x in results if ok]
#         item["image_path"] = self.IMAGE_STORE
#         return item