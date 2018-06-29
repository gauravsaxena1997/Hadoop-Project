from django.conf.urls import url
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

app_name = 'docker'

urlpatterns = [
    url(r'^version/$', views.version, name='version'),

    # Docker hadoop version1
    url(r'^hadoopv1/$', views.hadoopv1, name='hadoopv1'),
    url(r'^posthadoopv1/$', views.posthadoopv1, name='posthadoopv1'),
    url(r'^hv1_playbook/$', views.hv1_playbook, name='hv1_playbook'),
   
    # Docker hadoop version2
    url(r'^hadoopv2/$', views.hadoopv2, name='hadoopv2'),
    url(r'^posthadoopv2/$', views.posthadoopv2, name='posthadoopv2'),
    url(r'^hv2_playbook/$', views.hv2_playbook, name='hv2_playbook'),

    # Cluster Clear
    url(r'^clear_cluster/$', views.clear_cluster, name='clear_cluster'),

]