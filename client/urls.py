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

]