# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ConcertItem(scrapy.Item):
    # define the fields for your item here like:
    venue = scrapy.Field()
    artist = scrapy.Field()
    month = scrapy.Field()
    day = scrapy.Field()
    image = scrapy.Field()
    ticket_link = scrapy.Field()
    
