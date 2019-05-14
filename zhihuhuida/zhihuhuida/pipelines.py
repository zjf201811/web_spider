# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
name=input('请输入用户名:')

class ZhihuhuidaPipeline(object):
    def open_spider(self,spider):
        self.file=open('{}的所有回答.txt'.format(name),'w',encoding='utf-8')
    def process_item(self, item, spider):
        title = item['title']
        content = item['content']
        count = item['count']
        info="    {count}. {title}\n\n{content}\n\n\n\n\n\n".format(count=str(count),title=title,content=content)
        self.file.write(info)
        return item
    def close_spider(self,spider):
        self.file.close()
