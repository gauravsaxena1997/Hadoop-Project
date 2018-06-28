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


#---------------------------------------------------- Docker hadoop version 1.2.1-------------------------------------------------------------
def dochadoopv1 (request):
	return render (request, 'dochadoopv1.html')

# def postdochadoopv1 (request):
# 	index_value,ip_list, container_id, container_name, container_type, service_status = ([] for i in range(6))
# 	nodes = request.POST ['nodes']
# 	service_type = request.POST ['service_type']
# 	request.session['service_type'] = service_type
# 	for i in range (int(nodes)):
# 		os.system (' sudo docker run -itd --privileged --name  container_'+str(i)+' hadoopv1.2')
# 		container_name.append('container_'+str(i))
# 		hostname = sb.getoutput('sudo docker exec container_'+str(i)+' hostname')
# 		hostname = str(hostname)
# 		container_id.append(hostname)
# 		ip = sb.getoutput('sudo docker exec container_'+str(i)+' hostname -i')
# 		ip = str(ip)
# 		ip_list.append(ip)
# 		sb.getoutput ('sudo docker exec '+hostname+' service sshd start')
# 		request.session['container_name'] = container_name
# 		request.session['container_id'] = container_id
# 		request.session['ip_list'] = ip_list
# 		request.session['container_type'] = container_type
# 		request.session['service_status'] = service_status
# 		request.session['index_value'] = index_value
# 		sb.getoutput ('ssh-keyscan '+ip)
# 		fhand = open("/etc/ansible/hosts","a+")
# 		#---- namenode and other datanodes
# 		#---- namenode and jobtracker on one machine &amp; datanodes and tasktracker on others
# 		if ( service_type == 'nn_dn' or service_type == 'nnjt_dntt' ):
# 			print('inside it..........')
# 			if ( i == 0 ):
# 				fhand.write('\n[docker-nn]\n')
# 				fhand.write(ip+'\n')
# 				if ( service_type == 'nn_dn' ):
# 					container_type.append('namenode')
# 				else:
# 					container_type.append('namenode & jobtracker')
# 			else:
# 				fhand.write('\n[docker-dn]\n')
# 				fhand.write(ip+'\n')
# 				if ( service_type == 'nn_dn' ):
# 					container_type.append('datanode')
# 				else:
# 					container_type.append('datanode & tasktracker')

# 		#---- Seperate namenode and jobtracker & datanodes and tasktracker on same machines
# 		elif ( service_type == 'nn_jt_dntt' ):
# 			if ( i == 0 ):
# 				fhand.write('\n[docker-nn]\n')
# 				fhand.write(ip+'\n')
# 				container_type.append('namenode')
# 			elif ( i == 1 ):
# 				fhand.write('\n[docker-jt]\n')
# 				fhand.write(ip+'\n')
# 				container_type.append('jobtracker')
# 			else:
# 				fhand.write('\n[docker-dn]\n')
# 				fhand.write(ip+'\n')
# 				container_type.append('datanode & tasktracker')

# 		#---- Seperate namenode, jobtracker, datanodes and tasktracker
# 		else:
# 			temp = ((int(nodes)-2)/2) + 1
# 			print (temp)
# 			if ( i == 0 ):
# 				fhand.write('\n[docker-nn]\n')
# 				fhand.write(ip+'\n')
# 				container_type.append('namenode')
# 			elif ( i == 1 ):
# 				fhand.write('\n[docker-jt]\n')
# 				fhand.write(ip+'\n')
# 				container_type.append('jobtracker')
# 			elif ( i>=2 and i<=temp ):
# 				fhand.write('\n[docker-dn]\n')
# 				fhand.write(ip+'\n')
# 				container_type.append('datanode')
# 			else:
# 				fhand.write('\n[docker-tt]\n')
# 				fhand.write(ip+'\n')
# 				container_type.append('tasktracker')
	
# 		index_value.append(i)
# 		service_status.append('Running')
# 	fhand.close()
# 	return render (request, 'dochv1_playbook.html')


