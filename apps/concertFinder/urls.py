from django.conf.urls import url 
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView


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
    url(r'^logout', views.logout),
    url(r'^edit/(?P<concert_id>\d+)', views.showEdit),
    url(r'^update/(?P<concert_id>\d+)', views.update),
    url(r'^destroy/(?P<concert_id>\d+)', views.destroy),
    url(r'^favicon.ico$',RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'),permanent=False),name="favicon"),
    url(r'^', views.index)
]