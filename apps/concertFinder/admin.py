# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import ConcertInfo, ConcertVenue
# admin.site.register(ConcertVenue)
# admin.site.register(ConcertInfo)
@admin.register(ConcertInfo)
class ConcertAdmin(admin.ModelAdmin):
    list_display = ['venue','artist','month','day','year']
@admin.register(ConcertVenue)
class Venue(admin.ModelAdmin):
    list_display = ['venue_name']