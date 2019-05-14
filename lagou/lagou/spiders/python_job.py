# -*- coding: utf-8 -*-
import scrapy


class PythonJobSpider(scrapy.Spider):
    name = 'python_job'
    allowed_domains = ['lagou.com']
    start_urls = ['https://www.lagou.com/jobs/5920752.html']

    def parse(self, response):
        print(response.xpath('//div[@class="job-detail"]/text()').extract())
        # title = response.xpath('//h3/text()').extract()
        # print(title)
