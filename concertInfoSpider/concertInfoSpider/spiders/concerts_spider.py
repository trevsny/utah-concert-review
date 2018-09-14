# -*- coding: utf-8 -*-
import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
# Need to figure out file path to import the Concert model in order to save to db
from concertInfoSpider.items import ConcertItem 
from datetime import datetime

class ConcertsSpider(scrapy.Spider):
    name = 'concerts'
    allowed_domains = [
        # 'www.usana-amp.com/events/', TODO usana's website no longer exists
        'thestateroom.com/shows'
    ]
    start_urls = [
        'http://thestateroom.com/shows'
    ]
    currentYear = datetime.now().year

    def start_requests(self):
        return [
            # scrapy.Request('http://thestateroom.com/shows', callback = self.parseSR, errback = self.errback),
            # scrapy.Request('http://www.vivintarena.com/events?event_type=Concert', callback = self.parseVivint, errback = self.errback),
            # scrapy.Request('https://www.egyptiantheatrecompany.org/', callback = self.parseEgyptian, errback = self.errback),
            # scrapy.Request('http://thecommonwealthroom.ticketfly.com/listing', callback = self.parseCommon, errback = self.errback),
            # scrapy.Request('https://www.kilbycourt.com/', callback = self.parseKilby, errback = self.errback),
            # scrapy.Request('http://maverikcenter.com/events-tickets/upcoming-events/', callback = self.parseMaverik, errback = self.errback),
            scrapy.Request('https://theunioneventcenter.com/upcomingevents/', callback = self.parseUnion, errback = self.errback)
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
        print("Inside the parseSR function")
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
            print("Crawled SR website")
            yield item
        
    def parseVivint(self, response):
        print("Inside the parseVivint function")
        # 1 Run extraction css selectors
        # 2 Place extracted data into the ConcertItem()
        
        artists = response.css(".title").css("h5::text").extract()
        days = response.css(".date").css("em::text").extract()
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
        # change number to month name
        for i in range(len(monthArray)):
            if monthArray[i] == '1':
                monthArray[i] = "January"
            elif monthArray[i] == '2':
                monthArray[i] = "February"
            elif monthArray[i] == '3':
                monthArray[i] = "March"
            elif monthArray[i] == '4':
                monthArray[i] = "April"
            elif monthArray[i] == '5':
                monthArray[i] = "May"
            elif monthArray[i] == '6':
                monthArray[i] = "June"
            elif monthArray[i] == '7':
                monthArray[i] = "July"
            elif monthArray[i] == '8':
                monthArray[i] = "August"      
            elif monthArray[i] == '9':
                monthArray[i] = "September"
            elif monthArray[i] == '10':
                monthArray[i] = "October"
            elif monthArray[i] == '11':
                monthArray[i] = "November"
            elif monthArray[i] == '12':
                monthArray[i] = "December"   
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
        # Change number to month name
        for i in range(len(monthArray)):
                    if monthArray[i] == '1':
                        monthArray[i] = "January"
                    elif monthArray[i] == '2':
                        monthArray[i] = "February"
                    elif monthArray[i] == '3':
                        monthArray[i] = "March"
                    elif monthArray[i] == '4':
                        monthArray[i] = "April"
                    elif monthArray[i] == '5':
                        monthArray[i] = "May"
                    elif monthArray[i] == '6':
                        monthArray[i] = "June"
                    elif monthArray[i] == '7':
                        monthArray[i] = "July"
                    elif monthArray[i] == '8':
                        monthArray[i] = "August"      
                    elif monthArray[i] == '9':
                        monthArray[i] = "September"
                    elif monthArray[i] == '10':
                        monthArray[i] = "October"
                    elif monthArray[i] == '11':
                        monthArray[i] = "November"
                    elif monthArray[i] == '12':
                        monthArray[i] = "December"
        images = response.css('.list-view-item').css('a').css('img::attr(src)').extract()
        ticket_links = response.css(".ticket-link").css("a::attr(href)").extract()
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
        # Change month abbreviations to full name
        for i in range(len(months)):
            if months[i] == "Jan":
                months[i] = "January"
            elif months[i] == "Feb":
                months[i] = "February"
            elif months[i] == "Mar":
                months[i] = "March"
            elif months[i] == "Apr":
                months[i] = "April"
            elif months[i] == "Jun":
                months[i] = "June"
            elif months[i] == "Jul":
                months[i] = "July"
            elif months[i] == "Aug":
                months[i] = "August"
            elif months[i] == "Sep":
                months[i] = "September"
            elif months[i] == "Oct":
                months[i] = "October"
            elif months[i] == "Nov":
                months[i] = "November"
            elif months[i] == "Dec":
                months[i] = "December"
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

    # TODO
    # USANA??? What the H happened to its website?
    #  ---TODO--
    # Park City Live
    # The Union
    # City Park, Cherry Peak Resort, Deer Valley
    # Saltair
    # Ogden Twilight
    # Kingsbury Hall
    # The Complex
    # Metro Music Hall
    # Sky SLC?? DJs
    # In the Venue
    # DeJoria Center
    # UVU center
    # Rice-Eccles Stadium
    # Lavell Edwards Stadium? Besides stadium of fire?
    # Scera Shell
    # Urban Lounge
    # Eccles Theater
    # Snow Basin Resort
    # Snow Park Amphitheater
    # Living Arenas
    # Utah Cultural Celebration Center
    # Velour
    # The Post Theater
    # Soundwell
    # The Royal
    # Tuacahn Amphitheater

#    TODO 
# Add Kenley Amphitheater 
# Add Sandy Amphitheater
# BlueBird Concert Series
# Red Butte Garden

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