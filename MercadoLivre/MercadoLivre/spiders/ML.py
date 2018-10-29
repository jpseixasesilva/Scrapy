# -*- coding: utf-8 -*-
import scrapy


class MlSpider(scrapy.Spider):
    name = 'ML'
    ##allowed_domains = ['mercadolivre.com.br']
    start_urls = ['https://lista.mercadolivre.com.br/instrumentos-corda-guitarras/']

    def parse(self, response):
        items = response.xpath('//ol[@id="searchResults"]/li')
                    
        for item in items:
            url = url = item.xpath('./div/div/div/div/ul/li/a/@href').extract_first()
            yield scrapy.Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        title = response.xpath('//h1[@class="item-title__primary "]/text()').extract_first()
        pricef = response.xpath('//span[@class="price-tag-fraction"]/text()').extract_first()
        pricec = response.xpath('//span[@class="price-tag-cents"]/text()').extract_first()
        pricet = pricef+','+pricec
        model = response.xpath('//strong[contains(text(), "Modelo")]/following-sibling::span/text()').extract_first()
        yield {
            'title': title,
            'pricet': pricet,
            'model': model,
        }