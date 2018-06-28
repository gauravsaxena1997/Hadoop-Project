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
import sys,os,time

def version (request):
	return render (request, 'version-vm.html')

def hadoopv1 (request):
	return render (request, 'vmhadoopv1.html')


def posthadoopv1 (request):
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

def loading_hv1 (request):
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
	ip = sb.getoutput("nmap -n -sn 192.168.122.1/24 -oG - | awk '/Up$/{print $2}'")
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

def hv1_playbook (request):
	service_type = request.session.get('service_type')
	if ( service_type == 'nn_dn' ):
		os.system('sudo ansible-playbook /etc/ansible/playbooks/vm/onlynndn.yml')
	elif ( service_type == 'nnjt_dntt' ):
		os.system('sudo ansible-playbook /etc/ansible/playbooks/vm/nnjt_dntt.yml')
	elif ( service_type == 'nn_jt_dntt' ):
		os.system('sudo ansible-playbook /etc/ansible/playbooks/vm/nn_jt_dntt.yml')
	print("Cleaning hosts")
	open('/etc/ansible/hosts', 'w').close()
	vm = 'vm'
	request.session['vm'] = vm
	return redirect ('/dashboard/')

# ------------------------------------------------------------hadoop v2 ---------------------------------------------------------------------

def hadoopv2 (request):
	return render (request, 'vmhadoopv2.html')

def posthadoopv2 (request):
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

def loading_hv2 (request):
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
	return redirect('/dashboard')

def hv2_playbook (request):
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