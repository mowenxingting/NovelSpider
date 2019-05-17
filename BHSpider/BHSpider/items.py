# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NovelItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    novel_Url = scrapy.Field()
    novel_ID = scrapy.Field()
    novel_Author = scrapy.Field()
    novel_Name = scrapy.Field()
    novel_CoverURL = scrapy.Field()
    novel_Intro = scrapy.Field()
    novel_Type = scrapy.Field()
    novel_Style = scrapy.Field()
    novel_Isfinished = scrapy.Field()
    novel_Wordscount = scrapy.Field()
    novel_LatestUpdateTime=scrapy.Field()
class ChapterItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    novel_ID = scrapy.Field()
    chapter_ID = scrapy.Field()
    chapter_Url=scrapy.Field()
    chapter_Content=scrapy.Field()
    chapter_Title=scrapy.Field()