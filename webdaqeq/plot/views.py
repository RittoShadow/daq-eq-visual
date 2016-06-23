# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.generic import FormView
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout

import matplotlib
import subprocess
matplotlib.use('Agg')
import netifaces as net
import plot
import os
import io
import re
import time
from PIL import Image
from matplotlib.backends.backend_agg import FigureCanvasAgg
from models import configForm, notifyForm
from command_client import *

daqeq_home = settings.DAQEQ_HOME

def home(request):
	return render(request, "plot/home.html", {})

def loginDAQEQ(request):
	if request.method == "POST":
	    username = request.POST['username']
	    password = request.POST['password']
	    user = authenticate(username=username, password=password)
	    if user is not None:
	        if user.is_active:
	            login(request, user)
	            return render(request, "plot/home.html", { "page_title" : "Bienvenido, "+username , "page_content" : "Has iniciado sesión."})
	        else:
	            return render(request, "plot/home.html", { "page_title" : "Bienvenido, intruso" , "page_content" : "No has iniciado sesión."})
	    else:
			return render(request, "registration/login.html", { "page_title" : "Error" , "page_content" : "Combinación de usuario y contraseña incorrectas."})
	else:
		return render(request, "registration/login.html", {})

def logoutDAQEQ(request):
	logout(request)
	return render(request, "plot/home.html", {})

@login_required(login_url="/plot/login/")
def index(request):
	files = sorted(map(lambda p : daqeq_home+'trunk/enviados/'+str(p), os.listdir(daqeq_home+'trunk/enviados')), key=os.path.getsize)
	files = files + map(lambda p: daqeq_home+"trunk/"+str(p), os.listdir(daqeq_home+'trunk/'))
	files = filter(lambda p : re.search("[\w_-]+TEST[\w_-]+\.txt",p),files)
	return render(request, "plot/index.html", { "buffer" : files , "page_title" : "Seleccione un archivo:" })
# Create your views here.

def formatData(request):
	if request.method == "POST":
		buff = request.POST["to_plot"]
		if buff:
			return render(request, "plot/index.html", { "page_title" : "Visualización" , "plot" : True , "data" : buff })
		else:
			files = sorted(map(lambda p : '/home/pi/Desktop/daqeq/trunk/enviados/'+str(p), os.listdir('/home/pi/Desktop/daqeq/trunk/enviados')), key=os.path.getctime)
			return render(request, 'plot/index.html', { "graph" : "Something to show, but no" , "file" : files[-1] })
	else:
		return render(request, 'plot/index.html',{ "graph" : "Nothing to show"})

def subscribe(request):
	ip = net.ifaddresses('eth0')[2][0]['addr']
	return render(request, 'plot/plot.html', { "ip" : ip })

def newPlot(request,data):
	data = plot.parse(data)
	figure = plot.staticPlot(data)
	canvas = FigureCanvasAgg(figure)
	response = HttpResponse(content_type='image/png')
	canvas.print_png(response)
	return response

def config(request):
	if request.method == "POST":
		return request
	else:
		configData = parseConfigFile(request)
		return render(request, 'plot/config.html', configData)

def parseConfigFile(request):
	return {}

def start_stop_signal(request):
	import os, signal
	# Obtener PID del proceso de app en c++ de daq-eq
	pid = os.popen("pgrep 'RBA-DAQ-EQ'").read()
	if (pid) :
		if "command" in request.POST:
			if request.POST["command"] == "stop":
			    # Enviar signal SIG_USR1 a app en c++, para iniciar/detener adquirir datos
				os.kill(int(pid), signal.SIGUSR1) # Unix version only...
			elif request.POST["command"] == "start":
				command_server("0")
			elif request.POST["command"] == "trigger":
				os.kill(int(pid), signal.SIGALRM)
		else:
			os.kill(int(pid), signal.SIGUSR1)
	if request.POST["this_url"]:
		return redirect(request.POST["this_url"])

def ask_daqeq_status():
	import os

	# Obtener PID del proceso de app en c++ de daq-eq
	route = settings.BASE_DIR+"/plot"
	os.chdir(route)
	#t = subprocess.Popen(["sudo","python","ask_daqeq_status.py"],stdout=PIPE)
	result = int(os.popen("sudo python ask_daqeq_status.py").read().strip())
	print "Result is: "+str(result)
	if result == 0:
		return "Reiniciar"
	elif result == 1:
		return "Detener"
	else:
		return "Error"

@login_required(login_url="/plot/login/")
def view(request):
	return render(request, 'plot/views.html', {})

