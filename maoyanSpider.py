import requests
from lxml import etree
import json


class MaoyanSpider(object):
	def __init__(self):
		self.headers = {
		"User_Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
		"cookie": "__mta=45439771.1545831750478.1545833664312.1545833671605.3; uuid_n_v=v1; uuid=169C2AC0091411E9A15EBD81A577D9A741204A0D92CC4C1C8AD25723CFABC229; _csrf=30af4999f8627c90f4b2eeca59323edabc98f558e51db8394737c4417d5d7ae7; _lxsdk_cuid=167eac09af4c8-050980e5f45035-19291c0a-100200-167eac09af4c8; _lxsdk=169C2AC0091411E9A15EBD81A577D9A741204A0D92CC4C1C8AD25723CFABC229; _lxsdk_s=167eaddcf1e-092-52a-a5e%7C%7C4"
		}

	def get_one_page(self,url):
		response = requests.get(url, headers=self.headers)
		return response.text

	def parse_one_page(self,html):
		selector = etree.HTML(html)
		dd_list = selector.xpath("//dl[@class='board-wrapper']/dd")
		content_list = []
		for dd in dd_list:
			item = {}
			item["top"] = dd.xpath("./i/text()")[0] if len(dd.xpath("./i/text()"))>0 else None
			item["title"] = dd.xpath(".//p[@class='name']/a/text()")[0] if len(dd.xpath(".//p[@class='name']/a/text()")) else None
			item["actor"] = dd.xpath(".//p[@class='star']/text()")[0].replace("主演：","").strip() if len(dd.xpath(".//p[@class='star']/text()")) else None
			item["time"] = dd.xpath(".//p[@class='releasetime']/text()")[0] if len(dd.xpath(".//p[@class='releasetime']/text()"))>0 else None
			item["star"] = dd.xpath(".//p[@class='score']/i/text()")[0] + dd.xpath(".//p[@class='score']/i/text()")[1] if len(dd.xpath(".//p[@class='score']/i/text()"))>0 else None
			item["img"] = dd.xpath("./a/img[2]/@data-src")[0] if len(dd.xpath("./a/img[2]/@data-src"))>0 else None
			content_list.append(item)
		return content_list

	def write_to_file(self, content_list):
		with open("maoyan_movie.txt", 'a', encoding="utf-8") as f:
			for content in content_list:
				f.write(json.dumps(content, ensure_ascii=False, indent=2))
				f.write("\n")

	def run(self):
		for i in range(0,100,10):
			url = "https://maoyan.com/board/4?offset=" + str(i)
			html = self.get_one_page(url)
			content_list = self.parse_one_page(html)
			self.write_to_file(content_list)

if __name__ == '__main__':
	maoyan_spider = MaoyanSpider()
	maoyan_spider.run()
