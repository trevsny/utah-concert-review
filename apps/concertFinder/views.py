# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from concertInfoSpider.concertInfoSpider.items import ConcertItem
from .models import *
from datetime import datetime, timedelta, date
from concertInfoSpider.concertInfoSpider.spiders.concerts_spider import *
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from twisted.internet import reactor
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from dotenv import load_dotenv
import os

load_dotenv()

KEVIN_LOGIN = os.getenv('KEVIN_LOGIN')
KEVIN_PASSWORD = os.getenv('KEVIN_PASSWORD')

@xframe_options_exempt
def index(request):
    concerts = ConcertInfo.objects.all().order_by("year","month", "day")
    for concert in concerts:
        concert.month = changeIntToMonthName(concert.month)
    count = concerts.count()
    return render(request, "concertFinder/index.html", {'concerts':concerts, 'count':count})
@xframe_options_exempt
def filterByVenue(request):
    concerts = ConcertInfo.objects.filter(venue__venue_name__icontains = request.GET['venue_starts_with']).order_by("year", "month","day")
    for concert in concerts:
        concert.month = changeIntToMonthName(concert.month)
    count = concerts.count()
    print(count)
    return render(request, ('concertFinder/filtered.html'), {'concerts':concerts, 'count': count})
@xframe_options_exempt
def filterByArtist(request):
    concerts = ConcertInfo.objects.filter(artist__icontains = request.GET['artist_starts_with']).order_by("year","month","day")
    for concert in concerts:
        concert.month = changeIntToMonthName(concert.month)
    count = concerts.count()
    return render(request, ('concertFinder/filtered.html'), {'concerts': concerts, 'count':count})
@xframe_options_exempt
def filterByDate(request):
    if request.GET['month'] == "Select Month":
        count = 0
        return render(request, 'concertFinder/filtered.html')
    else:
        concerts = ConcertInfo.objects.filter(month__exact = request.GET['month']).order_by("year", "month","day")
        count = concerts.count()
        for concert in concerts:
            concert.month = changeIntToMonthName(concert.month)
        return render(request, ('concertFinder/filtered.html'), {'concerts': concerts, 'count': count})
@xframe_options_exempt
def showAllConcerts(request):
    concerts = ConcertInfo.objects.all().order_by("year", "month","day")
    count = concerts.count()
    for concert in concerts:
        concert.month = changeIntToMonthName(concert.month)
    return render(request, 'concertFinder/filtered.html', {'concerts': concerts, 'count':count})
