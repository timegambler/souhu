import pymongo
import copy
import logging
import scrapy
import json
from scrapy.utils.project import get_project_settings
import pymongo
import re
from scrapy_redis.spiders import RedisSpider

settings = get_project_settings()


class SouhuspiderSpider4(RedisSpider):
    name = 'souhuspider4'
    allowed_domains = ['souhu.com']  # redis允许静态写
    redis_key = "souhuspider4:strat_urls"
    custom_settings = {'ITEM_PIPELINES': {'souhu.pipelines.SouhuPipeline3': 303}}

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
            del res_data['_id']
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
