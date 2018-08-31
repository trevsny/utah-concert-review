# -*- coding: utf-8 -*-
import scrapy
# Need to figure out file path to import the Concert model in order to save to db
from concertInfoSpider.items import ConcertItem 

class ConcertsSpider(scrapy.Spider):
    name = 'concerts'
    allowed_domains = [
        'www.usana-amp.com/events/',
        'thestateroom.com/shows'

    ]
    start_urls = [
        'https://www.usana-amp.com/events//',
        'http://thestateroom.com/shows'
    ]

    def parse(self, response):
        # extracting response from USANA
        if not response:
            print("error with USANA scrape")
        # venue = 'USANA Amphitheater'
        # image = response.css("")
        months = response.css(".mm::text").extract() #result is a list of months
        days = response.css(".dd::text").extract()
        artists = response.css("h2").css("a::text").extract()
        ticket_links = response.css(".wraper-bottom-right.valign-wrapper").css("a::attr(href)").extract()
        
        for i in range(len(months)):
            item = ConcertItem()
            item['venue'] = "USANA Amphitheater"
            item['artist'] = artists[i].strip()
            item['month'] = months[i]
            item['day'] = days[i]
            item['image'] = "Nothing for now"
            item['ticket_link'] = ticket_links[i]
            yield item
        
        yield scrapy.Request('http://thestateroom.com/shows', callback = self.parseSR)
    # State Room parse 
    def parseSR(self, response):
        if not response:
            print("Error with State Room scrape")
            return
        else:
            venue = "The State Room"
            artists = response.css("h2").css("a::text").extract()
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
            for date in array:
                head,sep,tail = date.partition(',')
                newdate = head
                head,sep,tail = newdate.partition(' ')
                monthArray.append(head)
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
                item['image'] = 'http://thestateroom.com' + images[i]
                item['ticket_link'] = ticket_links[i]
                yield item
                print("Crawled SR website", item)
    
    #The State Room potential spider
    #http://thestateroom.com/shows
    # response.css("h2").css("a::text").extract() -----for artists
    # response.css("h3").css("span::text").extract() -----for dates(includes Month, Day, Year)
    # response.css(".ohanah-registration-link").css("a::attr(href)").extract() ----link to buy tickets
    # --images-- must put http://thestateroom.com before the link
    # response.css(".ohanah_modal::attr(href)").extract()

    #------The Depot uses client-side rendering so I can't scrape the data I want with scrapy

    # Vivint Arena
    # http://www.vivintarena.com/events?event_type=Concert
    # ----artists--- response.css(".title").css("h5::text").extract() 
    # ---specify month to get artists for that month---?? to get month 
    # response.css("#october").css(".title").css("h5::text").extract() 
    # ----days---- response.css(".date").css("em::text").extract() 
    # ----time of concert response.css(".date").css("i::text").extract() 
    # ---ticket_links,  remember when /tickets is extracted to skip it before saving other links to db
    # response.css(".tickets").css("a::attr(href)").extract() 
    # --images--
    # response.css(".synopsis").css("img::attr(src)").extract()

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

    # Owl Bar in Sundance --- https://www.sundanceresort.com/events/owl-bar-live-music/
    # ---dates and artists --- eliminate first p tag since it isn't an artist or date
    # response.css(".Main__contentWrapper").css("p::text").extract()
    # some .join may be required for artists
    # --ticket_link--- no tickets to buy just cover charge at the door
    
    # Red Butte Garden --- https://www.redbuttegarden.org/concerts/
    # --- artists--- for some reason it gathers all of them, past and future
    # response.css(".con-title.caps").css("a::text").extract()
    # ---date--- day of week/month/day ---need to split up month and day 
    # response.css(".con-date::text").extract()
    # ---ticket_link--- all the same
    # https://redbuttegarden.ticketfly.com

    # SLC Gallivan Center - Twilight concert series
    # Uses an img tag to display artists, times/dates
    # Prob manual input is best here

    # The Commonwealth Room --- http://thecommonwealthroom.ticketfly.com/listing
    # ---artists--- 
    # response.css(".headliners.summary").css('a::text').extract()
    # --dates-- numbers that need to be converted into month name or keep as month number
    # response.css(".dates::text").extract()
    # Can get time concert starts...might be tricky to save
    # --ticket_link-- 
    # response.css(".ticket-link").css("a::attr(href)").extract()

    # The Egyptian --Park City-- https://www.egyptiantheatrecompany.org/
    # --artists-- careful because not all are concerts
    # response.css(".event_info").css("h2::text").extract()
    # --date--sometimes multiple shows in a row written as Aug 25-29
    # response.css(".event_info").css(".thedate::text").extract()
    # --ticket_link-- 
    #  response.css(".event_info").css("a::attr(href)").extract()

    # All of Park City events  --- https://www.visitparkcity.com/events/music-and-concerts/

    # Kilby Court -- https://www.kilbycourt.com/
    # -- artists -- 
    # response.css(".headliners.summary").css('a::text').extract()
    # --date-- returns day of week as well...Monday, Wednesday, etc.
    # response.css(".dates::text").extract()
    # --ticket_link--
    # response.css(".ticket-link").css("a::attr(href)").extract()

    # Maverik Center -- http://maverikcenter.com/events-tickets/upcoming-events/
    # --artists--
    # response.css(".data-info").css("h4::text").extract()
    # --date-- gives date and then in next h5 tag gives you time door opens and show time
    # response.css(".data-info").extract_first().css("h5::text").extract()
    # --ticket_link-- every other link(starting with the second link) is a link to more info on the artist
    # response.css(".buttons").css("a::attr(href)").extract()
    # --image-- response.css(".image").css('img::attr(src)').extract()

    # TODO
    # USANA
    # The State Room
    # The Commonwealth Room
    # Vivint arena
    # Kenley Amphitheater
    # Sandy Amphitheater
    # Sundance Bluebird Concert series
    # Owl bar in Sundance
    # Red Butte Garden 
    # Gallivan Center
    # The Egyptian
    # Kilby Kourt
    # Maverik Center
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