@login_required(login_url="/plot/login/")
def sensor(request):
	if request.POST['command'] == 'refresh':
		ans = command_server("elg")
		print "Refresh"
	elif request.POST['command'] == 'add':
		ans = command_server("sms", request.POST['serial'])
		return JsonResponse(ans.split(";"), safe=False)
	sensor = command_server("cag")
	return JsonResponse(sensor, safe=False)

@login_required(login_url="/plot/login/")
def configVerification(request):
	route = settings.BASE_DIR+"/plot"
	os.chdir(route)
	if request.method == "POST":
		if request.POST["this_url"] == "/plot/config/":
			sensorParams = ""
			if "enableAutoStart" in request.POST:
				command_server("east")
			else:
				command_server("easf")
			if "enableTrigger" in request.POST:
				command_server("etst")
			else:
				command_server("etsf")
			if "enableRecording" in request.POST:
				command_server("erst")
			else:
				command_server("ersf")
			if request.POST["graphWindow"]:
				command_server("ngs",request.POST["graphWindow"])
			if request.POST["filterWindow"]:
				command_server("nfs",request.POST["filterWindow"])
			if request.POST["preEventTime"]:
				command_server("nas",request.POST["preEventTime"])
			if request.POST["postEventTime"]:
				command_server("nbs",request.POST["postEventTime"])
			if request.POST["minTimeRunning"]:
				command_server("nms",request.POST["minTimeRunning"])
			if request.POST["votes"]:
				command_server("nvs",request.POST["votes"])
			if request.POST["recordLength"]:
				command_server("nrs",request.POST["recordLength"])
			if request.POST["portNumber"]:
				command_server("nps",request.POST["portNumber"])
			if request.POST["filenameFormat"]:
				command_server("sfs",request.POST["filenameFormat"])
			if request.POST["serverURL"]:
				command_server("sus",request.POST["serverURL"])
			if request.POST["networkName"]:
				command_server("sns",request.POST["networkName"])
			if request.POST["outputDir"]:
				command_server("sos",request.POST["outputDir"])
			listSensorParams = []
			if request.POST.getlist("serialNum"):
				for i in range(len(request.POST.getlist("serialNum"))):
					sensorParams = request.POST.getlist("serialNum")[i] + ";"
					if request.POST.getlist("position")[i]:
						sensorParams = sensorParams + request.POST.getlist("position")[i].strip(";") + ";"
					if request.POST.getlist("triggerX")[i]:
						sensorParams = sensorParams + request.POST.getlist("triggerX")[i].strip(";") + ";"
					if request.POST.getlist("triggerY")[i]:
						sensorParams = sensorParams + request.POST.getlist("triggerY")[i].strip(";") + ";"
					if request.POST.getlist("triggerZ")[i]:
						sensorParams = sensorParams + request.POST.getlist("triggerZ")[i].strip(";") + ";"
					if request.POST.getlist("detriggerX")[i]:
						sensorParams = sensorParams + request.POST.getlist("detriggerX")[i].strip(";") + ";"
					if request.POST.getlist("detriggerY")[i]:
						sensorParams = sensorParams + request.POST.getlist("detriggerY")[i].strip(";") + ";"
					if request.POST.getlist("detriggerZ")[i]:
						sensorParams = sensorParams + request.POST.getlist("detriggerZ")[i].strip(";") + ";"
					if request.POST.getlist("detrend")[i]:
						sensorParams = sensorParams + request.POST.getlist("detrend")[i].strip(";") + ";"
					if request.POST.getlist("votesX")[i]:
						sensorParams = sensorParams + request.POST.getlist("votesX")[i].strip(";") + ";"
					if request.POST.getlist("votesY")[i]:
						sensorParams = sensorParams + request.POST.getlist("votesY")[i].strip(";") + ";"
					if request.POST.getlist("votesZ")[i]:
						sensorParams = sensorParams + request.POST.getlist("votesZ")[i].strip(";") + ";"
					if "check"+request.POST.getlist("serialNum")[i] in request.POST:
						sensorParams = sensorParams + "1;"
					else:
						sensorParams = sensorParams + "0;"
					if request.POST["isRed"+request.POST.getlist("serialNum")[i]] == "true":
						sensorParams = sensorParams + "1;"
					else:
						sensorParams = sensorParams + "0;"
					if len(sensorParams.split(";"))==15:
						print "Sending..."
						listSensorParams.append(sensorParams)
			command_server("cas",listSensorParams)
			command_server("0")
		elif request.POST["this_url"] == "/plot/notification/":
			if request.POST["sendFrequency"]:
				command_server("nss",request.POST["sendFrequency"])
			if request.POST["verificationFrequency"]:
				command_server("nos",request.POST["verificationFrequency"])
			if request.POST["username"]:
				command_server("sis",request.POST["username"])
			if request.POST["password"]:
				command_server("sps",request.POST["password"])
			if request.POST["structure"]:
				command_server("sss",request.POST["structure"])
			if request.POST["email"]:
				command_server("ses",request.POST["email"])
			if request.POST["phoneNumber"]:
				command_server("sts",request.POST["phoneNumber"])
			if request.POST["authenticationURL"]:
				command_server("sas",request.POST["authenticationURL"])
			if request.POST["recordURL"]:
				command_server("srs",request.POST["recordURL"])
			if request.POST["structHealthURL"]:
				command_server("shs",request.POST["structHealthURL"])
			if "sendSMS" in request.POST:
				command_server("emst")
			else:
				command_server("emsf")
			if "sendRecord" in request.POST:
				command_server("esst")
			else:
				command_server("essf")
			if "compressRecord" in request.POST:
				command_server("ecst")
			else:
				command_server("ecsf")
			if "sendStructHealth" in request.POST:
				command_server("ehst")
			else:
				command_server("ehsf")
			command_server("0")
		else:
			return request
	return redirect(request.POST["this_url"])

