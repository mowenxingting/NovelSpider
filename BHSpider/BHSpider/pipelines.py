# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector
import BHSpider.settings
from BHSpider.items import NovelItem,ChapterItem
import json
from scrapy.exceptions import DropItem
import BHSpider.settings as settings
import codecs
import logging
import requests
# import urllib
import os

# 去重过滤器
class DuplicatesPipeline(object):
    def __init__(self):
        self.novel_ids_seen = set()
        self.chapter_ids_seen = set()

    def process_item(self, item, spider):
        if isinstance(item, NovelItem):
            if item['novel_ID'] in self.novel_ids_seen:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.novel_ids_seen.add(item['novel_ID'])
                return item
        else:
            if item['chapter_ID'] in self.chapter_ids_seen:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.chapter_ids_seen.add(item['chapter_ID'])
                return item

# Json存储过滤器
class JsonWriterPipeline(object):
    '''保存到文件中对应的class
       1、在settings.py文件中配置
       2、在自己实现的爬虫类中yield item,会自动执行'''
    def __init__(self):
        self.file=codecs.open("novels_chapters.json", 'a', encoding='utf-8')
        # self.file = open('info.json', 'a', encoding='utf-8')#保存为json文件
    def process_item(self, item, spider):
        line=json.dumps(dict(item),ensure_ascii=False)+ "\n"
        self.file.write(line) #转为json的
        return item
    def spider_closed(self, spider):#爬虫结束时关闭文件
        self.file.close()

class BhspiderPipeline(object):
    # def process_item(self, item, spider):
    #     return item

    def __init__(self):
        pass

    def process_item(self, item, spider):
        conn = mysql.connector.connect(user=settings.db_configs['db_user'],
                                       password=settings.db_configs['db_password'],
                                       database=settings.db_configs['db_name'])
        cursor = conn.cursor()
        try:
            print('item=',item)
            if isinstance(item, NovelItem):
                sql="insert into novels( novel_Url , novel_ID , novel_Author , novel_Name , novel_CoverURL , novel_Intro , novel_Type , novel_Isfinished , novel_Wordscount , novel_LatestUpdateTime) values ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )"
                params = (item["novel_Url"], item["novel_ID"], item["novel_Author"], item["novel_Name"], item["novel_CoverURL"],item["novel_Intro"], item["novel_Type"], item["novel_Isfinished"],item["novel_Wordscount"], item["novel_LatestUpdateTime"])
            else :
                sql='insert into chapters( novel_ID , chapter_ID , chapter_Url , chapter_Content, chapter_Title ) values ( %s, %s, %s, %s, %s )'
                params=(item['novel_ID'] , item['chapter_ID'] , item['chapter_Url'] , item['chapter_Content'], item['chapter_Title'])
            insert = cursor.execute(sql, params)
            conn.commit()
            return item
        except Exception:
            print('--------------database operation exception!!-----------------')
            print(Exception)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

class PicPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item,NovelItem) and item["novel_CoverURL"]:
            if item["novel_CoverURL"].split('/')[-1]=='nocover.jpg':
                pass
            else:
                try:
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'}
                    res = requests.get(item['novel_CoverURL'], headers=headers)
                    # req = urllib.request.Request(url=item['addr'], headers=headers)
                    # res = urllib.request.urlopen(req)
                    img_name = item['novel_ID'] + item['novel_Name'] + '.' + item["novel_CoverURL"].split('.')[-1]
                    file_name = os.path.join(r'F:\Python-Test-Examples\BHSpider\Covers', img_name)
                    with open(file_name, 'wb') as fp:
                        fp.write(res.content)
                except Exception:
                    print ('--------------image save exception!!-----------------')
                    print(file_name)
                    print(Exception)
        return item