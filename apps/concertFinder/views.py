# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from concertInfoSpider.concertInfoSpider.items import ConcertItem

def index(request):
    response = "Hello, I'm first request"
    context = {
        'item': ConcertItem
    }
    return render(request, "concertFinder/index.html", context)