class ConfigurationFormView(FormView):
	template_name = 'plot/notification.html'
	form_class = configForm

	def __init__(self, *args, **kwargs):
		route = settings.BASE_DIR+"/plot"
		os.chdir(route)
		if command_server("eag") == "1":
			self.initial['enableAutoStart'] = 'on'
		else:
			self.initial['enableAutoStart'] = None
		if command_server("etg") == "1":
			self.initial['enableTrigger'] = 'on'
		else:
			self.initial['enableTrigger'] = None
		if command_server("erg") == "1":
			self.initial['enableRecording'] = 'on'
		else:
			self.initial['enableRecording'] = None
		self.initial['graphWindow'] = command_server("ngg")
		self.initial['filterWindow'] = command_server("nfg")
		self.initial['preEventTime'] = command_server("nag")
		self.initial['postEventTime'] = command_server("nbg")
		self.initial['minTimeRunning'] = command_server("nmg")
		self.initial['votes'] = command_server("nvg")
		self.initial['recordLength'] = command_server("nrg")
		self.initial['portNumber'] = command_server("npg")
		self.initial['filenameFormat'] = command_server("sfg")
		self.initial['serverURL'] = command_server("sug")
		self.initial['networkName'] = command_server("sng")
		self.initial['outputDir'] = command_server("sog")
		super(ConfigurationFormView, self).__init__(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(ConfigurationFormView, self).get_context_data(**kwargs)
		context["page_title"] = "Configuración"
		context["this_url"] = "/plot/config/"
		context["action_text"] = ask_daqeq_status()
		context["sensors"] = command_server("cag")
		return context


class NotificationFormView(FormView):
	template_name = 'plot/notification.html'
	form_class = notifyForm

	def __init__(self, *args, **kwargs):
		route = settings.BASE_DIR+"/plot"
		os.chdir(route)
		if command_server("emg") == "1":
			self.initial['sendSMS'] = 'on'
		else:
			self.initial['sendSMS'] = None
		if command_server("esg") == "1":
			self.initial['sendRecord'] = 'on'
		else:
			self.initial['sendRecord'] = None
		if command_server("ecg") == "1":
			self.initial['compressRecord'] = 'on'
		else:
			self.initial['compressRecord'] = None
		if command_server("ehg") == "1":
			self.initial['sendStructHealth'] = 'on'
		else:
			self.initial['sendStructHealth'] = None
		self.initial["sendFrequency"] = command_server("nsg")
		self.initial["verificationFrequency"] = command_server("nog")
		self.initial["username"] = command_server("sig")
		self.initial["password"] = command_server("spg")
		self.initial["structure"] = command_server("ssg")
		self.initial["email"] = command_server("seg")
		self.initial["phoneNumber"] = command_server("stg")
		self.initial["authenticationURL"] = command_server("sag")
		self.initial["recordURL"] = command_server("srg")
		self.initial["structHealthURL"] = command_server("shg")
		super(NotificationFormView, self).__init__(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(NotificationFormView, self).get_context_data(**kwargs)
		context["page_title"] = "Notificaciones"
		context["this_url"] = "/plot/notification/"
		context["action_text"] = ask_daqeq_status()
		return context
