# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class FangchanxinxiPipeline(object):
    def open_spider(self,spider):
        self.file=open('哈尔滨所有近期房源.txt','w',encoding='utf-8')
    def process_item(self, item, spider):
        info_url=item['info_url']
        title=item['title']
        structure=item['structure']
        area=item['area']
        orientation=item['orientation']
        floor=item['floor']
        district=item['district']
        price=item['price']
        unit_price=item['unit_price']
        context='详情页面:{}\n标题:{}\n格局:{}-面积:{}-朝向:{}-楼层:{}\n小区:{}\n价格:{}({})\n\n\n'.format(info_url,title,structure,area,orientation,floor,district,price,unit_price)
        self.file.write(context)
        return item
    def close_spider(self,spider):
        self.file.close()
