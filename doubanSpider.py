import requests
from lxml import etree
import json


class DoubanSpider(object):

	def __init__(self):
		self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'}
		
	def get_one_page(self,url):
		response = requests.get(url, headers=self.headers)
		return response.text

	def parse_one_page(self,html):
		selector = etree.HTML(html)
		li_list = selector.xpath("//ol[@class='grid_view']/li")
		content_list = []
		for li in li_list:
			item = {}	
			item["top"] = int(li.xpath(".//div[@class='pic']/em/text()")[0]) if len(li.xpath(".//div[@class='pic']/em/text()"))>0 else None
			item["title"] = li.xpath(".//div[@class='hd']/a/span[1]/text()")[0] if len(li.xpath(".//div[@class='hd']/a/span[1]/text()"))>0 else None
			item["star"] = li.xpath(".//div[@class='star']/span[2]/text()")[0] if len(li.xpath(".//div[@class='star']/span[2]/text()"))>0 else None
			item["quote"] = li.xpath(".//p[@class='quote']/span/text()")[0] if len(li.xpath(".//p[@class='quote']/span/text()"))>0 else None
			content_list.append(item)
		return content_list

	def write_to_file(self,content_list):
		with open("douban_movie.txt",'a',encoding="utf-8") as f:
			for content in content_list:
				f.write(json.dumps(content,ensure_ascii=False,indent=2))
				f.write("\n")

	def run(self):
		for i in range(0,226,25):
			url = "https://movie.douban.com/top250?start="+str(i)+"&filter="
			html = self.get_one_page(url)
			content_list = self.parse_one_page(html)
			self.write_to_file(content_list)

if __name__ == '__main__':
	douban_spider = DoubanSpider()
	douban_spider.run()
	       


		
