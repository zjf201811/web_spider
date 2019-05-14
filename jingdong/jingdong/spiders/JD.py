# -*- coding: utf-8 -*-
import scrapy


class JdSpider(scrapy.Spider):
    store_dict={}
    page=1
    name = 'JD'
    allowed_domains = ["search.jd.com"]
    keyword=input("请输入keyword:")
    start_urls = ["https://search.jd.com/Search?keyword={keyword}&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&suggest=1.def.0.V03--12%2C20%2C&wq=jizhua&stock=1&page=1".format(keyword=keyword)]
    base_url = "https://search.jd.com/Search?keyword={keyword}&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&suggest=1.def.0.V03--12%2C20%2C&wq=jizhua&stock=1&page={page}"
    def parse(self, response):
        commodity_title=response.xpath('//div[@class="gl-i-wrap"]/div[1]/a/@title').extract()
        commodity_url=response.xpath('//div[@class="gl-i-wrap"]/div[1]/a/@href').extract()
        price=response.xpath('//div[@class="gl-i-wrap"]//div[@class="p-price"]/strong/i/text()').extract()
        store = response.xpath('//span[@class="J_im_icon"]/a/text()').extract()
        store_url = response.xpath('//span[@class="J_im_icon"]/a/@href').extract()
        print(commodity_title,commodity_url,price,store,store_url)
        for i,j in zip(store,store_url):
            self.store_dict.update({i:j})
        print(self.page)
        if self.page < 199:
            self.page += 2
            yield scrapy.Request(self.base_url.format(keyword=self.keyword, page=self.page),callback=self.parse)
        else:
            for i in self.store_dict:
                yield scrapy.Request(self.store_dict[i],callback=self.store_parse)

    def store_parse(self, response):
        commodity_url=response.xpath()



