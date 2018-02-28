# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ExhibitorItem(scrapy.Item):
    title = scrapy.Field()
    html_detail = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)