def postdochadoopv1 (request):
	index_value,ip_list, container_id, container_name, container_type, service_status = ([] for i in range(6))
	nodes = request.POST ['nodes']
	service_type = request.POST ['service_type']
	request.session['service_type'] = service_type
	for i in range (int(nodes)):
		sb.getoutput (' sudo docker run -itd --privileged --name  container_'+str(i)+' hadoopv1.2')
		container_name.append('container_'+str(i))
		hostname = sb.getoutput('sudo docker exec container_'+str(i)+' hostname')
		container_id.append(hostname)
		ip = sb.getoutput('sudo docker exec container_'+str(i)+' hostname -i')
		ip_list.append(ip)
		sb.getoutput ('sudo docker exec '+hostname+' service sshd start')
		request.session['container_name'] = container_name
		request.session['container_id'] = container_id
		request.session['ip_list'] = ip_list
		request.session['container_type'] = container_type
		request.session['service_status'] = service_status
		request.session['index_value'] = index_value
		sb.getoutput ('ssh-keyscan '+ip)
		#---- namenode and other datanodes
		#---- namenode and jobtracker on one machine &amp; datanodes and tasktracker on others
		if ( service_type == 'nn_dn' or service_type == 'nnjt_dntt' ):
			if ( i == 0 ):
				fhand = open("/etc/ansible/hosts","a+")
				fhand.write('\n[docker-nn]\n')
				fhand.write(ip+'\n')
				fhand.close()
				if ( service_type == 'nn_dn' ):
					container_type.append('namenode')
				else:
					container_type.append('namenode & jobtracker')
			else:
				fhand = open("/etc/ansible/hosts","a+")
				fhand.write('\n[docker-dn]\n')
				fhand.write(ip+'\n')
				fhand.close()
				container_type.append('datanode')

		#---- Seperate namenode and jobtracker & datanodes and tasktracker on same machines
		elif ( service_type == 'nn_jt_dntt' ):
			if ( i == 0 ):
				fhand = open("/etc/ansible/hosts","a+")
				fhand.write('\n[docker-nn]\n')
				fhand.write(ip+'\n')
				fhand.close()
				container_type.append('namenode')
			elif ( i == 1 ):
				fhand = open("/etc/ansible/hosts","a+")
				fhand.write('\n[docker-jt]\n')
				fhand.write(ip+'\n')
				fhand.close()
				container_type.append('jobtracker')
			else:
				fhand = open("/etc/ansible/hosts","a+")
				fhand.write('\n[docker-dn]\n')
				fhand.write(ip+'\n')
				fhand.close()
				container_type.append('datanode & tasktracker')

		#---- Seperate namenode, jobtracker, datanodes and tasktracker
		else:
			temp = ((int(nodes)-2)/2) + 1
			print (temp)
			if ( i == 0 ):
				fhand = open("/etc/ansible/hosts","a+")
				fhand.write('\n[docker-nn]\n')
				fhand.write(ip+'\n')
				fhand.close()
				container_type.append('namenode')
			elif ( i == 1 ):
				fhand = open("/etc/ansible/hosts","a+")
				fhand.write('\n[docker-jt]\n')
				fhand.write(ip+'\n')
				fhand.close()
				container_type.append('jobtracker')
			elif ( i>=2 and i<=temp ):
				fhand = open("/etc/ansible/hosts","a+")
				fhand.write('\n[docker-dn]\n')
				fhand.write(ip+'\n')
				fhand.close()
				container_type.append('datanode')
			else:
				fhand = open("/etc/ansible/hosts","a+")
				fhand.write('\n[docker-tt]\n')
				fhand.write(ip+'\n')
				fhand.close()
				container_type.append('tasktracker')
	
		index_value.append(i)
		service_status.append('Running')
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
	index_value,ip_list, container_id, container_name, container_type, service_status = ([] for i in range(6))
	nodes = request.POST ['nodes']
	service_type = request.POST ['service_type']
	request.session['service_type'] = service_type
	for i in range (int(nodes)):
		os.system (' sudo docker run -itd --privileged --name container_'+str(i)+' hadoopv2.7')
		container_name.append('container_'+str(i))
		hostname = os.system('sudo docker exec container_'+str(i)+' hostname')
		container_id.append(hostname)
		ip = os.system('sudo docker exec container_'+str(i)+' hostname -i')
		ip_list.append(ip)
		os.system ('sudo docker exec '+hostname+' service sshd start')
		request.session['container_name'] = container_name
		request.session['container_id'] = container_id
		request.session['ip_list'] = ip_list
		request.session['container_type'] = container_type
		request.session['service_status'] = service_status
		request.session['index_value'] = index_value
		os.system ('ssh-keyscan '+ip)
		fhand = open("/etc/ansible/hosts","a+")
		#---- namenode and other datanodes
		#---- namenode and jobtracker on one machine &amp; datanodes and tasktracker on others
		if ( service_type == 'nn_dn' or service_type == 'nnrm_dnnm' ):
			if ( i == 0 ):
				fhand.write('\n[docker-nn]\n')
				fhand.write(ip+'\n')
				if ( service_type == 'nn_dn' ):
					container_type.append('namenode')
				else:
					container_type.append('namenode & resourcemanager')
			else:
				fhand.write('\n[docker-dn]\n')
				fhand.write(ip+'\n')
				container_type.append('datanode')

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
			print (temp)
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
	return render (request, 'dochv2_playbook.html')

