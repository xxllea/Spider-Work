# encoding:utf-8
import requests
from lxml import etree
import json


class JiandanSpider:
	def __init__(self):
		self.start_url = 'http://jandan.net/page/1/'
		self.part_url = "http://jandan.net/"
		self.headers = {
		"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
		"Accept-Encoding": "gzip, deflate",
		"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
		"Connection": "keep-alive",
		"Host": "i.jandan.net",
		"Referer": "http://jandan.net/",
		"Upgrade-Insecure-Requests": "1"
		}

	def parse_url(self,url):
		print(url)
		response = requests.get(url,headers=self.headers)
		return response.content

	def get_content_list(self,html_str):
		html = etree.HTML(html_str)
		content_list = []
		div_list = html.xpath("//div[@id='maincontent']/div[@class='post']")
		for div in div_list:
			item = {}
			item["title"] = div.xpath(".//h2[@class='thetitle']/a/text()")[0] if len(div.xpath(".//h2[@class='thetitle']/a/text()"))>0 else None
			item["index"] = div.xpath(".//div[@class='indexs']/text()")[0].strip() if len(div.xpath(".//div[@class='indexs']/text()"))>0 else None
			item["href"] = div.xpath(".//h2[@class='thetitle']/a/@href")[0] if len(div.xpath(".//h2[@class='thetitle']/a/@href"))>0 else None
			item["content"] = self.get_detail_content(item["href"])
			content_list.append(item)
		next_url = self.part_url + html.xpath("//div[@class='wp-pagenavi']/a[last()][contains(text(),'下一页')]/@href")[0] if len(html.xpath("//div[@class='wp-pagenavi']/a[last()][contains(text(),'下一页')]/@href"))>0 else None
		return content_list,next_url

	def get_detail_content(self,detail_url):
		html_str = self.parse_url(detail_url)
		html = etree.HTML(html_str)
		content = ''.join(html.xpath("//div[@id='maincontent']//div[@class='entry']/p/text()")).replace("\r\n|\n",'').strip()
		if len(content) == 0 :
			content = ','.join(html.xpath("//div[@id='maincontent']//div[@class='entry']/p/img/@data-original")) 
		return content

	def write_to_file(self,content_list):
		with open("jiandan.txt", "a", encoding="utf-8") as f:
			for content in content_list:
				f.write(json.dumps(content,ensure_ascii=False,indent=2))
				f.write("\n")
			print("保存成功")

	def run(self):
		next_url = self.start_url
		while next_url is not None:
			html = self.parse_url(next_url)
			content_list,next_url = self.get_content_list(html)
			self.write_to_file(content_list) 


if __name__ == '__main__':
	jiandan_spider = JiandanSpider()
	jiandan_spider.run()


