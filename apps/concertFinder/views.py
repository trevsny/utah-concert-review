# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from concertInfoSpider.concertInfoSpider.items import ConcertItem
from .models import *

def index(request):
    response = "Hello, I'm first request"
    context = {
        'item': ConcertItem,
        'concerts': ConcertInfo.objects.all()
    }
    return render(request, "concertFinder/index.html", context)
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