from django.conf.urls import url
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

app_name = 'client'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^new/$', views.new, name='new'),
    url(r'^existing/$', views.existing, name='existing'),
    url(r'^del_client/$', views.del_client, name='del_client'),

    # Operations
    url(r'^ls/$', views.ls, name='ls'),
    url(r'^mkdir/$', views.mkdir, name='mkdir'),
    url(r'^rmr/$', views.rmr, name='rmr'),
    url(r'^touchz/$', views.touchz, name='touchz'),
    url(r'^rm/$', views.rm, name='rm'),
    url(r'^put/$', views.put, name='put'),
    url(r'^cat/$', views.cat, name='cat'),
    url(r'^chown/$', views.chown, name='chown'),
    url(r'^count/$', views.count, name='count'),
    url(r'^clear_all/$', views.clear_all, name='clear_all'),

]