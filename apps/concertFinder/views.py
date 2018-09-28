# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from concertInfoSpider.concertInfoSpider.items import ConcertItem
from .models import *
from datetime import datetime, timedelta

def index(request):
    context = {
        'concerts': ConcertInfo.objects.all().order_by("year","-month", "day")
    }
    return render(request, "concertFinder/index.html", context)

def filterByVenue(request):
    concerts = ConcertInfo.objects.filter(venue__venue_name__startswith = request.POST['venue_starts_with'])
    return render(request, ('concertFinder/filtered.html'), {'concerts':concerts})

def filterByArtist(request):
    concerts = ConcertInfo.objects.filter(artist__startswith = request.POST['artist_starts_with'])
    return render(request, ('concertFinder/filtered.html'), {'concerts': concerts})

def filterByDate(request):
    print(request.POST['month'])
    concerts = ConcertInfo.objects.filter(month__startswith = request.POST['month']).order_by("year").order_by("day")
    return render(request, ('concertFinder/filtered.html'), {'concerts': concerts})

def showAllConcerts(request):
    concerts = ConcertInfo.objects.all().order_by("year").order_by("month").order_by("day")
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
        # Change strings of month names to integers for datetime comparison
        if concert.month == "January":
            concert.month = 1
        elif concert.month == "February":
            concert.month = 2
        elif concert.month == "March":
            concert.month = 3
        elif concert.month == "April":
            concert.month = 4
        elif concert.month == "May":
            concert.month = 5
        elif concert.month == "June":
            concert.month = 6
        elif concert.month == "July":
            concert.month = 7
        elif concert.month == "August":
            concert.month = 8
        elif concert.month == "September":
            concert.month = 9
        elif concert.month == "October":
            concert.month = 10
        elif concert.month == "November":
            concert.month = 11
        elif concert.month == "December":
            concert.month = 12
        # Change Day and Year columns to integers
        intDay = int(concert.day)
        intYear = int(concert.year)
        # Now check for old concerts
        yesterday = datetime.today() - timedelta(1)
        try:
            concertDate = datetime(intYear, concert.month, intDay)
            if concertDate <= yesterday:
                concertToDelete = ConcertInfo.objects.get(id = concert.id)
                concertToDelete.delete()
                print('successful deletion')
        except ValueError:
            print("In Value Error sections")
    
    def changeIntToMonthName(self, monthArray):
        for i in range(len(monthArray)):
            if monthArray[i] = 1
                monthArray[i] = "January"
            elif monthArray[i] == 2:
                monthArray[i] = "February"
            elif monthArray[i] == 3:
                monthArray[i] = "March"
            elif monthArray[i] == 4:
                monthArray[i] = "April"
            elif monthArray[i] == 5:
                monthArray[i] = "May"
            elif monthArray[i] == 6:
                monthArray[i] = "June"
            elif monthArray[i] == 7:
                monthArray[i] = "July"
            elif monthArray[i] == 8:
                monthArray[i] = "August"      
            elif monthArray[i] == 9:
                monthArray[i] = "September"
            elif monthArray[i] == 10:
                monthArray[i] = "October"
            elif monthArray[i] == 11:
                monthArray[i] = "November"
            elif monthArray[i] == 12:
                monthArray[i] = "December"
        return monthArray