def dochv2_playbook (request):
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

	return HttpResponse(status=201)


# --------------------------------------------------------------------VM----------------------------------------------------------
def version_vm (request):
	return render (request, 'version-vm.html')

def vmhadoopv1 (request):
	return render (request, 'vmhadoopv1.html')


def postvmhadoopv1 (request):
	print('postvmhadoopv1')
	nodes = request.POST ['nodes']
	ram = request.POST ['ram']
	cpu = request.POST ['cpu']
	service_type = request.POST ['service_type']
	request.session['service_type'] = service_type
	for i in range (1, int(nodes)+1):
		os.system('sudo qemu-img create -f qcow2 -b /var/lib/libvirt/images/hadoopv1.qcow2 /var/lib/libvirt/images/node'+str(i)+'.qcow2')
		os.system('sudo virt-install --ram ' +ram+ ' --vcpu '+cpu+' --disk path=/var/lib/libvirt/images/node'+str(i)+'.qcow2 --import --name node'+str(i)+' --noautoconsole')
	return render (request, 'loading_vm_hv1.html')

def loading_vm_hv1 (request):
	service_type = request.session.get('service_type')
	fhand = open("/etc/ansible/hosts","a+")
	ip_list = []
	service_provided = []
	ip_list.append('192.168.122.1')
	if ( service_type == 'nn_dn' or service_type == 'nn_jt_dntt'):
		service_provided.append('namenode')
	elif ( service_type == 'nnjt_dntt' ):
		service_provided.append('namenode & jobtracker')
		fhand.write('\n[vm-jt]\n')
		fhand.write(ip_list[0])
	ip = os.system("nmap -n -sn 192.168.122.1/24 -oG - | awk '/Up$/{print $2}'")
	ip_list.extend(ip.split())
	ip_list.pop()
	print(ip_list)
	for i in ip_list[1:]:
	# #---- namenode and other datanodes
		if ( service_type == 'nn_dn'):
			fhand.write('\n[vm-dn]\n')
			fhand.write(i)
			service_provided.append('datanode')
	# #---- namenode and jobtracker on one machine &amp; datanodes and tasktracker on others
		elif (service_type == 'nnjt_dntt' ):
			fhand.write('\n[vm-dn-tt]\n')
			fhand.write(i)
			service_provided.append('datanode & tasktracker')
	# #---- Seperate namenode and jobtracker & datanodes and tasktracker on same machines
		elif ( service_type == 'nn_jt_dntt' ):
			if ( i == ip_list[1] ):
				print(i)
				fhand.write('\n[vm-jt]\n')
				fhand.write(i)
				container_type.append('jobtracker')
			else:
				print(i)
				fhand.write('\n[vm-dn]\n')
				fhand.write(ip+'\n')
				container_type.append('datanode & tasktracker')
	fhand.close()
	print(service_provided)
	return render (request, 'vmhv1_playbook.html')

