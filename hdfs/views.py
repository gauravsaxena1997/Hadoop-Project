from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.views.generic import View
from django.template import loader
from django.http import HttpResponse
from django.core.urlresolvers import reverse

# Create your views here.
import webbrowser as wb
import mysql.connector as pysql
import subprocess as sb
import time
import sys
import os
# Create your views here.
def hdfs (request):
	return render (request, 'hdfs.html')

def phdfs (request):
	local_from = request.POST['from']
	to = request.POST['to']
	print (local_from)
	print (to)
	os.system('docker exec container_0 hadoop fs -put ' + local_from + " " + to )
	time.sleep(2)
	os.system('docker exec container_0 hadoop fs -cat ' + to )
	return render (request, 'hdfs.html')
