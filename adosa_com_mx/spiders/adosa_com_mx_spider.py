# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy import Request
from urlparse import urlparse
from json import loads
from datetime import date
import time
import datetime

class AdosaComMxSpider(scrapy.Spider):

    name = "adosa_com_mx_spider"

###########################################################

    def __init__(self, categories=None, *args, **kwargs):
        super(AdosaComMxSpider, self).__init__(*args, **kwargs)

        if not categories:
            raise CloseSpider('Received no categories!')
        else:
            self.categories = categories
        self.start_urls = loads(self.categories).keys()

###########################################################

    def start_requests(self):
        for url in self.start_urls:
            yield Request(('http://adosa.com.mx')+url, callback=self.parse, meta={'CatURL':url})

###########################################################

    def parse(self, response):
        
        products = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_Panel_resultados"]/div/div')

        print len(products)

        if not products: return
        
        for i in products:
            item = {}

            item['Vendedor'] = 214
            item['ID'] = i.xpath('./@id').extract_first().split('_')[-1]
            item['Title'] = ' '.join(i.xpath('.//a[contains(@href, "detalle_articulo")]//text()').extract()).replace('\n','').replace('\r','').strip()
            #item['Description'] = ''

            price = ''.join(i.xpath('.//*[contains(@id, "id_oferta")]/@value').re(r'[\d.]+'))
            if not price:
                price = ''.join(i.xpath('.//*[contains(@id, "id_normal")]/@value').re(r'[\d.]+'))
            if price:
                item['Price'] = price.strip()
                item['Currency'] = 'MXN'

            item['Category URL'] = response.meta['CatURL']
            item['Details URL'] = response.urljoin(i.xpath('./div[2]/a/@href').extract_first())
            item['Date'] = date.today()

            item['timestamp'] = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            item['image_url'] = response.urljoin(i.xpath('./img/@data-original').extract_first())

            if price:
                yield item            

        # Pagination seems not to be here.

        # next = response.xpath('//*[@class="numbers"]//*[@class="actual"]/following-sibling::a[1]/@href').extract()
        # if next:
        #     yield Request(response.urljoin(next[0]), callback=self.parse, meta=response.meta)
    