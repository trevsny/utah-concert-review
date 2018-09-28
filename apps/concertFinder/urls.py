from django.conf.urls import url 
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^concerts', views.create),
    url(r'^filterbyvenue', views.filterByVenue),
    url(r'^filterbyartist', views.filterByArtist),
    url(r'^filterbydate', views.filterByDate)
    
]