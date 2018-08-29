# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class ConcertVenue(models.Model):
    venue = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class ConcertInfo(models.Model):
    venue = models.ForeignKey(ConcertVenue, related_name = "concerts", on_delete = models.CASCADE)
    artist = models.CharField(max_length = 255)
    month = models.CharField(max_length = 255)
    day = models.CharField(max_length = 255)
    image = models.CharField(max_length = 255, default = "")
    ticket_link = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
