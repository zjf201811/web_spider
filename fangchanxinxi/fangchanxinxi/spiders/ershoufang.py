# -*- coding: utf-8 -*-
import scrapy


class ErshoufangSpider(scrapy.Spider):
    name = 'ershoufang'
    allowed_domains = ['58.com']
    start_urls = []
    base_url = "https://hrb.58.com/{area}/ershoufang/h1/"
    for area in ['nangang','daoli','xiangfang','pingfang','daowai','jiangbei']:
        start_urls.append("https://hrb.58.com/{area}/ershoufang/h1/".format(area=area))

    def parse(self, response):
        # print(self.start_urls)
        next_url=response.xpath('//div[@class="pager"]/a[@class="next"]/@href').extract()
        info_url=response.xpath('//div[@class="list-info"]/h2/a/@href').extract()
        title = response.xpath('//h2[@class="title"]/a/text()').extract()
        structure = response.xpath('//p[@class="baseinfo"][1]/span[1]/text()').extract()
        area = response.xpath('//p[@class="baseinfo"][1]/span[2]/text()').extract()
        orientation = response.xpath('//p[@class="baseinfo"][1]/span[3]/text()').extract()
        floor = response.xpath('//p[@class="baseinfo"][1]/span[4]/text()').extract()
        district = response.xpath('//p[@class="baseinfo"][2]/span[1]/a[1]/text()').extract()
        price = response.xpath('//p[@class="sum"]/b/text()').extract()
        unit_price = response.xpath('//p[@class="unit"]/text()').extract()
        for i in zip(info_url,title,structure,area,orientation,floor,district,price,unit_price):
            yield {'info_url':i[0],'title':i[1],'structure':i[2],'area':i[3],'orientation':i[4],'floor':i[5],'district':i[6],'price':i[7],'unit_price':i[8]}

        # for url in info_url:
        #     # pass
        #     yield scrapy.Request(url, callback=self.info_parse)
        if next_url:
            yield scrapy.Request("https://hrb.58.com"+next_url[0],callback=self.parse)

    def info_parse(self,response):
        print(response.text)