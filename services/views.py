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

service_type = []

def services (request):
	return render (request, 'service.html')

def version_docker (request):
	return render (request, 'version-docker.html')

def version_vm (request):
	return render (request, 'version-vm.html')

def dochadoopv1 (request):
	return render (request, 'dochadoopv1.html')

def dochadoopv2 (request):
	return render (request, 'dochadoopv2.html')

def postdochadoopv1 (request):
	nodes = request.POST ['nodes']
	stype = request.POST ['service_type']
	service_type.append(stype)
	print ( service_type[0] )
	for i in range (int(nodes)):
		os.system (' sudo docker run -itd --name containe'+str(i)+' hadoopv1.2')
		hostname = sb.getoutput('sudo docker exec containe'+str(i)+' hostname')
		sb.getoutput ('sudo docker exec '+hostname+' service sshd start')
		ip = sb.getoutput('sudo docker exec containe'+str(i)+' hostname -i')
		sb.getoutput ('ssh-keyscan '+ip)
		#---- Namenode and other Datanodes
		#---- Namenode and JobTracker on one machine &amp; Datanodes and TaskTracker on others
		if ( service_type[0] == 'nn_dn' or service_type[0] == 'nnjt_dntt' ):
			if ( i == 0 ):
				fhand = open("/etc/ansible/hosts","a+")
				fhand.write('\n[docker-nn]\n')
				fhand.write(ip+'\n')
				fhand.close()
			else:
				fhand = open("/etc/ansible/hosts","a+")
				fhand.write('\n[docker-dn]\n')
				fhand.write(ip+'\n')
				fhand.close()
		#---- Seperate Namenode and JobTracker & Datanodes and TaskTracker on same machines
		elif ( service_type[0] == 'nn_jt_dntt' ):
			if ( i == 0 ):
				fhand = open("/etc/ansible/hosts","a+")
				fhand.write('\n[docker-nn]\n')
				fhand.write(ip+'\n')
				fhand.close()
			elif ( i == 1 ):
				fhand = open("/etc/ansible/hosts","a+")
				fhand.write('\n[docker-jt]\n')
				fhand.write(ip+'\n')
				fhand.close()
			else:
				fhand = open("/etc/ansible/hosts","a+")
				fhand.write('\n[docker-dn]\n')
				fhand.write(ip+'\n')
				fhand.close()
		#---- Seperate Namenode, JobTracker, Datanodes and TaskTracker
		else:
			temp = ((int(nodes)-2)/2) + 1
			print (temp)
			if ( i == 0 ):
				fhand = open("/etc/ansible/hosts","a+")
				fhand.write('\n[docker-nn]\n')
				fhand.write(ip+'\n')
				fhand.close()
			elif ( i == 1 ):
				fhand = open("/etc/ansible/hosts","a+")
				fhand.write('\n[docker-jt]\n')
				fhand.write(ip+'\n')
				fhand.close()
			elif ( i>=2 and i<=temp ):
				print("Loop counter: "+str(i))
				fhand = open("/etc/ansible/hosts","a+")
				fhand.write('\n[docker-dn]\n')
				fhand.write(ip+'\n')
				fhand.close()
			else:
				print("else........")
				print("Loop counter: "+str(i))
				fhand = open("/etc/ansible/hosts","a+")
				fhand.write('\n[docker-tt]\n')
				fhand.write(ip+'\n')
				fhand.close()
	return render (request, 'loader.html')


def loader (request):
	print ('ansible playbook is running...')
	if ( service_type[0] == 'nn_dn' ):
		os.system('sudo ansible-playbook /etc/ansible/playbooks/docker/onlynndn.yml')
	elif ( service_type[0] == 'nnjt_dntt' ):
		os.system('sudo ansible-playbook /etc/ansible/playbooks/docker/nnjt_dntt.yml')
	elif ( service_type[0] == 'nn_jt_dntt' ):
		os.system('sudo ansible-playbook /etc/ansible/playbooks/docker/nn_jt_dntt.yml')
	else:
		os.system('sudo ansible-playbook /etc/ansible/playbooks/docker/nn_jt_dn_tt.yml')

	return HttpResponse(status=201)
