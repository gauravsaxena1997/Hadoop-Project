from django.conf.urls import url
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

app_name = 'services'

urlpatterns = [
    url(r'^$', views.services, name='services'),

    # Select version of hadoop
    url(r'^version_docker/$', views.version_docker, name='version_docker'),
    url(r'^version_vm/$', views.version_vm, name='version_vm'),

    # Docker hadoop version1
    url(r'^dochadoopv1/$', views.dochadoopv1, name='dochadoopv1'),
    url(r'^postdochadoopv1/$', views.postdochadoopv1, name='postdochadoopv1'),
    url(r'^dochv1_playbook/$', views.dochv1_playbook, name='dochv1_playbook'),
   
    # Docker hadoop version2
    url(r'^dochadoopv2/$', views.dochadoopv2, name='dochadoopv2'),
    url(r'^postdochadoopv2/$', views.postdochadoopv2, name='postdochadoopv2'),
    url(r'^dochv2_playbook/$', views.dochv2_playbook, name='dochv2_playbook'),

    # VM hadoop version1
    url(r'^vmhadoopv1/$', views.vmhadoopv1, name='vmhadoopv1'),
    url(r'^postvmhadoopv1/$', views.postvmhadoopv1, name='postvmhadoopv1'),
    url(r'^loading_vm_hv1/$', views.loading_vm_hv1, name='loading_vm_hv1'),
    url(r'^vmhv1_playbook/$', views.vmhv1_playbook, name='vmhv1_playbook'),
    
    # VM hadoop version2
    url(r'^vmhadoopv2/$', views.vmhadoopv2, name='vmhadoopv2'),
    url(r'^postvmhadoopv2/$', views.postvmhadoopv2, name='postvmhadoopv2'),
    url(r'^loading_vm_hv2/$', views.loading_vm_hv2, name='loading_vm_hv2'),
    url(r'^vmhv2_playbook/$', views.vmhv2_playbook, name='vmhv2_playbook'),
]