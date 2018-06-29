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

def version (request):
	return render (request, 'version-docker.html')

def hadoopv1 (request):
	return render (request, 'dochadoopv1.html')

def posthadoopv1 (request):
	index_value,ip_list, container_id, container_name, container_type, service_status = ([] for i in range(6))
	nodes = request.POST ['nodes']
	service_type = request.POST ['service_type']
	print(service_type)
	request.session['service_type'] = service_type
	for i in range (int(nodes)):
		os.system (' sudo docker run -itd --privileged --name  container_'+str(i)+' hadoopv1.2')
		container_name.append('container_'+str(i))
		hostname = sb.getoutput('sudo docker exec container_'+str(i)+' hostname')
		container_id.append(hostname)
		sb.getoutput ('sudo docker exec '+hostname+' service sshd start')
		ip = sb.getoutput('sudo docker exec container_'+str(i)+' hostname -i')
		ip_list.append(ip)
		fhand = open("/etc/ansible/hosts","a+")
		# sb.getoutput ('ssh-keyscan '+ip)
		#---- namenode and other datanodes
		if ( service_type == 'nn_dn'):
			if ( i == 0 ):
				fhand.write('\n[docker-nn]\n')
				fhand.write(ip+'\n')
				container_type.append('namenode')
			else:
				fhand.write('\n[docker-dn]\n')
				fhand.write(ip+'\n')
				container_type.append('datanode')
		# -----namenode and jobtracker on one machine &amp; datanodes and tasktracker on others
		elif (service_type == 'nnjt_dntt' ):
			if ( i == 0 ):
				fhand.write('\n[docker-nn]\n')
				fhand.write(ip+'\n')
				container_type.append('namenode & jobtracker')
			else:
				fhand.write('\n[docker-dn]\n')
				fhand.write(ip+'\n')
				container_type.append('datanode & tasktracker')
		#---- Seperate namenode and jobtracker & datanodes and tasktracker on same machines
		elif ( service_type == 'nn_jt_dntt' ):
			if ( i == 0 ):
				fhand.write('\n[docker-nn]\n')
				fhand.write(ip+'\n')
				container_type.append('namenode')
			elif ( i == 1 ):
				fhand.write('\n[docker-jt]\n')
				fhand.write(ip+'\n')
				container_type.append('jobtracker')
			else:
				fhand.write('\n[docker-dn]\n')
				fhand.write(ip+'\n')
				container_type.append('datanode & tasktracker')

		#---- Seperate namenode, jobtracker, datanodes and tasktracker
		elif ( service_type == 'nn_jt_dn_tt' ):
			temp = ((int(nodes)-2)/2) + 1
			if ( i == 0 ):
				fhand.write('\n[docker-nn]\n')
				fhand.write(ip+'\n')
				container_type.append('namenode')
			elif ( i == 1 ):
				fhand.write('\n[docker-jt]\n')
				fhand.write(ip+'\n')
				container_type.append('jobtracker')
			elif ( i>=2 and i<=temp ):
				fhand.write('\n[docker-dn]\n')
				fhand.write(ip+'\n')
				container_type.append('datanode')
			else:
				fhand.write('\n[docker-tt]\n')
				fhand.write(ip+'\n')
				container_type.append('tasktracker')
	
		index_value.append(i)
		service_status.append('Running')
	fhand.close()
	request.session['container_name'] = container_name
	request.session['container_id'] = container_id
	request.session['ip_list'] = ip_list
	request.session['container_type'] = container_type
	request.session['service_status'] = service_status
	request.session['index_value'] = index_value
	return render (request, 'dochv1_playbook.html')

def hv1_playbook (request):
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

def hadoopv2 (request):
	return render (request, 'dochadoopv2.html')

