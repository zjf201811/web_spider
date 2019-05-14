# -*- coding: utf-8 -*-
import scrapy


class MovieSpider(scrapy.Spider):
    count=0
    name = 'movie'
    allowed_domains = ['movie.douban.com']
    start=0
    start_urls = ['https://movie.douban.com/top250?start=0']

    def parse(self, response):
        count=self.count
        title = response.xpath("//span[@class='title'][1]/text()").extract()
        raning_num = response.xpath("//span[@class='rating_num'][1]/text()").extract()
        info = response.xpath("//div[@class='info']/div[@class='bd']/p[1]/text()").extract()
        intro = response.xpath("//div[@class='info']/div[@class='bd']//span[@class='inq']/text()  ").extract()
        print(title,raning_num,info,intro)
        for i in range(25):
            self.count+=1
            yield {'count': str(self.count),'title':title[i],'raning_num':raning_num[i],'info':info[2*i]+info[2*i+1],'intro':intro[i]}
        if self.start < 250:
            self.start += 25
            yield scrapy.Request("https://movie.douban.com/top250?start={}".format(self.start),callback=self.parse)
