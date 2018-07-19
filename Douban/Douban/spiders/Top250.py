# -*- coding: utf-8 -*-
import scrapy

from Douban.items import DoubanItem


class Top250Spider(scrapy.Spider):
    name = 'Top250'
    allowed_domains = ['movie.douban.com']

    offset=0
    url='https://movie.douban.com/top250?start='
    start_urls = [url+str(offset)]



    def parse(self, response):


        all_node=response.xpath('//div[@class="info"]')

        for node in all_node:
            item=DoubanItem()
            # //div[@class="info"]/div/a/span[@class="title"][1]/text()
            title=node.xpath('.//span[@class="title"][1]/text()').extract()[0]
            content=node.xpath('.//div[@class="bd"]/p/text()').extract()[0]
            content="".join(content).replace('\n',"")
            score=node.xpath('.//div[@class="star"]/span[2]/text()').extract()[0]
            info=node.xpath('.//p[@class="quote"]/span/text()').extract()

            if len(info)>0:
                info=info[0]

            item['title']=title
            item['content']=content
            item['score']=score
            item['info']=info

            yield item


        if self.offset<225:
            self.offset+=25


        next_url=self.url+str(self.offset)

        yield scrapy.Request(next_url,callback=self.parse)