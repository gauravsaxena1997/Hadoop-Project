from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.views.generic import View
from django.template import loader
from django.http import HttpResponse
from django.core.urlresolvers import reverse

# extra
import os
import subprocess as sb
import mysql.connector as pysql
import services.views



def index (request):
	print ('Welcome....')
	return render (request, 'index.html')

def signup (request):
	return render (request, 'signup.html')

def postsignin (request):
	email = request.POST['email']
	password = request.POST['password']
	conn = pysql.connect(user='root',password='m487',database='hadoop',host='localhost')
	if ( conn.is_connected() ):
		cur = conn.cursor()
		query =  ("SELECT * FROM signup "
	                 "WHERE email='{}' and password='{}';".format(email,password) )
		try:
			cur.execute (query)
			x =   fetch = cur.fetchall()
			print (x)
			if ( len(fetch)>0 ):
				print('Success....')
				return render (request, 'success.html')
			else:
				print('invalid....')
				return render (request, 'invalid.html')
	 
		except:
			conn.rollback()
			print("oops..!!")	
	else:
		print ('Something went wrong...')

def postsignup (request):
	name =  request.POST['name']
	email =  request.POST['email']
	contact =  request.POST['contact']
	password =  request.POST['password']
	conn = pysql.connect(user='root',password='m487',host='localhost')
	if ( conn.is_connected() ):
		print ('Database connected successfully...')
		cur = conn.cursor()
		cur.execute ("""create database if not exists hadoop""")
		cur.execute ("use hadoop")
		cur.execute ("""create table if not exists signup (  
						name CHAR(20) NOT NULL,
						email CHAR(30) NOT NULL PRIMARY KEY,
						contact BIGINT UNSIGNED NOT NULL,
						password CHAR(15) NOT NULL )""")
		query = ("INSERT INTO signup "
	          "(name, email, contact, password) "
	          "VALUES ('%s','%s','%d','%s')" % (name, email, int(contact), password) )
		try:
			cur.execute(query)
			conn.commit()
			message = ' Account created successfully'
			return render (request, 'index.html', {'message': message})
		except:
			conn.rollback()
			print("oops..!!")
	else:
		print ('Something went wrong...')
		message = 'Something went wrong'
		return render (request, 'signup.html', {'message': message})

def dashboard (request):
	print ('Dashboard is here...............')
	status = request.session.get('status')
	if ( status == None ):                                                                                 #-- There are no clusters
		container_name = request.session.get('container_name')
		if ( container_name == None ):
			no_cluster = "No Cluster"
			return render (request, 'dashboard.html', {'no_cluster':no_cluster})

		else:                                                                                              #-- Everything works fine
			container_id = request.session.get('container_id')
			ip_list = request.session.get('ip_list')
			service_type = request.session.get('service_type')
			container_type = request.session.get('container_type')
			print(service_type)
			all_details = zip(container_name,ip_list,container_id,container_type)
			cluster = "Cluster is here."
			return render (request, 'dashboard.html',{ 'all_details' : all_details , 'cluster':cluster , 'service_type':service_type})

	elif ( status == 'clear' ):                                                                           #-- Cleaing up whole cluster
		request.session['status'] = None
		container_name = request.session.get('container_name')
		container_id = request.session.get('container_id')
		ip_list = request.session.get('ip_list')
		request.session['container_name'] = None
		request.session['container_id'] = None
		request.session['ip_list'] = None
		request.session['container_type'] = None
		print('Cluster clear')
		message = "Cluster is cleared"
		request.session['message'] = message
		return render (request, 'dashboard.html',{'message':message})

def twitter (request):
	return render (request, 'twitter.html')

def about (request):
	return render (request, 'about.html')

def settings (request):
	return render (request, 'settings.html')

def clear_cluster (request):
	sb.getoutput ('docker kill $(docker ps -qa)')
	sb.getoutput ('docker rm $(docker ps -qa)')
	request.session['status'] = 'clear'
	return redirect('/dashboard/')
