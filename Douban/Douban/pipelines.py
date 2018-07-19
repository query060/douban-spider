# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from pymongo import MongoClient
from douban.settings import MONGO_HOST
from douban.settings import MONGO_PORT
from douban.settings import MONGO_DBNAME
from douban.settings import SHEET_NAME

# MONGO_HOST='127.0.0.1'
# MONGO_PORT=27017
# MONGO_DBNAME='douban'
# SHEET_NAME='doubanPosition'


class DoubanMongoPipeline(object):
    def open_spider(self, spider):
        client = MongoClient(MONGO_HOST, MONGO_PORT)

        dbname = client[MONGO_DBNAME]
        self.collection=dbname[SHEET_NAME]

    def process_item(self, item, spider):
        python_dict = dict(item)

        self.collection.insert_one(python_dict)

        return item

    def close_spider(self, spider):
        pass



class DoubanPipeline(object):


    def open_spider(self,spider):
        self.file=open(spider.name+'.json','w',encoding='utf-8')

    def process_item(self, item, spider):

        python_dict=dict(item)

        python_str=json.dumps(python_dict,ensure_ascii=False)+'\n'

        self.file.write(python_str)

        return item

    def close_spider(self,spider):
        self.file.close()