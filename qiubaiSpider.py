import requests
from lxml import etree
import json


class QiubaiSpider(object):
	def __init__(self):
		self.url_temp = "https://www.qiushibaike.com/hot/page/{}/"
		self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"}
		
	def get_url_list(self):
		return [self.url_temp.format(i) for i in range(1,14)]

	def parse_url(self, url):
		response = requests.get(url,headers=self.headers)
		return response.content.decode()

	def get_content_list(self, html_str):
		html = etree.HTML(html_str)
		div_list = html.xpath("//div[@id='content-left']/div")
		content_list = []
		for div in div_list:
			item = {}
			item["content"] = div.xpath(".//div[@class='content']/span/text()")
			item["content"] = [i.replace("\n","") for i in item["content"]]
			item["author_gender"] = div.xpath(".//div[contains(@class,'articleGender')]/@class")
			item["author_gender"] = item["author_gender"][0].split(" ")[-1].replace("Icon","") if len(item["author_gender"])>0 else None
			item["author_age"] =  div.xpath(".//div[contains(@class,'articleGender')]/text()") 
			item["author_age"] = item["author_age"][0] if len(item["author_age"])>0 else None
			item["content_img"] = div.xpath(".//div[@class='thumb']/a/img/@src")
			item["content_img"] = "https:"+item["content_img"][0] if len(item["content_img"])>0 else None
			item["author_img"] = div.xpath(".//div[@class='author clearfix']//img/@src") 
			item["author_img"] = "https:"+item["author_img"][0] if len(item["author_img"])>0 else None
			item["stats_vote"] = div.xpath(".//span[@class='stats-vote']/i/text()") 
			item["stats_vote"] = item["stats_vote"][0] if len(item["stats_vote"])>0 else None
			content_list.append(item)
		return content_list

	def write_to_file(self, content_list):
		with open("qiubai.txt","a") as f:
			for content in content_list:
				f.write(json.dumps(content, ensure_ascii=False, indent=2))
				f.write("\n")
		
	def run(self): 
		url_list = self.get_url_list()
		for url in url_list:
			html_str = self.parse_url(url)
			content_list = self.get_content_list(html_str)
			self.write_to_file(content_list)


if __name__ == '__main__':
	qiubai = QiubaiSpider()
	qiubai.run()

