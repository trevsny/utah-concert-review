# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from concertInfoSpider.items import ConcertItem
from concertInfoSpider.spiders.concerts_spider import *
from apps.concertFinder.models import *

class ConcertinfospiderPipeline(object):
    # def __init__(self):
        # self.setupDBCon()
        # self.createTables()

    # these functions are available in the pipeline
    # def from_crawler(cls, crawler):
   
    # def close_spider(self, spider):
    

    def process_item(self, item, spider):
        print("Show me the money Jerry", item)
        # self.storeInDb(**item)
        venues = ConcertVenue.objects.all()
        for ven in venues:
            concertVenueExists = False
            if item['venue'] == ven.venue_name:
                ConcertInfo.objects.create(venue = ven, artist = item['artist'], month = item['month'], day = item['day'], image = item['image'], ticket_link = item['ticket_link'])
                concertVenueExists = True
                break
        if concertVenueExists:
            return item
        else:
            newVenue = ConcertVenue.objects.create(venue_name = item['venue'])
            ConcertInfo.objects.create(venue = newVenue, artist = item['artist'], month = item['month'], day = item['day'], image = item['image'], ticket_link = item['ticket_link'])
            return item