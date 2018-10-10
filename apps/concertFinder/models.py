# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
# Create your models here.

def currentYear():
        return datetime.datetime.today().year
class ConcertVenue(models.Model):
    venue_name = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.venue_name

class ConcertNote(models.Model):
    note_attending = models.CharField(max_length=255, default="")
    note_featured = models.CharField(max_length=255, default="")

    def __str__(self):
        template = '{0.note_attending}{0.note_featured}'
        return template.format(self)

class ConcertInfo(models.Model):
    venue = models.ForeignKey(ConcertVenue, related_name = "concerts", on_delete = models.CASCADE)
    artist = models.CharField(max_length = 255)
    month = models.IntegerField()
    day = models.IntegerField()
    year = models.IntegerField(default = datetime.datetime.today().year)
    image = models.CharField(max_length = 255, default = "static/ucr.jpg")
    ticket_link = models.CharField(max_length = 255, default = "")
    note_attend = models.ForeignKey(ConcertNote, related_name = "attending", blank = True, null = True, on_delete = models.CASCADE)
    note_feature = models.ForeignKey(ConcertNote, related_name = "featured", blank = True, null = True, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        template = '{0.artist}{0.month}{0.day}'
        return template.format(self)