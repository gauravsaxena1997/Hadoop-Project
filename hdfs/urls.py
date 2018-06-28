from django.conf.urls import url
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

app_name = 'hdfs'

urlpatterns = [
    url(r'^$', views.hdfs, name='hdfs'),
    url(r'^phdfs/$', views.phdfs, name='phdfs'),
]