from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.views.generic import View
from django.template import loader
from django.http import HttpResponse
from django.core.urlresolvers import reverse

# extra
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
	print ('Clustering is done...............')
	# print (ip_list)
		# hostname = sb.getoutput('sudo docker exec containe'+str(i)+' hostname')
		# ip = os.system('sudo docker exec containe'+str(i)+' hostname -i')
		# print ('Name: containe'+ str(i)+ '\t\t IP: ' +str(ip)+ '\t\t Container_Id: '+ hostname)
		# fhand = open("/etc/ansible/hosts","a+")
		# fhand.write(ps)
	return render (request, 'dashboard.html')

def twitter (request):
	return render (request, 'twitter.html')

def about (request):
	return render (request, 'about.html')

def settings (request):
	return render (request, 'settings.html')