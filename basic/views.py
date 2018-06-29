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
	container_name = request.session.get('container_name')
	vm = request.session.get('vm')

	print (vm)

	if ( container_name == None and vm == None):
		request.session['client'] = None
		no_cluster = "No Cluster"
		request.session['no_cluster'] = no_cluster
		return render (request, 'dashboard.html', {'no_cluster':no_cluster})

	elif (container_name == None and vm == 'vm'):
		ip_list = request.session.get('ip_list')
		service_provided = request.session.get('service_provided')	
		service_status = request.session.get('service_status')	
		all_details = zip(ip_list,service_provided,service_status)
		request.session['no_cluster'] = 'cluster_existed'
		vm = "VM based Cluster"
		print(vm)
		return render (request, 'dashboard.html', {'vm':vm , 'all_details':all_details })

	else:                                                                                              #-- Everything works fine
		index_value = request.session.get('index_value')
		service_type = request.session.get('service_type')
		container_id = request.session.get('container_id')
		ip_list = request.session.get('ip_list')
		container_type = request.session.get('container_type')
		service_status = request.session.get('service_status')
		request.session['no_cluster'] = 'cluster_existed'
		docker = "docker"
		all_details = zip(index_value,container_name,ip_list,container_id,container_type,service_status)
		return render (request, 'dashboard.html',
			{'all_details':all_details ,'docker':docker,'service_type':service_type})

def service_status (request):
	service_status = request.session.get('service_status')
	reference_var = request.GET['reference_var']
	index = int(request.GET['index'])
	service_type = request.GET['type']
	service_type = service_type.split('&')
	if (len(service_type) == 1):
		if (service_status[index] == 'Running'): 
			os.system('sudo docker exec '+reference_var+' hadoop-daemon.sh stop '+service_type[0])
			service_status[index] = 'Stopped'
		else:
			os.system('sudo docker exec '+reference_var+' hadoop-daemon.sh start '+service_type[0])
			service_status[index] = 'Running'
	else:
		print(service_type)
		print('two')
	print (service_status)
	request.session['service_status'] = service_status
	return redirect ('/dashboard/')

def about (request):
	return render (request, 'about.html')

def create (request):
	return render (request, 'service.html')

def settings (request):
	return render (request, 'settings.html')



