# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from concertInfoSpider.concertInfoSpider.items import ConcertItem
from .models import *

def index(request):
    context = {
        'concerts': ConcertInfo.objects.all(),
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