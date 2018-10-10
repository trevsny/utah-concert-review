# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from concertInfoSpider.concertInfoSpider.items import ConcertItem
from .models import *
from datetime import datetime, timedelta
from concertInfoSpider.concertInfoSpider.spiders.concerts_spider import *
from scrapy.crawler import Crawler, CrawlerRunner, CrawlerProcess
from scrapy.settings import Settings
from scrapy import signals, cmdline
from twisted.internet import reactor
# import scrapy
import runpy, cmd
from scrapyd_api import ScrapydAPI
from django.views.decorators.csrf import csrf_exempt
import threading
# from concertInfoSpider.concertInfoSpider.settings import *
from scrapy.utils.project import get_project_settings 
# ---Can't find this module ^^

# connect scrapyd service
# scrapyd = ScrapydAPI('http://localhost:6800')

def index(request):
    concerts = ConcertInfo.objects.all().order_by("year","month", "day")
    for concert in concerts:
        concert.month = changeIntToMonthName(concert.month)
    return render(request, "concertFinder/index.html", {'concerts':concerts})

def filterByVenue(request):
    concerts = ConcertInfo.objects.filter(venue__venue_name__startswith = request.POST['venue_starts_with']).order_by("year", "month","day")
    for concert in concerts:
        concert.month = changeIntToMonthName(concert.month)
    return render(request, ('concertFinder/filtered.html'), {'concerts':concerts})

def filterByArtist(request):
    concerts = ConcertInfo.objects.filter(artist__startswith = request.POST['artist_starts_with']).order_by("year","month","day")
    for concert in concerts:
        concert.month = changeIntToMonthName(concert.month)
    return render(request, ('concertFinder/filtered.html'), {'concerts': concerts})

def filterByDate(request):
    print(request.POST['month'])
    concerts = ConcertInfo.objects.filter(month__startswith = request.POST['month']).order_by("year", "month","day")
    for concert in concerts:
        concert.month = changeIntToMonthName(concert.month)
    return render(request, ('concertFinder/filtered.html'), {'concerts': concerts})

def showAllConcerts(request):
    concerts = ConcertInfo.objects.all().order_by("year", "month","day")
    for concert in concerts:
        concert.month = changeIntToMonthName(concert.month)
    return render(request, 'concertFinder/allConcerts.html', {'concerts': concerts})

# don't create duplicate concerts
def create(request):
    if request.method == "POST":
        venues = ConcertVenue.objects.all()
        for venue in venues:
            concertVenueExist = False
            if venue.venue_name == request.POST['venue']:
                newConcert = ConcertInfo.objects.create(venue = venue, artist = request.POST['artist'], month = request.POST['month'], day = request.POST['day'], image = request.POST['image'], ticket_link = request.POST['ticket_link'])
                concertVenueExist = True
                break
                
        if concertVenueExist:
            return redirect('/') 
        else:  
            newVenue = ConcertVenue.objects.create(venue_name = request.POST['venue'])
            newConcert = ConcertInfo.objects.create(venue = newVenue, artist = request.POST['artist'], month = request.POST['month'], day = request.POST['day'], image = request.POST['image'], ticket_link = request.POST['ticket_link'])
            return redirect('/')

def destroy(request):
    # concerts = ConcertInfo.objects.all()
    if request.method == "POST":
        deleteOldEntries()
        return redirect('/')
    else:
        return redirect('/')
# Function to delete old database entries of concerts
def deleteOldEntries():
    concerts = ConcertInfo.objects.all()
    for concert in concerts:
        # Now check for old concerts
        yesterday = datetime.today() - timedelta(1)
        try:
            concertDate = datetime(concert.year, concert.month, concert.day)
            if concertDate <= yesterday:
                concertToDelete = ConcertInfo.objects.get(id = concert.id)
                concertToDelete.delete()
                print('successful deletion')
        except ValueError:
            print("In Value Error sections")
    
