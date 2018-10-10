from django.conf.urls import url 
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^concerts', views.create),
    url(r'^filterbyvenue', views.filterByVenue),
    url(r'^filterbyartist', views.filterByArtist),
    url(r'^filterbydate', views.filterByDate),
    url(r'^showAll', views.showAllConcerts),
    url(r'^destroyOld', views.destroyOld),
    url(r'^scrape', views.scrape),
    url(r'^login', views.showLoginPage),
    url(r'^gologin', views.login),
    url(r'^success', views.success),
    url(r'^logout', views.logout)
]