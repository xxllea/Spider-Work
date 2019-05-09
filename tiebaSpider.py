# coding=utf-8
import requests
from lxml import etree
import json


class BaiduSpider:
	def __init__(self,tieba_name):
		self.tieba_name = tieba_name
		self.headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36"}
		self.part_url = "http://tieba.baidu.com/mo/q----,sz@320_240-1-3---2/"
		self.start_url = "http://tieba.baidu.com/mo/q----,sz@320_240-1-3---2/m?kw="+tieba_name+"&lp=5011&lm=&pn=0"

	def parse_url(self, url):
		print(url)
		response = requests.get(url, headers=self.headers)
		return response.content

	def get_content_list(self, html_str):
		html = etree.HTML(html_str)
		content_list = []
		div_list = html.xpath("//div[contains(@class, 'i')]")
		for div in div_list:
			item = {}
			item["title"] = div.xpath("./a/text()")[0] if len(div.xpath("./a/text()"))>0 else None
			item["href"] = self.part_url + div.xpath("./a/@href")[0] if len(div.xpath("./a/@href"))>0 else None
			item["content"] = self.parse_detail_content(item["href"],[])
			content_list.append(item)		
		next_url = self.part_url+html.xpath("//a/text()='下一页')]/@href")[0] if len(html.xpath("//a/text()='下一页')]/@href")) else None
		return content,next_url

	def parse_detail_content(self, detail_url, total_content):
		html_str = self.parse_url(detail_url)
		html = etree.HTML(html_str)
		detail_content = []
		div_list = html.xpath("//div[@class='i']")
		for div in div_list:
			item = []
			item["name"] = div.xpath(".//span[@class='g']/a/text()")[0] if len(div.xpath(".//span[@class='g']/a/text()"))>0 else None
			item["time"] = div.xpath(".//span[@class='b']/text()")[0] if len(div.xpath(".//span[@class='b']/text()"))>0 else None
			item["say"] = ''.join(div.xpath("./text()")) if len(div.xpath("./text()"))>0 else None
			detail_content.append(item)
		total_content.extend(detail_content)
		
		detail_next_url = html.xpath("//a/text()='下一页')]/@href")
		if len(detail_next_url)>0:
			detail_next_url = self.part_url+detail_next_url[0]
			return self.parse_detail_content(detail_next_url,total_content)
		return total_content

	def write_to_file(self,content_list):
		file_path = self.tieba_name+".txt"
		with open(file_path,'a',encoding="utf-8") as f:
			for content in content_list:
				f.write(json.dumps(content, ensure_ascii=False, indent=2))
				f.write("\n")

	def run(self): 
		next_url = self.start_url
		while next_url is not None:
			html = self.parse_url(next_url)
			content_list,next_url = self.get_content_list(html)
			self.write_to_file(content_list)
			print("保存成功")


if __name__ == '__main__':
	name = input("请输入贴吧名字:")
	baidu_Spider = BaiduSpider(name)
	baidu_Spider.run()

