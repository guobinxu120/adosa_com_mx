# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, FormRequest
from urlparse import urlparse
import json, urllib
from scrapy.selector import Selector

from scrapy.utils.response import open_in_browser
class CategoriesOfAdosaComMx(scrapy.Spider):

	name = "categories_of_adosa_com_mx"
	start_urls = ('http://adosa.com.mx/',)

	def parse(self, response):

		url = "http://adosa.com.mx/busqueda.aspx/crea_menu"
		
		headers = {
		    #'Accept':'application/json, text/javascript, */*; q=0.01',
		    #'Accept-Encoding':'gzip, deflate',
		    #'accept-language':'en-US,en;q=0.8',
		    #'Connection':'keep-alive',
		    #'Content-Length':'151',
		    'content-type':'application/json; charset=UTF-8',  # this value must be here. otherwise the response is incorrect
		    # 'Cookie':cookie,
		    # 'Host':host,
		    #'Origin':'http://adosa.com.mx',
		    #'Referer':'http://adosa.com.mx/',
		    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
		    'X-Requested-With':'XMLHttpRequest'
		}

		for x in xrange(1,6):
			
			payload = {"id_catego":str(x)}

			yield scrapy.Request(url, method='POST',
                            callback=self.parse_category,
                            #errback=self.errback_httpbin,
                            body=json.dumps(payload),
                            headers=headers)

	def parse_category(self, response):
		data = json.loads(response.body)
		sel = Selector(text=data['d'])
		links = sel.xpath('//body/li/div/ul/li[position()<last()]/a/@href').extract()
		
		yield {'links':list("/"+x for x in links)}
