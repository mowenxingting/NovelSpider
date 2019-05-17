import scrapy
import re
from scrapy.selector import Selector
from scrapy.http import HtmlResponse,Request
from BHSpider.items import NovelItem,ChapterItem
import datetime

class BHSpider(scrapy.Spider):
    name='BHSpider'
    allowed_domains=['www.baihexs.com']
    start_urls=['http://www.baihexs.com/book/72610.html',]
    #重写发出请求的方法，设置时间限制
    def make_requests_from_url(self, url):
        self.logger.debug('Try first time')
        return scrapy.Request(url=url, meta={'download_timeout': 30}, callback=self.parse, dont_filter=False)

    def parse(self,response):
        sel = Selector(response)
        if(re.match(r'(https?\:\/\/)?www\.baihexs\.com\/book\/\d+\.html',response.url)):
            novel_item=NovelItem()
            novel_item['novel_Url'] =response.url
            novel_item['novel_ID'] =response.url.split('/')[-1].split('.')[0]
            novel_item['novel_Author'] =sel.xpath('//div[@id="author"]/a/text()').extract()[0]
            novel_item['novel_Name'] =sel.xpath('//h1/text()').extract()[0]
            novel_item['novel_CoverURL'] =sel.xpath('//div[@id="bookimg"]/img/@src').extract()[0]
            novel_item['novel_Intro'] =''.join(''.join(sel.xpath('//div[@id="bookintro"]/p/text()').extract()).split())
            novel_item['novel_Type'] =sel.xpath('//div[@id="count"]/span[1]/text()').extract()[0]
            novel_item['novel_Isfinished'] =sel.xpath('//div[@id="count"]/span[6]/text()').extract()[0]
            novel_item['novel_Wordscount'] =int(sel.xpath('//div[@id="count"]/span[5]/text()').extract()[0][:-1])*1000
            # novel_item['novel_LatestUpdateTime'] =datetime.datetime.strptime(sel.xpath('//div[@class="new"]/span[1]/text()').extract()[0].split('：')[1].strip(),'%Y-%m-%d')
            novel_item['novel_LatestUpdateTime'] = sel.xpath('//div[@class="new"]/span[1]/text()').extract()[0].split('：')[1].strip()
            yield novel_item
        # elif(re.match(r'(https?\:\/\/)?www\.baihexs\.com\/\d+/\d+/\d+\.html',response.url)):
        #     chapter_item=ChapterItem()
        #     chapter_item['novel_ID'] =response.url.split('/')[-2]
        #     chapter_item['chapter_ID'] =response.url.split('/')[-1].split('.')[0]
        #     chapter_item['chapter_Url'] =response.url
        #     chapter_item['chapter_Title'] =sel.xpath('//h1/text()').extract()[0]
        #     chapter_item['chapter_Content'] =''.join(sel.xpath('//div[@id="content"]').xpath('string(.)').extract()[0].split())
        #     yield chapter_item
        else:
            pass
        all_urls = sel.xpath('//a/@href').extract()  # 提取界面所有的url
        for url in all_urls:
            if re.match(r'^/.+',url):
                url= response.urljoin(url)
            if url.startswith("http://www.baihexs.com/") or url.startswith("https://www.baihexs.com/") and not re.match(r'(https?\:\/\/)?www\.baihexs\.com\/\d+/\d+(/\d+\.html)?',url):
                # 回调函数默认为parse,也可以通过from scrapy.http import Request来指定回调函数
                # yield Request(url, callback=self.parse)
                yield self.make_requests_from_url(url)