from django.conf.urls import url , include
from . import views
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static


app_name = 'twitter'

urlpatterns = [
    url(r'^$', views.twitter, name='twitter'),
    url(r'^analyse/$', views.analyse, name='analyse'),


]
