from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.views.generic import View
from django.template import loader
from django.http import HttpResponse
from django.core.urlresolvers import reverse
# Create your views here.
import mysql.connector as pysql
import subprocess as sb
import sys,os,time

def index (request):
	client = request.session.get('client')
	print (client)
	no_cluster = request.session.get('no_cluster')
	print(no_cluster)
	if (no_cluster=='No Cluster'):
		return render (request,'client/client.html',{'no_cluster':no_cluster})
	elif (client==None):
		cluster_existed = 'cluster_existed'
		return render (request,'client/client.html',{'cluster_existed':cluster_existed})
	elif (client=='created'):
		return redirect ('/client/home/')

def existing (request):
	request.session['client_name'] = 'container_2'
	request.session['client_id'] = sb.getoutput('sudo docker exec container_2 hostname')
	request.session['client_ip'] = sb.getoutput('sudo docker exec container_2 hostname -i')
	request.session['client'] = 'created'
	return redirect ('/client/home/')

def new (request):
	os.system (' sudo docker run -itd --privileged --restart always --name client hadoopv1.2')
	request.session['client_name'] = 'client'
	request.session['client_id'] = sb.getoutput('sudo docker exec client hostname')
	request.session['client_ip'] = sb.getoutput('sudo docker exec client hostname -i')
	request.session['client'] = 'created'
	return redirect ('/client/home/')

def home (request):
	client_name = request.session.get('client_name') 
	client_ip = request.session.get('client_ip') 
	client_id = request.session.get('client_id') 
	return render (request,'client/home.html',{
		'client_name':client_name,
		'client_ip':client_ip,
		'client_id':client_id
		})

def del_client (request):
	os.system('docker kill client')
	os.system('docker rm client')
	request.session['client_name'] = None
	request.session['client_id'] = None
	request.session['client_ip'] = None
	request.session['client'] = None
	return redirect ('/client/')


















