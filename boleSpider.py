import requests
from lxml import etree
import json


class BoleSpider:
	def __init__(self):
		self.url_list = ["http://blog.jobbole.com/all-posts/page/{}/".format(i) for i in range(1,565)]
		self.headers = {
		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
		"Accept-Encoding": "gzip, deflate",
		"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
		"Cache-Control": "max-age=0",
		"Connection": "keep-alive",
		"Host": "blog.jobbole.com",
		"Referer": "http://blog.jobbole.com/",
		"Upgrade-Insecure-Requests": "1"
		}

	def parse_url(self, url):
		print(url)
		response = requests.get(url, headers=self.headers)
		return response.content

	def get_content_list(self, html_str):
		html = etree.HTML(html_str)
		div_list = html.xpath("//div[@id='archive']/div[@class='post floated-thumb']")
		content_list = []
		for div in div_list:
			item = {}
			item["title"] = div.xpath("./div[@class='post-meta']/p/a[1]/text()")[0] if len(div.xpath("./div[@class='post-meta']/p/a[1]/text()"))>0 else None
			item["time"] = div.xpath("./div[@class='post-meta']/p/text()")[0] if len(div.xpath("./div[@class='post-meta']/p/text()"))>0 else None
			item["href"] = div.xpath("./div[@class='post-meta']/p/a[1]/@href")[0] if len(div.xpath("./div[@class='post-meta']/p/a[1]/@href"))>0 else None
			item["content"] = self.get_detail_content(item["href"])
			content_list.append(item)
		return content_list

	def get_detail_content(self, detail_url):
		html_str = self.parse_url(detail_url)
		html = etree.HTML(html_str)
		content = ''.join(html.xpath("//div[@class='entry']//text()")) 
		return content

	def write_to_file(self, content_list):
		with open("bole.txt", "a" ,encoding="utf-8") as f:
			for content in content_list:
				f.write(json.dumps(content, ensure_ascii=False, indent=2))
				f.write("\n")
			print("保存成功")

	def run(self):
		for url in self.url_list:
			html = self.parse_url(url)
			content_list = self.get_content_list(html)
			self.write_to_file(content_list)


if __name__ == '__main__':
	bole_spider = BoleSpider()
	bole_spider.run()
			
