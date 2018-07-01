import os
import MySQLdb
import requests
import pandas as pd
from lxml import html
from sqlalchemy import create_engine

URL = "https://en.wikipedia.org/wiki/2018_Winter_Olympics_medal_table"

class WikiCrawler:
	def __init__(self):
		self.db_host = '127.0.0.1'
		self.db_name = 'WIKI'
		self.db_user = 'root'
		self.db_pass = 'root'
		self.table = "Olympics"
		self.create_connection()

	def create_connection(self):
		self.engine = create_engine("mysql+pymysql://root:root@localhost/WIKI?host=localhost?port=3306")

	def load_data(self, data):
		data.to_sql(self.table, self.engine, if_exists="append", index=False) 

	def crawl(self):
		resp = requests.get(URL).text
		resp = html.fromstring(resp)
		return resp

	def parse(self, resp):
		table = resp.xpath('//table[contains(@class, "wikitable sortable")]//tr')
		data = []
		for t in table:
			country = ''.join(t.xpath('.//th//a//text()'))
			short_name = ''.join(t.xpath('.//th//span//text()'))
			image = "http:%s" %''.join(t.xpath('.//img/@src'))
			numbers = [int(i) for i in t.xpath('.//td//text()')]
			if not numbers:
				continue

			if len(numbers) > 4:
				rank, gold, silver, bronze, total = numbers
			elif len(numbers) > 3:
				gold, silver, bronze, total = numbers
			else:
				print("New Case needs to be handled")
				break

			data.append({'country' : country, 
						 'short_name' : short_name,
						 'rank' : rank,
						 'gold' : gold,
						 'silver' : silver,
						 'bronze' : bronze,
	                  	'total' : total,
					    'image' : image}) 

		return pd.DataFrame(data)

	def run(self):
		hdoc = self.crawl()
		data = self.parse(hdoc)
		self.load_data(data)

if __name__ == "__main__":
	obj = WikiCrawler()
	obj.run()