def vmhv1_playbook (request):
	service_type = request.session.get('service_type')
	if ( service_type == 'nn_dn' ):
		os.system('sudo ansible-playbook /etc/ansible/playbooks/vm/onlynndn.yml')
	elif ( service_type == 'nnjt_dntt' ):
		os.system('sudo ansible-playbook /etc/ansible/playbooks/vm/nnjt_dntt.yml')
	elif ( service_type == 'nn_jt_dntt' ):
		os.system('sudo ansible-playbook /etc/ansible/playbooks/vm/nn_jt_dntt.yml')
	print("Cleaning hosts")
	# open('/etc/ansible/hosts', 'w').close()
	return HttpResponse(status=201)

# -----------------------------------hadoop v2 VM ----------------------------------------------

def vmhadoopv2 (request):
	return render (request, 'vmhadoopv2.html')

def postvmhadoopv2 (request):
	print('postvmhadoopv2')
	nodes = request.POST ['nodes']
	ram = request.POST ['ram']
	cpu = request.POST ['cpu']
	service_type = request.POST ['service_type']
	request.session['service_type'] = service_type
	for i in range (1, int(nodes)+1):
		os.system('sudo qemu-img create -f qcow2 -b /var/lib/libvirt/images/hadoopv2.qcow2 /var/lib/libvirt/images/node'+str(i)+'.qcow2')
		os.system('sudo virt-install --ram ' +ram+ ' --vcpu '+cpu+' --disk path=/var/lib/libvirt/images/node'+str(i)+'.qcow2 --import --name node'+str(i)+' --noautoconsole')
	return render (request, 'loading_vm_hv2.html')

def loading_vm_hv2 (request):
	service_type = request.session.get('service_type')
	fhand = open("/etc/ansible/hosts","a+")
	ip_list = []
	service_provided = []
	ip_list.append('192.168.122.1')
	if ( service_type == 'nn_dn' or service_type == 'nn_rm_dnnm'):
		service_provided.append('namenode')
	elif ( service_type == 'nnrm_dnnm' ):
		service_provided.append('namenode & resourcemanager')
		fhand.write('\n[vm-rm]\n')
		fhand.write(ip_list[0])
	ip = os.system("nmap -n -sn 192.168.122.1/24 -oG - | awk '/Up$/{print $2}'")
	ip_list.extend(ip.split())
	ip_list.pop()
	print(ip_list)
	for i in ip_list[1:]:
	# #---- namenode and other datanodes
		if ( service_type == 'nn_dn'):
			fhand.write('\n[vm-dn]\n')
			fhand.write(i)
			service_provided.append('datanode')
	# #---- namenode and jobtracker on one machine &amp; datanodes and tasktracker on others
		elif (service_type == 'nnjt_dntt' ):
			fhand.write('\n[vm-dn-tt]\n')
			fhand.write(i)
			service_provided.append('datanode & tasktracker')
	# #---- Seperate namenode and jobtracker & datanodes and tasktracker on same machines
		elif ( service_type == 'nn_jt_dntt' ):
			if ( i == ip_list[1] ):
				print(i)
				fhand.write('\n[vm-jt]\n')
				fhand.write(i)
				container_type.append('jobtracker')
			else:
				print(i)
				fhand.write('\n[vm-dn]\n')
				fhand.write(ip+'\n')
				container_type.append('datanode & tasktracker')
	fhand.close()
	print(service_provided)
	return render (request, 'vmhv2_playbook.html')

def vmhv2_playbook (request):
	service_type = request.session.get('service_type')
	print('success......')
	time.sleep(15)
	# if ( service_type == 'nn_dn' ):
	# 	os.system('sudo ansible-playbook /etc/ansible/playbooks/vm/onlynndn.yml')
	# elif ( service_type == 'nnjt_dntt' ):
	# 	os.system('sudo ansible-playbook /etc/ansible/playbooks/vm/nnjt_dntt.yml')
	# elif ( service_type == 'nn_jt_dntt' ):
	# 	os.system('sudo ansible-playbook /etc/ansible/playbooks/vm/nn_jt_dntt.yml')
	# print("Cleaning hosts")
	# open('/etc/ansible/hosts', 'w').close()
	return HttpResponse(status=201)



