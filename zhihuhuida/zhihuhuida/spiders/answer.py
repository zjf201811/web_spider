# -*- coding: utf-8 -*-
import scrapy
import json
import re


class AnswerSpider(scrapy.Spider):
    count = 0
    name = 'answer'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    start_user = input("请输入url_tocken:")
    answer_url = 'https://www.zhihu.com/api/v4/members/{user}/answers?include={include}&offset={offset}&limit={limit}&sort_by=created'
    answer_query = 'data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Creview_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Clabel_info%2Crelationship.is_authorized%2Cvoting%2Cis_author%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B*%5D.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics'

    def start_requests(self):
        yield scrapy.Request(self.answer_url.format(user=self.start_user,include=self.answer_query,offset=0,limit=20),callback=self.parse_answer)

    def parse_answer(self,response):
        results = json.loads(response.text)
        for answer in results.get('data'):

            content=answer.get('content')
            content = re.sub('<.*?>', '', content)
            # context=re.sub(context,'<.+>','')
            # print({'title':answer.get('question').get('title'),'content':content})
            self.count+=1
            yield {'count': self.count,'title':answer.get('question').get('title'),'content':content}


        if 'paging' in results.keys() and results.get('paging').get('is_end')==False:
            page=results.get('paging').get('next')
            offset = re.findall('offset=(\d+)', page)[0]
            print(offset)

            next_page = self.answer_url.format(user=self.start_user,include=self.answer_query,offset=offset,limit=20)

            for i in range(50):
                print("")
            print(next_page)
            print(response.url)
            yield scrapy.Request(next_page,self.parse_answer)