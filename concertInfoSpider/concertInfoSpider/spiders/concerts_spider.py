# -*- coding: utf-8 -*-
import scrapy
import re
# from scrapy_splash import SplashRequest
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
# Need to figure out file path to import the Concert model in order to save to db
from concertInfoSpider.items import ConcertItem 
from datetime import datetime

class ConcertsSpider(scrapy.Spider):
    name = 'concerts'
    # allowed_domains = [
    #     # 'www.usana-amp.com/events/', TODO usana's website no longer exists
    #     'thestateroom.com/shows'
    # ]
    # start_urls = [
    #     'http://thestateroom.com/shows'
    # ]
    currentYear = datetime.now().year

    def start_requests(self):
        return [
            scrapy.Request('http://thestateroom.com/shows', callback = self.parseSR, errback = self.errback),
            scrapy.Request('http://www.vivintarena.com/events?event_type=Concert', callback = self.parseVivint, errback = self.errback),
            scrapy.Request('https://www.egyptiantheatrecompany.org/', callback = self.parseEgyptian, errback = self.errback),
            scrapy.Request('http://thecommonwealthroom.ticketfly.com/listing', callback = self.parseCommon, errback = self.errback),
            scrapy.Request('https://www.kilbycourt.com/', callback = self.parseKilby, errback = self.errback),
            scrapy.Request('http://maverikcenter.com/events-tickets/upcoming-events/', callback = self.parseMaverik, errback = self.errback),
            scrapy.Request('https://theunioneventcenter.com/upcomingevents/', callback = self.parseUnion, errback = self.errback),
            scrapy.Request('https://tickets.utah.edu/category/events/', callback = self.parseKingsbury, errback = self.errback),
            scrapy.Request('https://tickets.utah.edu/category/events/page/2/', callback = self.parseKingsbury, errback = self.errback),
            scrapy.Request('https://tickets.utah.edu/category/events/page/3/', callback = self.parseKingsbury, errback = self.errback),
            scrapy.Request('https://tickets.utah.edu/category/events/page/4/', callback = self.parseKingsbury, errback = self.errback),
            scrapy.Request('http://www.thecomplexslc.com/', callback = self.parseComplex, errback = self.errback),
            scrapy.Request('https://www.metromusichall.com/', callback = self.parseMetro, errback = self.errback),
            scrapy.Request('http://www.theurbanloungeslc.com/', callback = self.parseUrbanL, errback = self.errback),
            # SplashRequest('http://soundwellslc.com/', callback = self.parseSoundwell, args = { 'wait': 0.5})
        ]
    
    def errback (self, failure):
        # log all failures
        self.logger.error(repr(failure))
        # in case you want to do something special for some errors,
        # you may need the failure's type:
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)
        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
       

        
    # State Room parse -- was called parseSR

    def parseSR(self, response):
        venue = "The State Room"
        artists = response.css(".event_detail_title").css("span::text").extract()
        dates = response.css("h3").css("span::text").extract()
        # separate month and day from the start time and blank space extracted
        array = []
        for date in dates:
            if 'pm' in date:
                continue
            elif date == " ":
                continue
            elif ' ' in date:
                array.append(date)
        # separate month and day so each can be saved individually in db
        monthArray = []
        dayArray = []
        yearArray = []
        for date in array:
            head,sep,tail = date.partition(', ')
            yearArray.append(tail)
            newdate = head
            head,sep,tail = newdate.partition(' ')
            # monthArray returns ['August','','September,''].  Need to eliminate ''
            if head == "":
                continue
            else:
                monthArray.append(head)
                # 
            if tail == " ":
                continue
            else:
                dayArray.append(tail)
        # change month name to int for db
        monthArray = self.changeMonthNameToNumber(monthArray)
        # change days to int for db
        dayArray = list(map(int, dayArray))
        ticket_links = response.css(".ohanah-registration-link").css("a::attr(href)").extract()
        # --images-- must put http://thestateroom.com before the link
        images = response.css(".ohanah_modal::attr(href)").extract()

        for i in range(len(artists)):
            item = ConcertItem()
            item['venue'] = "The State Room"
            item['artist'] = artists[i]
            item['month'] = monthArray[i]
            item['day'] = dayArray[i]
            item['year'] = yearArray[i]
            item['image'] = 'http://thestateroom.com' + images[i]
            item['ticket_link'] = ticket_links[i]
            yield item
        
    def parseVivint(self, response):
        print("Inside the parseVivint function")
        # 1 Run extraction css selectors
        # 2 Place extracted data into the ConcertItem()
        
        artists = response.css(".title").css("h5::text").extract()
        days = response.css(".date").css("em::text").extract()
        # change days (strings) to int for db
        days = list(map(int, days))
        images = response.css(".synopsis").css("img::attr(src)").extract()
        # ticket_links get extracted as 'url', '/tickets', 'url', '/tickets.  Ignore the '/tickets'
        ticket_links = []
        tickets = response.css(".tickets").css("a::attr(href)").extract() 
        for ticket in tickets:
            if ticket == '/tickets':
                continue
            else:
                ticket_links.append(ticket)
        # Sometimes the artists and ticket_links quantities don't match up
        differenceInLengths = len(artists) - len(ticket_links)
        if differenceInLengths >= 1:
            for i in range(0,differenceInLengths):
                # Generic link for buying tickets at Vivint Arena
                ticket_links.append('https://www.ticketmaster.com/new/venue/246072?_ga=2.28280443.630826876.1536686741-1322752007.1534960663&x-flag-desktop=true&m_efeat6690v1desktop&x-flag-desktop-ads-variant=3')
        # Setting data 
        for i in range(len(artists)):
            item = ConcertItem()
            item['venue'] = "Vivint Arena"
            item['artist'] = artists[i]
            item['month'] = "Manually input"
            item['day'] = days[i]
            item['year'] = self.currentYear
            item['image'] = images[i]
            item['ticket_link'] = ticket_links[i]
            yield item
    # Note to self.  Must manually input month names for all Vivint concerts
    def parseEgyptian(self, response):
        artists = response.css(".event_info").css("h2::text").extract()
        images = response.css('.flyer').css('a').css('img::attr(src)').extract()
        ticket_links = response.css(".event_info").css("a::attr(href)").extract()
        for i in range(len(artists)):
            item = ConcertItem()
            item['venue'] = "The Egyptian"
            item['artist'] = artists[i]
            item['month'] = "Manually input"
            item['day'] = "Manually input"
            item['year'] = self.currentYear
            item['image'] = images[i]
            item['ticket_link'] = ticket_links[i]
            yield item
    # The Commonwealth Room
    def parseCommon(self, response):
        artists = response.css(".headliners.summary").css('a::text').extract()
        initialArray = response.css(".dates::text").extract()
        monthArray = []
        dayArray = []
        # Separate the day and month
        for i in range(len(initialArray)):
            head, sep, tail = initialArray[i].partition(' ')
            head, sep, tail = tail.partition('.')
            monthArray.append(head)
            dayArray.append(tail)
        # resulting month number is a string - make it an int
        monthArray = list(map(int, monthArray))
        # change day number string to an int
        dayArray = list(map(int, dayArray))
        images = response.css(".list-view-item").css('a').css('img::attr(src)').extract()
        ticket_links = response.css(".ticket-link").css("a::attr(href)").extract()
        # If a show is sold out then the ticket_link goes away
        differenceInLengths = len(artists) - len(ticket_links)
        if differenceInLengths >= 1:
            for i in range(0,differenceInLengths):
                ticket_links.append("http://thecommonwealthroom.ticketfly.com/listing")
        # send data to pipeline
        for i in range(len(artists)):
            item = ConcertItem()
            item['venue'] = "The Commonwealth Room"
            item['artist'] = artists[i]
            item['month'] = monthArray[i]
            item['day'] = dayArray[i]
            item['year'] = self.currentYear
            item['image'] = images[i]
            item['ticket_link'] = ticket_links[i]
            yield item

    # Kilby Court
    def parseKilby(self, response):
        artists = response.css(".headliners.summary").css('a::text').extract()
        initialArray = response.css(".dates::text").extract()
        monthArray = []
        dayArray = []
        # Separate month and day
        for i in range(len(initialArray)):
            head, sep, tail = initialArray[i].partition(', ')
            head, sep, tail = tail.partition('/')
            monthArray.append(head)
            dayArray.append(tail)
        # Change month name to a number for db
        monthArray = self.changeMonthNameToNumber(monthArray)
        # Change day str to int
        dayArray = list(map(int, dayArray))
        images = response.css('.list-view-item').css('a').css('img::attr(src)').extract()
        ticket_links = response.css(".ticket-link").css("a::attr(href)").extract()
        # Data to send to pipelines.py
        for i in range(len(artists)):
            item = ConcertItem()
            item['venue'] = "Kilby Court"
            item['artist'] = artists[i]
            item['month'] = monthArray[i]
            item['day'] = dayArray[i]
            item['year'] = self.currentYear
            item['image'] = images[i]
            item['ticket_link'] = ticket_links[i]
            yield item

    # Maverik Center
    def parseMaverik(self, response):
        artists = response.css(".data-info").css("h4::text").extract()
        initialArray = response.css(".data-info").css("h5::text").extract()
        dateArray = []
        dayArray = []
        monthArray = []
        yearArray = []
        for i in range(len(initialArray)):
            if i % 2 == 0:
                dateArray.append(initialArray[i])

        for date in dateArray:
            head, sep, tail = date.partition(' ')
            monthArray.append(head)
            head, sep, tail = tail.partition(', ')
            dayArray.append(head)
            yearArray.append(tail)
        # Change month name to number for db
        monthArray = self.changeMonthNameToNumber(monthArray)
        # Change day str to int
        dayArray = list(map(int, dayArray))
        images = response.css('.image').css('img::attr(src)').extract()
        ticketArray = response.css(".buttons").css("a::attr(href)").extract()
        ticket_links = []
        for i in range(len(ticketArray)):
            if i % 2 == 0:
                ticket_links.append(ticketArray[i])
        differenceInLengths = len(artists) - len(ticket_links)
        if differenceInLengths >= 1:
            for i in range(0,differenceInLengths):
                ticket_links.append("http://maverikcenter.com/events-tickets/upcoming-events/")
        # Send data to pipeline
        for i in range(len(artists)):
            item = ConcertItem()
            item['venue'] = "Maverik Center"
            item['artist'] = artists[i]
            item['month'] = monthArray[i]
            item['day'] = dayArray[i]
            item['year'] = yearArray[i]
            item['image'] = images[i]
            item['ticket_link'] = ticket_links[i]
            yield item

    # The Union event center
    def parseUnion(self, response):
        artists = response.css('.eventlist-event--upcoming').css('h1').css('a::text').extract()
        months = response.css(".eventlist-datetag-startdate--month::text").extract()
        days = response.css(".eventlist-datetag-startdate--day::text").extract()
        images = response.css('.eventlist-event--upcoming').css('img::attr(data-src)').extract()
        ticket_links = response.css('.eventlist-event--upcoming').css('.eventlist-column-info').css('.eventlist-excerpt').css('a::attr(href)').extract()
        # Change month abbreviations to number
        months = self.changeMonthNameToNumber(months)
        # Change days strings to ints
        days = list(map(int, days))
        # If a sold out show exists
        differenceInLengths = len(artists) - len(ticket_links)
        if differenceInLengths >= 1:
            for i in range(0,differenceInLengths):
                ticket_links.append("https://theunioneventcenter.com/upcomingevents/")
        # Send data to pipeline
        for i in range(len(artists)):
            item = ConcertItem()
            item['venue'] = "The Union"
            item['artist'] = artists[i]
            item['month'] = months[i]
            item['day'] = days[i]
            item['year'] = self.currentYear
            item['image'] = images[i]
            item['ticket_link'] = ticket_links[i]
            yield item

    # Kingsbury Hall
    def parseKingsbury(self, response):
        venues = response.css(".eq-ht").css('.venue::text').extract()
        artists = response.css(".eq-ht").css('h3::text').extract()
        months = response.css(".eq-ht").css('.event-month::text').extract()
        days = response.css(".eq-ht").css('.event-day::text').extract()
        images = response.css(".eq-ht").css('img::attr(src)').extract()
        ticket_links = response.css(".eq-ht").css('a::attr(href)').extract()
        # change month abbreviations to number
        months = self.changeMonthNameToNumber(months)
        # Change days strings to ints
        days = list(map(int, days))
        # send data to pipeline
        for i in range(len(artists)):
            item = ConcertItem()
            item['venue'] = venues[i]
            item['artist'] = artists[i]
            item['month'] = months[i]
            item['day'] = days[i]
            item['year'] = self.currentYear
            item['image'] = images[i]
            item['ticket_link'] = ticket_links[i]
            yield item
    # The Complex
    def parseComplex(self, response):
        artists = response.css('.inner-box').css('.content').css('h3::text').extract()
        images = response.css('.portfolio-item').css('.image-box').css('img::attr(src)').extract()
        ticket_links = response.css('.inner-box').css('.content').css('a::attr(href)').extract()
        # Extracts month, day, and exact venue within The Complex
        initialArray = response.css('.inner-box').css('.content').css('h4::text').extract()
        dateArray = []
        dayArray = []
        monthArray = []
        for i in range(len(initialArray)):
            if i % 2 == 0:
                dateArray.append(initialArray[i])

        for date in dateArray:
            head, sep, tail = date.partition(' ')
            head, sep, tail = tail.partition(' ')
            monthArray.append(head)
            onlyInt = re.split('(\d+)',tail)
            dayArray.append(onlyInt[1])
        # Change month name to an int for db
        monthArray = self.changeMonthNameToNumber(monthArray)
        # Change day strings to ints
        dayArray = list(map(int, dayArray))

        # send data to pipeline
        for i in range(len(artists)):
            item = ConcertItem()
            item['venue'] = "The Complex"
            item['artist'] = artists[i]
            item['month'] = monthArray[i]
            item['day'] = dayArray[i]
            item['year'] = self.currentYear
            item['image'] = images[i]
            item['ticket_link'] = ticket_links[i]
            yield item

    # Metro Music Hall
    def parseMetro(self, response):
        artists = response.css('.list-view-details').css('.headliners').css('a::text').extract()
        # Returns day of week and date as 9/19
        dateArray = response.css('.list-view-details').css('.dates::text').extract()
        monthArray = []
        dayArray = []
        # separate out month from day
        for date in dateArray:
            head, sep, tail = date.partition(', ')
            head, sep, tail = tail.partition('/')
            monthArray.append(head)
            dayArray.append(tail)
        # Change month name to an int for db
        monthArray = self.changeMonthNameToNumber(monthArray)
        # Change day string to int
        dayArray = list(map(int, dayArray))
        images = response.css('.list-view-item').css('a').css('img::attr(src)').extract()
        ticket_links = response.css('.ticket-link').css('.primary-link').css('a::attr(href)').extract()
        # send data to pipeline
        for i in range(len(artists)):
            item = ConcertItem()
            item['venue'] = "Metro Music Hall"
            item['artist'] = artists[i]
            item['month'] = monthArray[i]
            item['day'] = dayArray[i]
            item['year'] = self.currentYear
            item['image'] = images[i]
            # Sometimes ticket_link array errors 'list index out of range'
            item['ticket_link'] = ticket_links[i]
            yield item

        #  The Urban Lounge
    def parseUrbanL(self, response):
        artists = response.css(".list-view-details").css(".headliners").css("a::text").extract()
        # Returns array with day of week, month/day
        dateArray = response.css(".list-view-details").css(".dates::text").extract()
        # Separate month from day
        monthArray = []
        dayArray = []
        for date in dateArray:
            head, sep, tail = date.partition(', ')
            head, sep, tail = tail.partition('/')
            monthArray.append(head)
            dayArray.append(tail)
        # change month number from string to int
        monthArray = list(map(int, monthArray))
        # change day number from str to int
        dayArray = list(map(int, dayArray))
        images = response.css('.list-view-item').css('a').css('img::attr(src)').extract()
        ticket_links = response.css('.ticket-price').css('a::attr(href)').extract()
        # send data to pipeline
        for i in range(len(artists)):
            item = ConcertItem()
            item['venue'] = "The Urban Lounge"
            item['artist'] = artists[i]
            item['month'] = monthArray[i]
            item['day'] = dayArray[i]
            item['year'] = self.currentYear
            item['image'] = images[i]
            item['ticket_link'] = ticket_links[i]
            yield item

    # Soundwell -JS rendered page
    # def parseSoundwell(self, response):
    #     print("In parseSoundwell function")
    #     print(response.css('h3::text').extract())
    
    def changeMonthNameToNumber(self, monthArray):
        for in range(len(monthArray)):
            if monthArray[i] == "January" or monthArray[i] =="Jan":
                monthArray[i] = 1
            elif monthArray[i] == "February" or monthArray[i] =="Feb":
                monthArray[i] = 2
            elif monthArray[i] == "March" or monthArray[i] =="Mar":
                monthArray[i] = 3
            elif monthArray[i] == "April" or monthArray[i] =="Apr":
                monthArray[i] = 4
            elif monthArray[i] == "May":
                monthArray[i] = 5
            elif monthArray[i] == "June" or monthArray[i] =="Jun":
                monthArray[i] = 6
            elif monthArray[i] == "July" or monthArray[i] =="Jul":
                monthArray[i] = 7
            elif monthArray[i] == "August" or monthArray[i] =="Aug":
                monthArray[i] = 8
            elif monthArray[i] == "September" or monthArray[i] =="Sep" or monthArray[i] == "Sept":
                monthArray[i] = 9
            elif monthArray[i] == "October" or monthArray[i] == "Oct":
                monthArray[i] = 10
            elif monthArray[i] == "November" or monthArray[i] == "Nov":
                monthArray[i] = 11
            elif monthArray[i] == "December" or monthArray[i] == "Dec":
                monthArray[i] = 12
        return monthArray

   
