# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import copy
import logging
import shutil
import pymongo
from scrapy.conf import settings
import re
from scrapy.exceptions import DropItem


class SouhuPipeline1(object):
    def process_item(self, item, spider):
        clien = pymongo.MongoClient(host=settings['MONGODB_HOST'], port=settings['MONGODB_PORT'])
        db = clien[settings['MONGODB_DBNAME']]
        coll = db[settings['MONGODB_COLNAME']]
        try:
            str_item = str(item)
            au_id_list = re.findall('\'authorId\': [0-9]*', str_item)
            au_id = au_id_list[0].split(':')[1]
            coll.insert_one({'authorId': au_id, 'use': '0'})
        except Exception as err:
            pass
        return item


class SouhuPipeline2(object):
    def process_item(self, item, spider):
        total, used, free = shutil.disk_usage("/")
        # 监测剩余空间，当前剩余空间 小于时，停止爬虫
        free_space = free // (2 ** 30)
        if free_space < settings['FREE_SPACE']:
            spider.crawler.engine.close_spider(spider, '空间不足，关闭爬虫')
        else:
            try:
                clien = pymongo.MongoClient(host=settings['MONGODB_HOST'], port=settings['MONGODB_PORT'])
                db = clien[settings['MONGODB_DBNAME']]
                coll = db[settings['MONGODB_COLNAME2']]
                coll.insert(item)
            except Exception as err:
                # print(err)
                pass

        return item


# 定义一个全局变量，等到每次积攒到10000条时再插入数

class SouhuPipeline3(object):
    item_list = []
    """
    对于一个大的表，使用insert远远优于update
    """

    def process_item(self, item, spider):
        clien = pymongo.MongoClient(host=settings['MONGODB_HOST'], port=settings['MONGODB_PORT'])
        db = clien[settings['MONGODB_DBNAME']]
        coll = db[settings['MONGODB_COLNAME3']]
        coll.insert(item)
        # self.item_list.append(item)
        # if len(self.item_list) > 100:
        #     lit = copy.deepcopy(self.item_list)
        #     lit = [item for item in lit if lit.count(item) == 1]
        #     try:
        #         self.coll.insert_many(lit)
        #         lit[:] = []
        #         self.item_list = lit
        #     except Exception as err:
        #         print(err)
        #         lit[:] = []
        #         self.item_list = lit

        # coll.update_one({'id': int(item['id'])}, {'$set': {'read_cnt': str(item['read_cnt'])}})
        return item


class DuplicatesPipeline(object):
    """
    去重并且聚集数据
    """

    def __init__(self):
        self.ids_seen = set()
        self.item_list = []

    clien = pymongo.MongoClient(host=settings['MONGODB_HOST'], port=settings['MONGODB_PORT'])
    db = clien[settings['MONGODB_DBNAME']]
    coll = db[settings['MONGODB_COLNAME3']]

    def process_item(self, item, spider):
        if item['id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['id'])
            self.item_list.append(item)
            if len(self.item_list) > 30:
                lit = copy.deepcopy(self.item_list)
                try:
                    self.coll.insert_many(lit)
                except Exception as err:
                    print(err)
                    lit[:] = []
                    self.item_list = lit

            return item