def posthadoopv2 (request):
	index_value,ip_list, container_id, container_name, container_type, service_status = ([] for i in range(6))
	nodes = request.POST ['nodes']
	service_type = request.POST ['service_type']
	request.session['service_type'] = service_type
	for i in range (int(nodes)):
		os.system (' sudo docker run -itd --privileged --name container_'+str(i)+' hadoopv2.7')
		container_name.append('container_'+str(i))
		hostname = sb.getoutput('sudo docker exec container_'+str(i)+' hostname')
		container_id.append(hostname)
		sb.getoutput ('sudo docker exec '+hostname+' service sshd start')
		ip = sb.getoutput('sudo docker exec container_'+str(i)+' hostname -i')
		ip_list.append(ip)
		fhand = open("/etc/ansible/hosts","a+")
		#---- namenode and other datanodes
		if ( service_type == 'nn_dn'):
			if ( i == 0 ):
				fhand.write('\n[docker-nn]\n')
				fhand.write(ip+'\n')
				container_type.append('namenode')
			else:
				fhand.write('\n[docker-dn]\n')
				fhand.write(ip+'\n')
				container_type.append('datanode')
		#---- namenode and jobtracker on one machine &amp; datanodes and tasktracker on others
		elif ( service_type == 'nnrm_dnnm' ):
			if ( i == 0 ):
				fhand.write('\n[docker-nn]\n')
				fhand.write(ip+'\n')
				container_type.append('namenode & resourcemanager')
			else:
				fhand.write('\n[docker-dn]\n')
				fhand.write(ip+'\n')
				container_type.append('datanode & nodemanager')
		#---- Seperate namenode and jobtracker & datanodes and tasktracker on same machines
		elif ( service_type == 'nn_rm_dnnm' ):
			if ( i == 0 ):
				fhand.write('\n[docker-nn]\n')
				fhand.write(ip+'\n')
				container_type.append('namenode')
			elif ( i == 1 ):
				fhand.write('\n[docker-rm]\n')
				fhand.write(ip+'\n')
				container_type.append('resourcemanager')
			else:
				fhand.write('\n[docker-dn]\n')
				fhand.write(ip+'\n')
				container_type.append('datanode & nodemanager')
		#---- Seperate namenode, jobtracker, datanodes and tasktracker
		else:
			temp = ((int(nodes)-2)/2) + 1
			if ( i == 0 ):
				fhand.write('\n[docker-nn]\n')
				fhand.write(ip+'\n')
				container_type.append('namenode')
			elif ( i == 1 ):
				fhand.write('\n[docker-rm]\n')
				fhand.write(ip+'\n')
				container_type.append('resourcemanager')
			elif ( i>=2 and i<=temp ):
				fhand.write('\n[docker-dn]\n')
				fhand.write(ip+'\n')
				container_type.append('datanode')
			else:
				fhand.write('\n[docker-nm]\n')
				fhand.write(ip+'\n')
				container_type.append('nodemanager')

		index_value.append(i)
		service_status.append('Running')
	fhand.close()
	request.session['container_name'] = container_name
	request.session['container_id'] = container_id
	request.session['ip_list'] = ip_list
	request.session['container_type'] = container_type
	request.session['service_status'] = service_status
	request.session['index_value'] = index_value
	return render (request, 'dochv2_playbook.html')

def hv2_playbook (request):
	print ('ansible playbook is running...')
	service_type = request.session.get('service_type')
	if ( service_type == 'nn_dn' ):
		os.system('sudo ansible-playbook /etc/ansible/playbooks/docker/hv2_nndn.yml')
	elif ( service_type == 'nnrm_dnnm' ):
		os.system('sudo ansible-playbook /etc/ansible/playbooks/docker/nnrm_dnnm.yml')
	elif ( service_type == 'nn_rm_dnnm' ):
		os.system('sudo ansible-playbook /etc/ansible/playbooks/docker/nn_rm_dnnm.yml')
	else:
		os.system('sudo ansible-playbook /etc/ansible/playbooks/docker/nn_rm_dn_nm.yml')
	
	open('/etc/ansible/hosts', 'w').close()
	return HttpResponse(status=201)

def clear_cluster (request):
	sb.getoutput ('docker kill $(docker ps -qa)')
	sb.getoutput ('docker rm $(docker ps -qa)')
	container_name = request.session.get('container_name')
	container_id = request.session.get('container_id')
	ip_list = request.session.get('ip_list')
	service_status = request.session.get('service_status')
	index_value = request.session.get('index_value')
	request.session['container_name'] = None
	request.session['container_id'] = None
	request.session['ip_list'] = None
	request.session['container_type'] = None
	request.session['index_value'] = None
	request.session['service_status'] = None
	return redirect ('/dashboard/')