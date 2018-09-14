# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
# Create your models here.

class ConcertVenue(models.Model):
    venue_name = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.venue_name

class ConcertInfo(models.Model):
    venue = models.ForeignKey(ConcertVenue, related_name = "concerts", on_delete = models.CASCADE)
    artist = models.CharField(max_length = 255)
    month = models.CharField(max_length = 255)
    day = models.CharField(max_length = 255)
    year = models.IntegerField(default = datetime.datetime.today().year)
    image = models.CharField(max_length = 255, default = "")
    ticket_link = models.CharField(max_length = 255, default = "")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.artist, self.venue, self.month, self.day, self.year