# don't create duplicate concerts
def create(request):
    # Function to get checkbox data
    def checkboxes(newConcert):
        notes = ConcertNote.objects.all()
        # If notes already exist in db
        if notes:
            for note in notes:
                if request.POST.get('note_attending') and request.POST.get('note_featured'):
                    newConcert.note_attend = note
                    newConcert.note_feature = note
                    newConcert.save()
                    break
                elif request.POST.get('note_attending') and not request.POST.get('note_featured'):
                    newConcert.note_attend = note
                    newConcert.note_feature = None
                    newConcert.save()
                    break
                elif request.POST.get('note_featured') and not request.POST.get('note_attending'):
                    newConcert.note_feature = note
                    newConcert.note_attend = None
                    newConcert.save()
                    break
                else:
                    newConcert.note_feature = None
                    newConcert.note_attend = None
                    newConcert.save()
            return newConcert
        # If notes doesn't exist - Creating one object in notes table - hard coded phrases
        else:
            newNote = ConcertNote.objects.create(note_attending = "We'll be there!", note_featured = "UCR Featured Concert")
            if request.POST.get('note_attending') and request.POST.get('note_featured'):
                newConcert.note_attend = newNote
                newConcert.note_feature = newNote
                newConcert.save()
            elif request.POST.get('note_attending') and not request.POST.get('note_featured'):
                newConcert.note_attend = newNote
                newConcert.save()
            elif request.POST.get('note_featured') and not request.POST.get('note_attending'):
                newConcert.note_feature = newNote
                newConcert.save()
            else:
                return newConcert
    ##### end of checkboxes()

    # post method validation inside def create(request) 
    if request.method == "POST":
        # validations for form
        error = False
        if not request.POST['venue']:
            messages.error(request, "Forgot the venue")
            error = True
        if not request.POST['artist']:
            messages.error(request, "Forgot the artist")
            error = True
        if request.POST['month'] == '0':
            messages.error(request, "Please select month")
            error = True
        if request.POST['day'] == '0':
            messages.error(request, "Please select day")
            error = True
        if error:
            return redirect('/success')
        # create object
        venues = ConcertVenue.objects.all()
        # When database is empty need this line
        concertVenueExist = False
        # Does venue already exist in db?
        for venue in venues:
            concertVenueExist = False
            if venue.venue_name == request.POST['venue']:
                if request.POST['year']:  #Check year was input
                    if request.POST['image']: #Check for image input
                        newConcert = ConcertInfo.objects.create(venue = venue, artist = request.POST['artist'], month = int(request.POST['month']), day = int(request.POST['day']), year = int(request.POST['year']), image = request.POST['image'], ticket_link = request.POST['ticket_link'])
                        concertVenueExist = True
                        checkboxes(newConcert)
                        break
                    else:  #use default image src saved in models
                        newConcert = ConcertInfo.objects.create(venue = venue, artist = request.POST['artist'], month = int(request.POST['month']), day = int(request.POST['day']), year = int(request.POST['year']), ticket_link = request.POST['ticket_link'])
                        concertVenueExist = True
                        checkboxes(newConcert)
                        break
                else:  #no year input
                    if request.POST['image']: #Check for image input
                        newConcert = ConcertInfo.objects.create(venue = venue, artist = request.POST['artist'], month = int(request.POST['month']), day = int(request.POST['day']), image = request.POST['image'], ticket_link = request.POST['ticket_link'])
                        checkboxes(newConcert)
                        concertVenueExist = True
                        break
                    else: #use default image src saved in models
                        newConcert = ConcertInfo.objects.create(venue = venue, artist = request.POST['artist'], month = int(request.POST['month']), day = int(request.POST['day']), ticket_link = request.POST['ticket_link'])
                        checkboxes(newConcert)
                        concertVenueExist = True
                        break
        # if venue exists (aka True) then we already created object...send back to /success.  Otherwise venue does not exist already and we must create a new object with the new venue.
        if concertVenueExist:
            messages.success(request, "Successfully created!")
            return redirect('/success') 
        else:
            if request.POST['year']: 
                newVenue = ConcertVenue.objects.create(venue_name = request.POST['venue'])
                newConcert = ConcertInfo.objects.create(venue = newVenue, artist = request.POST['artist'], month = int(request.POST['month']), day = int(request.POST['day']), year = int(request.POST['year']), image = request.POST['image'], ticket_link = request.POST['ticket_link'])
                checkboxes(newConcert)
                print("Is int")
                messages.success(request, "Successfully created!")
                return redirect('/success')
            else:
                newVenue = ConcertVenue.objects.create(venue_name = request.POST['venue'])
                newConcert = ConcertInfo.objects.create(venue = newVenue, artist = request.POST['artist'], month = int(request.POST['month']), day = int(request.POST['day']), image = request.POST['image'], ticket_link = request.POST['ticket_link'])
                checkboxes(newConcert)
                print("Not an int")
                messages.success(request, "Successfully created!")
                return redirect('/success')
    else:
        return redirect('/')

# Delete concert record
def destroy(request, concert_id):
    if request.method == "POST":
        concert = ConcertInfo.objects.get(id = concert_id)
        concert.delete()
        messages.success(request, "Concert Deleted")
        return redirect('/success')
    else:
        return redirect('/')

def destroyOld(request):
    # concerts = ConcertInfo.objects.all()
    if request.method == "POST":
        count = deleteOldEntries()
        messages.success(request,"Deleted " + str(count) + " concert(s)")
        return redirect('/success')
    else:
        return redirect('/login')

