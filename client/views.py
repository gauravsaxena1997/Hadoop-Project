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
	command = request.session.get('command') 
	request.session['command'] = None
	return render (request,'client/home.html',{
		'client_name':client_name,
		'client_ip':client_ip,
		'client_id':client_id,
		'command':command           })

def del_client (request):
	os.system('docker kill client')
	os.system('docker rm client')
	request.session['client_name'] = None
	request.session['client_id'] = None
	request.session['client_ip'] = None
	request.session['client'] = None
	return redirect ('/client/')

def ls (request):
	client_name = request.session.get('client_name')
	command = sb.getoutput('docker exec '+client_name+' hadoop fs -ls hdfs://172.17.0.2:10001/')
	request.session['command'] = command
	return redirect ('/client/')

def cat (request):
	location = request.POST.get('location')
	client_name = request.session.get('client_name')
	command = sb.getoutput('docker exec '+client_name+' hadoop fs -cat hdfs://172.17.0.2:10001'+location)
	request.session['command'] = command
	return redirect ('/client/')

def mkdir (request):
	location = request.POST.get('location')
	client_name = request.session.get('client_name')
	sb.getoutput('docker exec '+client_name+' hadoop fs -mkdir hdfs://172.17.0.2:10001'+location)
	return redirect ('/client/')

def rmr (request):
	location = request.POST.get('location')
	client_name = request.session.get('client_name')
	sb.getoutput('docker exec '+client_name+' hadoop fs -rmr hdfs://172.17.0.2:10001'+location)
	return redirect ('/client/')

def touchz (request):
	location = request.POST.get('location')
	client_name = request.session.get('client_name')
	sb.getoutput('docker exec '+client_name+' hadoop fs -touchz hdfs://172.17.0.2:10001'+location)
	return redirect ('/client/')

def rm (request):
	location = request.POST.get('location')
	client_name = request.session.get('client_name')
	sb.getoutput('docker exec '+client_name+' hadoop fs -rm hdfs://172.17.0.2:10001'+location)
	return redirect ('/client/')

def clear_all (request):
	all_files = sb.getoutput ('hadoop fs -ls hdfs://172.17.0.2:10001/ | cut -d "/" -f2 | grep -vi Found')
	directories = all_files.split()
	for files in directories:
		print ('cleaning /'+files+' ...')
		sb.getoutput ('hadoop fs -rmr hdfs://172.17.0.2:10001/'+files)
	return redirect ('/client/')

def put (request):
	location_from = request.POST.get('location_from')
	location_to = request.POST.get('location_to')
	client_name = request.session.get('client_name')
	sb.getoutput('docker exec '+client_name+' hadoop fs -put '+location_from+ ' hdfs://172.17.0.2:10001'+location_to)
	return redirect ('/client/')

def chown (request):
	user = request.POST.get('user')
	location = request.POST.get('location')
	client_name = request.session.get('client_name')
	sb.getoutput('docker exec '+client_name+' hadoop fs -chown '+user+ ' hdfs://172.17.0.2:10001'+location)
	return redirect ('/client/')

def count (request):
	location = request.POST.get('location')
	client_name = request.session.get('client_name')
	command = sb.getoutput('docker exec '+client_name+' hadoop fs -count hdfs://172.17.0.2:10001'+location)
	request.session['command'] = command
	return redirect ('/client/')





