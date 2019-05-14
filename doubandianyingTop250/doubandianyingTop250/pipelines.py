# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

# class Doubandianyingtop250Pipeline(object):
#     def open_spider(self,spider):
#         self.file=open('豆瓣电影top250.txt','w',encoding='utf-8')
#     def process_item(self, item, spider):
#         count = item['count']
#         title = item['title']
#         raning_num = item['raning_num']
#         info = item['info']
#         info = re.sub("\s{3,}","",info)
#         intro = item['intro']
#         info="{count}. {title}\n评分：{raning_num}\n{info}\n{intro}\n\n\n\n".format(count=count,title=title,raning_num=raning_num,info=info,intro=intro)
#         self.file.write(info)
#         return item
#     def close_spider(self,spider):
#         self.file.close()
import pymongo

class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # collection_name = item.__class__.__name__
        self.db['user'].update({'title': item['title']},{'$set': item},True)
        return item