# TODO Add these sites to be scraped in version 2.0
# Kenley Amphitheater 
# Sandy Amphitheater
# BlueBird Concert Series
# Red Butte Garden
# Ogden Twilight
# Saltair
# Park City Live
# City Park, Cherry Peak Resort, Deer Valley
# Utah Symphony??
# Sky SLC?
# In the venue...couldn't access website
# Snow Park Amphitheater -- http://www.deervalley.com/WhatToDo/Summer/Amphitheater -- http://www.parkcitylivemusic.com/venues/snow-park-outdoor-amphitheater-at-deer-valley-resort



# Kenley Amphitheater ---- http://www.davisarts.org/summer-concert-series/
    # ---artists---delete the last one because it brings up Subscription Details and not an artist
    # response.css(".entry-title").css("a::text").extract()
    # ---date---first 3 words in p tag text is the date "August 25,2018 | blah blah..."
    # response.css(".post-content").css("p::text").extract()
    # ---ticket_link--- no need to extract
    #  https://tickets.davisarts.org/
    # --image-- dont save last result
    # response.css(".et_pb_image_container").css("img::attr(src)").extract()


    # Sandy Amphitheater --- https://sandyamp.com/events
    #  ---artists---date---time
    # response.css(".item-title::text").extract()
    # Figure out how to separately save words from that...convert each word in a list? and then pop, etc.?
    # --ticket-link-- all the same for every concert
    # https://sandyamp.com/ticket-info   is a redirect to smithtixs
    # --image-- add https://sandyamp.com to all links pulled
    

    # Sundance Bluebird Concert Series --- https://www.sundanceresort.com/events/bluebird/
    # ---dates--- (month and day)
    # response.css("li").css("strong::text").extract()
    # ---artists--- Might require manual input...doable because only 4-5 shows during the summer. Could use .join on \n to eliminate extra space.
    # --ticket_link--- 
    # response.css(".button.button--secondary").css("a::attr(href)").extract() 

    # Red Butte Garden --- https://www.redbuttegarden.org/concerts/
    # --- artists--- for some reason it gathers all of them, past and future
    # response.css(".con-title.caps").css("a::text").extract()
    # ---date--- day of week/month/day ---need to split up month and day 
    # response.css(".con-date::text").extract()
    # ---ticket_link--- all the same
    # https://redbuttegarden.ticketfly.com

  # Owl Bar in Sundance --- https://www.sundanceresort.com/events/owl-bar-live-music/
    # ---dates and artists --- eliminate first p tag since it isn't an artist or date
    # response.css(".Main__contentWrapper").css("p::text").extract()
    # some .join may be required for artists
    # --ticket_link--- no tickets to buy just cover charge at the door
    
    # All of Park City events  --- https://www.visitparkcity.com/events/music-and-concerts/