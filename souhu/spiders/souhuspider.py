# -*- coding: utf-8 -*-
import copy
import logging

import scrapy
import json
from scrapy.utils.project import get_project_settings
import pymongo
import re
from scrapy_redis.spiders import RedisSpider

settings = get_project_settings()


class SouhuspiderSpider1(scrapy.Spider):
    name = 'souhuspider1'
    allowed_domains = ['souhu.com']
    custom_settings = {'ITEM_PIPELINES': {'souhu.pipelines.SouhuPipeline1': 300}}

    def get_page_link():
        url_list = []
        for i in range(2, 15556):
            url_list.append('http://v2.sohu.com/integration-api/mix/region/' + str(i))
        return url_list

    start_urls = get_page_link()

    def parse(self, response):
        res = response.body.decode('utf-8')
        res = json.loads(res)
        res_data = res['data']
        return res_data


class SouhuspiderSpider2(scrapy.Spider):
    name = 'souhuspider2'
    allowed_domains = ['souhu.com']
    custom_settings = {'ITEM_PIPELINES': {'souhu.pipelines.SouhuPipeline2': 302}}

    # 根据作者id，获取作者文章，搜狐限制单个作者最多只能检索1000篇
    def get_author_page_json():
        clien = pymongo.MongoClient(host=settings['MONGODB_HOST'], port=settings['MONGODB_PORT'])
        db = clien[settings['MONGODB_DBNAME']]
        coll = db[settings['MONGODB_COLNAME']]
        id_list = list(coll.distinct(key='authorId'))
        # print('总共作者数量为：', len(id_list))
        # coll.update({},{"$set":{"use":'1'}},multi=True)
        url_list = ['http://v2.sohu.com/author-page-api/author-articles/pc/114988?pNo=3']
        for author_id in id_list:
            author_id = str(author_id).strip()
            # print(author_id)
            if author_id:
                for i in range(2, 51):
                    url_list.append(
                        'http://v2.sohu.com/author-page-api/author-articles/pc/' + str(author_id) + '?pNo=' + str(i))
        # print('总共链接数量为：', len(url_list))
        return url_list

    start_urls = get_author_page_json()

    def parse(self, response):
        res_0 = response.body.decode('utf-8')
        res_data = json.loads(res_0)
        res_data = res_data['data']['pcArticleVOS']
        # print('-'*50,type(res_data))
        if res_data:
            return res_data


class SouhuspiderSpider3(scrapy.Spider):
    name = 'souhuspider3'
    allowed_domains = ['souhu.com']
    custom_settings = {'ITEM_PIPELINES': {'souhu.pipelines.SouhuPipeline3': 301}}

    start_urls = ['http://v2.sohu.com/public-api/articles/360550711/pv', ]
    base_site = 'http://v2.sohu.com/public-api/articles/'

    def get_id():
        """
        对于超大的表，采用生成器取数据，一次性取出来容易造成内存不足
        """
        client = pymongo.MongoClient(host=settings['MONGODB_HOST'], port=settings['MONGODB_PORT'])
        db = client[settings['MONGODB_DBNAME']]
        coll = db[settings['MONGODB_COLNAME2']]
        skip = settings['SKIP']
        count_all = coll.find({}, {'_id': 0, 'id': 1}).count()
        for i in range(int(count_all / skip)):
            list_id = coll.find().limit(skip).skip(skip * i)
            yield list(list_id)

    g = get_id()

    # fp = open('myjson.json', 'a', encoding='utf-8')

    def parse(self, response):
        # 返回文章id和阅读量
        res_0 = response.body.decode('utf-8')
        res_1 = response.url
        res_data = copy.copy(response.meta)
        url_id = re.search('[0-9]{5,}', res_1).group()
        res_data['read_cnt'] = res_0
        # 删除多余元素不必要的元素
        try:
            del  res_data['_id']
        except:
            pass
        del res_data['download_latency']
        del res_data['download_slot']
        del res_data['download_timeout']
        # self.fp.write(str(res_data)+'\n')
        yield res_data
        page_list = next(self.g)
        for page in page_list:
            url = self.base_site + str(page['id']) + '/pv'
            yield scrapy.Request(url, callback=self.parse, meta=page, dont_filter=True)


# def parse(self, response):
#     # 返回文章id和阅读量
#     res_0 = response.body.decode('utf-8')
#     res_1 = response.url
#     url_id = re.search('[0-9]{5,}', res_1).group()
#     res_data = {'read_cnt': res_0, 'id': url_id}
#     return res_data

# def get_page_read_cnt():
#     clien = pymongo.MongoClient(host=settings['MONGODB_HOST'], port=settings['MONGODB_PORT'])
#     db = clien[settings['MONGODB_DBNAME']]
#     coll = db[settings['MONGODB_COLNAME2']]
#     id_curse = coll.find({}, {'id': 1, '_id': 0})
#     id_list = list(id_curse)
#     url_list = []
#     for id_json in id_list:
#         if id_json:
#             url_list.append('http://v2.sohu.com/public-api/articles/' + str(id_json['id']) + '/pv')
#         # return url_list
#     # url_list.append('http://v2.sohu.com/public-api/articles/' + str(url_id) + '/pv')
#     return url_list
