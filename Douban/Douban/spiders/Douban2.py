# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from douban.items import DoubanItem


class Douban2Spider(CrawlSpider):
    name = 'Douban2'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250?start=0']
    # offset=0

    # url='https://movie.douban.com/top250?start='


    rules = (

        Rule(LinkExtractor(allow=r'start='), callback='parse_item', follow=True),

    )




    def parse_item(self, response):
        # i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        # return i
        all_movies = response.xpath('//div[@class="info"]')
        print(all_movies)
        for movie in all_movies:
            item = DoubanItem()

            title = movie.xpath('.//span[@class="title"][1]/text()').extract()[0]
            content = movie.xpath('./div[@class="bd"]/p/text()').extract_first('')
            content = content.replace('\n', '').replace('\r', '')
            score = movie.xpath('.//span[@class="rating_num"]/text()').extract()[0]
            info = movie.xpath('.//p[@class="quote"]/span/text()').extract()

            if len(info) > 0:
                info = info[0]

            item['title'] = title
            item['content'] = content
            item['score'] = score
            item['info'] = info

            print(item)

            yield item