# function to run 'scrapy crawl concerts' from a script
@csrf_exempt
def scrape(request):
    if request.method == "POST":
        # instantiate spider object
        spider = ConcertsSpider()
        # Instantiate Settings object
        settings = Settings()
        # set the settings of my spider
        settings.set('ITEM_PIPELINES', {
        'concertInfoSpider.concertInfoSpider.pipelines.ConcertinfospiderPipeline': 300, })
        settings.set('TELNETCONSOLE_ENABLED', False)
        settings.set('DOWNLOAD_DELAY', 2)
        settings.set('BOT_NAME', 'concertInfoSpider')
        settings.set('NEWSPIDER_MODULE', 'concertInfoSpider.concertInfoSpider.spiders')
        settings.set('ROBOTSTXT_OBEY', True)
        settings.set('SPIDER_MODULES', ['concertInfoSpider.concertInfoSpider.spiders'])
        process = CrawlerProcess(settings = settings)
        process.crawl(spider)
        process.start()
        return redirect('/showAll')
    else:
        return redirect('/')
# Show login page
def showLoginPage(request):
    return render(request, 'concertFinder/login.html')

# Login
def login(request):
    if request.method == "POST":
        if request.POST['login_username'] == KEVIN_LOGIN and request.POST['login_password'] == KEVIN_PASSWORD:
            request.session['logged_in'] = True
            return redirect('/success')
        else:
            messages.error(request, "Invalid credentials, Kev")
            return redirect('/login')
    else:
        return redirect('/login')

# Show kevin's html page
def success(request):
    if not 'logged_in' in request.session:
        return redirect('/login')
    else:
        return render(request, 'concertFinder/kevin.html')
def logout(request):
    if request.method == "POST":
        try:
            del request.session['logged_in']
        except KeyError:
            pass
        return redirect('/login')
    else:
        return redirect('/')
def showEdit(request, concert_id):
    concert = ConcertInfo.objects.get(id = concert_id)
    return render(request, 'concertFinder/edit.html', {'concert':concert})

def update(request, concert_id):
    if request.method == "POST":
        notes = ConcertNote.objects.all()
        venues = ConcertVenue.objects.all()
        try:
            concert = ConcertInfo.objects.get(id = concert_id)
            for venue in venues:
                if venue.venue_name == request.POST['venue']:
                    concert.venue = venue
                    concert.save()
                else:
                    newVenue = ConcertVenue.objects.create(venue_name = request.POST['venue'])
                    concert.venue = newVenue
                    concert.save()
            concert.artist = request.POST['artist']
            if request.POST['month'] == '0':
                messages.error(request, "Select a month")
                return redirect('/edit/' + str(concert_id))
            else:
                concert.month = int(request.POST['month'])
                concert.save()
            if request.POST['day'] == '0':
                messages.error(request, "Select a day")
                return redirect('/edit/' + str(concert_id))
            else:
                concert.day = int(request.POST['day'])
                concert.save()

                concert.month = int(request.POST['month'])
            concert.year = int(request.POST['year'])
            concert.image = request.POST['image']
            concert.ticket_link = request.POST['ticket_link']
            # access notes
            for note in notes:
                # See if checkboxes are checked
                if request.POST.get('note_attending'):
                    concert.note_attend = note
                else:
                    concert.note_attend = None
                if request.POST.get('note_featured'):
                    concert.note_feature = note
                else:
                    concert.note_feature = None
            concert.save()
            messages.success(request, "Update successful")
            return redirect('/edit/'+str(concert_id))
        except:
            messages.error(request, "Update failed. :( Try deleting concert and creating it from scratch")
            return redirect('/edit/'+str(concert_id))
    else:
        return redirect('/')

# Function to delete old database entries of concerts
def deleteOldEntries():
    concerts = ConcertInfo.objects.all()
    count = 0
    for concert in concerts:
        # Now check for old concerts
        yesterday = date.today() - timedelta(1)
        try:
            concertDate = date(concert.year, concert.month, concert.day)
            if concertDate <= yesterday:
                concertToDelete = ConcertInfo.objects.get(id = concert.id)
                concertToDelete.delete()
                count = count + 1
                # print('successful deletion')
        except ValueError:
            # Months or days will be defaulted to 0 for some venues and those throw a ValueError upon attempted deletion
            pass
            print("In Value Error section")
    return count
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

