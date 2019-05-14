# -*- coding: utf-8 -*-
import scrapy
import json

class AllmovieSpider(scrapy.Spider):
    content=None
    name = 'allmovie'
    start=0
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%94%B5%E5%BD%B1&start=0']
    base_url='https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%94%B5%E5%BD%B1&start={start}'
    movie_info_url = 'https://movie.douban.com/j/subject_abstract?subject_id={id}'
    movie_url = 'https://movie.douban.com/subject/{id}'
    def parse(self, response):
        print(response.header.getlist('Set-Cookie'))
        results = json.loads(response.text)
        if results['data']:
            for i in results['data']:
                id = i.get('id')
                yield scrapy.Request(self.movie_info_url.format(id=id), callback=self.info_parse)
            self.start+=20

            yield scrapy.Request(self.base_url.format(start=self.start),callback=self.parse)

    def info_parse(self,response):
        results = json.loads(response.text)
        yield results['subject']






