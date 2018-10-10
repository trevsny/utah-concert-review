from django.conf.urls import url 
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^concerts', views.create),
    url(r'^filterbyvenue', views.filterByVenue),
    url(r'^filterbyartist', views.filterByArtist),
    url(r'^filterbydate', views.filterByDate),
    url(r'^showAll', views.showAllConcerts),
    url(r'^destroy', views.destroy),
    url(r'^scrape', views.scrape)
    
]