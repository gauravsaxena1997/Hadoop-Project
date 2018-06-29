from django.conf.urls import url, include
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('basic.urls')),
    url(r'^docker/', include('docker.urls') ),
    url(r'^vm/', include('vm.urls') ),
    url(r'^twitter/', include('twitter.urls') ),
    url(r'^client/', include('client.urls') ),

]


if settings.DEBUG:
	urlpatterns+= ( static(settings.STATIC_URL) )
