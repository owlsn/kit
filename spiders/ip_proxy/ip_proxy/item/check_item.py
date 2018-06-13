# coding = utf-8

import scrapy

class CheckItem(scrapy.Item):

    delay = scrapy.Field()

    ip = scrapy.Field()

    port = scrapy.Field()

    status = scrapy.Field()