def changeIntToMonthName(month):    
        if month == 1:
            month = "January"
        elif month == 2:
            month = "February"
        elif month == 3:
            month = "March"
        elif month == 4:
            month = "April"
        elif month == 5:
            month = "May"
        elif month == 6:
            month = "June"
        elif month == 7:
            month = "July"
        elif month == 8:
            month = "August"      
        elif month == 9:
            month = "September"
        elif month == 10:
            month = "October"
        elif month == 11:
            month = "November"
        elif month == 12:
            month = "December"
        return month 
# function to run 'scrapy crawl concerts' from a script
@csrf_exempt
def scrape(request):
    if request.method == "POST":
        print("in scrape function")
        print(threading.current_thread())
        print("List of threads", threading.enumerate())
        # scrapyd.schedule('concertInfoSpider', 'concerts')
        spider = ConcertsSpider()
    # reactor.run()
    # spider.start_requests()
    # reactor.stop()
    # settings = Settings()
    # newSettings = settings.copy()
    # crawler = CrawlerProcess(newSettings)
    # crawler.signals.disconnect_all(signal = spider.spider_open)
    # crawler.crawl('concerts')
    # runpy.run_module(scrapy)
    # cmd = Cmd()
    # Need to traverse file structure to go to spiders folder and then run scrapy crawl command or run as a script..
    # cmd.onecmd("scrapy crawl concerts")
    # runpy.run_path('../concertInfoSpider/concertInfoSpider/spiders/concerts_spider.py')
    # cmd = "scrapy crawl concerts"
    # cmdline.execute(['scrapy','crawl','concerts'])
    # instantiate settings
    # settings = Settings()
    # print("After settings")
    # instantiate crawler passing in settings
    # crawler = CrawlerProcess(settings)
        settings = Settings()
    # settings.set(
    #     'BOT_NAME', 'concertInfoSpider'
    # )
        settings.set('ITEM_PIPELINES', {
        'concertInfoSpider.concertInfoSpider.pipelines.ConcertinfospiderPipeline': 300, })
        settings.set('TELNETCONSOLE_ENABLED', False)
        settings.set('DOWNLOAD_DELAY', 2)
        print('after spider creation before CrawlerProcess instantiation')
        settings.set('BOT_NAME', 'concertInfoSpider')
        settings.set('NEWSPIDER_MODULE', 'concertInfoSpider.concertInfoSpider.spiders')
        settings.set('ROBOTSTXT_OBEY', True)
        settings.set('SPIDER_MODULES', ['concertInfoSpider.concertInfoSpider.spiders'])
        # settings.set('SPIDER_MIDDLEWARES', {
        # 'concertInfoSpider.middlewares.ConcertinfospiderSpiderMiddleware': 543,
        # })
        process = CrawlerProcess(settings = settings)
        # {'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'},
    # print("after instantiating crawler")
    # crawler = Crawler(ConcertsSpider, settings)
    # crawler = CrawlerRunner(settings)
    # instantiate spider
    # spider = ConcertsSpider()
    # print("after spider instance")
    # # process = CrawlerProcess(ConcertsSpider,settings)
        print("Before crawl function")
        process.crawl(spider)
    # print("Before spider crawls after signals thing")
    # spider.process.signals.
    # process.signals.connect(reactor.stop(), signal = signals.spider_closed)
        print("before start function")
        process.start()
        print('after start function')
        # reactor.run(installSignalHandlers = False)
    # process.start(stop_after_crawl = True)
    # process.crawl('concerts')
    # configure signals
    # print("Before first signals thing")
    # configure and start crawler, heads to concerts_spider.py now
    # crawler.start(stop_after_crawl = True)
    # crawler.crawl(spider)
    # crawler.stop()
    # print("after crawler stop")
    # # reactor.run()
    # print("After reactor.run()")
    # print("After reactor.run with signals things")
    return redirect('/showAll')
