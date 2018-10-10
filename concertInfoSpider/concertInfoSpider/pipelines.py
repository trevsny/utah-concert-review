# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from concertInfoSpider.concertInfoSpider.items import ConcertItem
from concertInfoSpider.concertInfoSpider.spiders.concerts_spider import *
from apps.concertFinder.models import *

class ConcertinfospiderPipeline(object):
    # def __init__(self):
    
    # these functions are available in the pipeline
    # def from_crawler(cls, crawler):
   
    # def close_spider(self, spider):
    

    def process_item(self, item, spider):
        print("In process_item function")
        venues = ConcertVenue.objects.all()   
        existingConcerts = ConcertInfo.objects.all()
        # Check if concert already saved in db
        # Maybe refactor with an 'if any()' clause
        if existingConcerts:
            for i in range(len(existingConcerts)):
                if item['artist'] == existingConcerts[i].artist and item['venue'] == existingConcerts[i].venue.venue_name and item['month'] == existingConcerts[i].month and item['day'] == existingConcerts[i].day:
                    raise DropItem("Already in db") #end process_item function aka don't save to db
                else:
                    continue
            # Since db not empty now check for duplicate venues
            # Check to see if venue already exists in the db
            # Now that duplicates have been checked and the duplicates have been Dropped, create new entries
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
        else:
            newVenue = ConcertVenue.objects.create(venue_name = item['venue'])
            ConcertInfo.objects.create(venue = newVenue, artist = item['artist'], month = item['month'], day = item['day'], image = item['image'], ticket_link = item['ticket_link'])
            return item
          