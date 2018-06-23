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



def services (request):
	return render (request, 'service.html')

def version_docker (request):
	return render (request, 'version-docker.html')

def version_vm (request):
	return render (request, 'version-vm.html')

#---------------------------------------------------- Docker hadoop version 1.2.1-------------------------------------------------------------
def dochadoopv1 (request):
	return render (request, 'dochadoopv1.html')

def postdochadoopv1 (request):
	ip_list = []
	container_id = []
	container_name = []
	container_type = []
	nodes = request.POST ['nodes']
	service_type = request.POST ['service_type']
	request.session['service_type'] = service_type
	for i in range (int(nodes)):
		sb.getoutput (' sudo docker run -itd --name container'+str(i)+' hadoopv1.2')
		container_name.append('container'+str(i))
		hostname = sb.getoutput('sudo docker exec container'+str(i)+' hostname')
		container_id.append(hostname)
		sb.getoutput ('sudo docker exec '+hostname+' service sshd start')
		ip = sb.getoutput('sudo docker exec container'+str(i)+' hostname -i')
		ip_list.append(ip)
		request.session['container_name'] = container_name
		request.session['container_id'] = container_id
		request.session['ip_list'] = ip_list
		request.session['container_type'] = container_type
		all_details = zip(container_name,ip_list,container_id)
		sb.getoutput ('ssh-keyscan '+ip)
		#---- Namenode and other Datanodes
		#---- Namenode and JobTracker on one machine &amp; Datanodes and TaskTracker on others
		if ( service_type == 'nn_dn' or service_type == 'nnjt_dntt' ):
			if ( i == 0 ):
				fhand = open("/etc/ansible/hosts","a+")
				fhand.write('\n[docker-nn]\n')
				fhand.write(ip+'\n')
				fhand.close()
				if ( service_type == 'nn_dn' ):
					container_type.append('NameNode')
				else:
					container_type.append('NameNode & TaskTracker')
			else:
				fhand = open("/etc/ansible/hosts","a+")
				fhand.write('\n[docker-dn]\n')
				fhand.write(ip+'\n')
				fhand.close()
				container_type.append('DataNode')

		#---- Seperate Namenode and JobTracker & Datanodes and TaskTracker on same machines
		elif ( service_type == 'nn_jt_dntt' ):
			if ( i == 0 ):
				fhand = open("/etc/ansible/hosts","a+")
				fhand.write('\n[docker-nn]\n')
				fhand.write(ip+'\n')
				fhand.close()
				container_type.append('NameNode')
			elif ( i == 1 ):
				fhand = open("/etc/ansible/hosts","a+")
				fhand.write('\n[docker-jt]\n')
				fhand.write(ip+'\n')
				fhand.close()
				container_type.append('JobTracker')
			else:
				fhand = open("/etc/ansible/hosts","a+")
				fhand.write('\n[docker-dn]\n')
				fhand.write(ip+'\n')
				fhand.close()
				container_type.append('DataNode & TaskTracker')

		#---- Seperate Namenode, JobTracker, Datanodes and TaskTracker
		else:
			temp = ((int(nodes)-2)/2) + 1
			print (temp)
			if ( i == 0 ):
				fhand = open("/etc/ansible/hosts","a+")
				fhand.write('\n[docker-nn]\n')
				fhand.write(ip+'\n')
				fhand.close()
				container_type.append('NameNode')
			elif ( i == 1 ):
				fhand = open("/etc/ansible/hosts","a+")
				fhand.write('\n[docker-jt]\n')
				fhand.write(ip+'\n')
				fhand.close()
				container_type.append('JobTracker')
			elif ( i>=2 and i<=temp ):
				fhand = open("/etc/ansible/hosts","a+")
				fhand.write('\n[docker-dn]\n')
				fhand.write(ip+'\n')
				fhand.close()
				container_type.append('DataNode')
			else:
				fhand = open("/etc/ansible/hosts","a+")
				fhand.write('\n[docker-tt]\n')
				fhand.write(ip+'\n')
				fhand.close()
				container_type.append('TaskTracker')
	
	return render (request, 'dochv1_playbook.html')

def dochv1_playbook (request):
	service_type = request.session.get('service_type')
	print ('ansible playbook is running...')
	if ( service_type == 'nn_dn' ):
		os.system('sudo ansible-playbook /etc/ansible/playbooks/docker/onlynndn.yml')
	elif ( service_type == 'nnjt_dntt' ):
		os.system('sudo ansible-playbook /etc/ansible/playbooks/docker/nnjt_dntt.yml')
	elif ( service_type == 'nn_jt_dntt' ):
		os.system('sudo ansible-playbook /etc/ansible/playbooks/docker/nn_jt_dntt.yml')
	else:
		os.system('sudo ansible-playbook /etc/ansible/playbooks/docker/nn_jt_dn_tt.yml')
	print("Cleaning hosts")
	open('/etc/ansible/hosts', 'w').close()
	return HttpResponse(status=201)
#---------------------------------------------------- Docker hadoop version 2.7.3-------------------------------------------------------------

def dochadoopv2 (request):
	return render (request, 'dochadoopv2.html')

def postdochadoopv2 (request):
	print('postdochadoopv2...........')
	nodes = request.POST ['nodes']
	service_type.append(stype)
	print ( service_type[0] )
	for i in range (int(nodes)):
		os.system (' sudo docker run -itd --name container'+str(i)+' hadoopv2.7')
		hostname = sb.getoutput('sudo docker exec container'+str(i)+' hostname')
		sb.getoutput ('sudo docker exec '+hostname+' service sshd start')
		ip = sb.getoutput('sudo docker exec container'+str(i)+' hostname -i')
		sb.getoutput ('ssh-keyscan '+ip)
		#---- Namenode and other Datanodes
		#---- Namenode and JobTracker on one machine &amp; Datanodes and TaskTracker on others
		if ( service_type[-1] == 'nn_dn' or service_type[-1] == 'nnrm_dnnm' ):
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
		elif ( service_type[-1] == 'nn_rm_dnnm' ):
			if ( i == 0 ):
				fhand = open("/etc/ansible/hosts","a+")
				fhand.write('\n[docker-nn]\n')
				fhand.write(ip+'\n')
				fhand.close()
			elif ( i == 1 ):
				fhand = open("/etc/ansible/hosts","a+")
				fhand.write('\n[docker-rm]\n')
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
				fhand.write('\n[docker-rm]\n')
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
				fhand.write('\n[docker-nm]\n')
				fhand.write(ip+'\n')
				fhand.close()
	return render (request, 'dochv2_playbook.html')

def dochv2_playbook (request):
	print ('ansible playbook is running...')
	if ( service_type[-1] == 'nn_dn' ):
		os.system('sudo ansible-playbook /etc/ansible/playbooks/docker/hv2_nndn.yml')
	elif ( service_type[-1] == 'nnrm_dnnm' ):
		os.system('sudo ansible-playbook /etc/ansible/playbooks/docker/nnrm_dnnm.yml')
	elif ( service_type[-1] == 'nn_rm_dnnm' ):
		os.system('sudo ansible-playbook /etc/ansible/playbooks/docker/nn_rm_dnnm.yml')
	else:
		os.system('sudo ansible-playbook /etc/ansible/playbooks/docker/nn_rm_dn_nm.yml')

	return HttpResponse(status=201)
