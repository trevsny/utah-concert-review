# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from concertInfoSpider.items import ConcertItem
from concertInfoSpider.spiders.concerts_spider import *
import json
import sqlite3 as lite


# con = None #db connection object - created on init and deleted on __del__

class ConcertinfospiderPipeline(object):
    def __init__(self):
        self.setupDBCon()
        self.createTables()

    # these functions are available in the pipeline
    # def from_crawler(cls, crawler):
   
    # def close_spider(self, spider):
    

    def process_item(self, item, spider):
        print("Show me the money Jerry", item)
        # newItem = ConcertItem(artist = item['artist'], month = item['month'], day = item['day'])
        # print("Printing the newItem after instantiating a new object of the ConcertItem class", newItem)
        
        self.storeInDb(**item)
        return item

    def storeInDb(self, item):
        self.storeConcertInfoInDb(**item)

    def storeConcertInfoInDb(self, **item):
        # cur = self.con.cursor()
        self.cur.execute("INSERT INTO Concerts(\
            artist, \
            month, \
            day, \
            ticket_link)\
        VALUES( ?, ?, ?, ?)", \
        (\
            item.get("artist",""),
            item.get('month', ""),
            item.get('day',""),
            item.get('ticket_link',"")
        ))
        self.con.commit()

    def setupDBCon(self):
        # self.con = lite.connect('test.db')
        self.con = lite.connect('../db.sqlite3')
        self.cur = self.con.cursor()
        
        
    def __del__(self):
        self.closeDB()
    
    def createTables(self):
        self.dropConcertsTable()
        self.createConcertsTable()

    def createConcertsTable(self):
        # cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS Concerts(id INTEGER PRIMARY KEY NOT NULL, \
        artist TEXT, \
        month TEXT, \
        day TEXT, \
        ticket_link TEXT)")

    def dropConcertsTable(self):
        # cur = self.con.cursor()
        self.cur.execute("DROP TABLE IF EXISTS Concerts")

    def closeDB(self):
        self.con.close()