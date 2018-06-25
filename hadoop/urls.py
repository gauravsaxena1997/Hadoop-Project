from django.conf.urls import url, include
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('cluster.urls')),
    url(r'^services/', include('services.urls') ),
    url(r'^twitter/', include('twitter.urls') ),
    
]


if settings.DEBUG:
	urlpatterns+= ( static(settings.STATIC_URL) )
