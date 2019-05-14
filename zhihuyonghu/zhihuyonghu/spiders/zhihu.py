# -*- coding: utf-8 -*-
import scrapy
import json
from zhihuyonghu.items import UserItem
import re


class ZhihuSpider(scrapy.Spider):
    yonghu_set=set()
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    start_user='shou-hu-song-shu-de-guang-ming-qi-shi'
    user_url = "https://www.zhihu.com/api/v4/members/{user}?include={include}"
    user_query = "allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics"
    follows_url = "https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}"
    follows_query = "data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics"
    the_url=follows_url.format(user=start_user,include=follows_query,offset=0,limit=20)
    def start_requests(self):
        yield scrapy.Request(self.user_url.format(user=self.start_user,include=self.user_query),callback=self.parse_user)
        yield scrapy.Request(self.the_url,callback=self.parse_follows)

        # url = 'https://www.zhihu.com/api/v4/members/feifeimao/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=20&limit=20' # 关注列表
        # url = 'https://www.zhihu.com/api/v4/members/nuttie-tina?include=allow_message%2Cis_followed%2Cis_following%2Cis_org%2Cis_blocking%2Cemployments%2Canswer_count%2Cfollower_count%2Carticles_count%2Cgender%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics' # 个人信息

        # yield scrapy.Request(url, callback=self.parse)

    def parse_user(self, response):
        result=json.loads(response.text)
        item = UserItem()
        for field in item.fields:
            if field in result.keys():
                item[field]=result.get(field)
        if result['url_token'] not in self.yonghu_set:
            self.yonghu_set.add(result['url_token'])
            yield item
            yield scrapy.Request(self.follows_url.format(user=result.get('url_token'), include=self.follows_query,limit=20, offset=0), callback=self.parse_follows)

            # self.offset=0
            # the_url = self.follows_url.format(user=item.get('url_token'), include=self.follows_query,offset=self.offset,limit=20)
            # yield scrapy.Request(the_url, callback=self.parse_follows)
    def parse_follows(self, response):
        for i in range(10):
            print("")
        print(response.url)
        results=json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                yield scrapy.Request(self.user_url.format(user=result.get('url_token'),include=self.user_query),self.parse_user)
        if 'paging' in results.keys() and results.get('paging').get('is_end')==False:
            page=results.get('paging').get('next')
            offset = re.findall('offset=(\d+)', page)[0]
            print(offset)

            next_page = self.follows_url.format(user=self.start_user,include=self.follows_query,offset=offset,limit=20)

            for i in range(50):
                print("")
            print(next_page)
            print(response.url)
            yield scrapy.Request(next_page,self.parse_follows)
