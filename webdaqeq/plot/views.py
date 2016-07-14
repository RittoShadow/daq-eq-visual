# -*- coding: utf-8 -*-
# Django
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.generic import FormView
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt,csrf_protect

# Standard
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg
import subprocess
import json
import zipfile
import StringIO
import netifaces as net
import plot
import os
from os.path import basename
import io
import re
import time
from PIL import Image
from models import configForm, notifyForm
from command_client import *

# Initializations
daqeq_home = settings.DAQEQ_HOME

@login_required(login_url="/plot/login/")
def home(request):
	"""
	Vista de home
	"""
	return render(request, "plot/home.html", {})

def loginDAQEQ(request):
	"""
	Login de app-web
	"""
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
	"""
	Logout de app-web
	"""
	logout(request)
	return render(request, "plot/home.html", {})

@login_required(login_url="/plot/login/")
def index(request):
	"""
	Datos de archivos .txt de daqeq
	"""
	files = sorted(map(lambda p : daqeq_home+'trunk/enviados/'+str(p), os.listdir(daqeq_home+'trunk/enviados')), key=os.path.getsize)
	files = files + map(lambda p: daqeq_home+"trunk/"+str(p), os.listdir(daqeq_home+'trunk/'))
	files = filter(lambda p : re.search("[\w_-]+TEST[\w_-]+\.txt",p),files)
	return render(request, "plot/index.html", { "files_list" : files , "page_title" : "" })

def formatData(request):
	"""
	Graficar
	"""
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
	# ip = 'localhost'
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
	"""
	Iniciar o Detener daqeq c++
	"""
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
	"""
	Preguntar estado de app c++
	"""
	# Obtener PID del proceso de app en c++ de daq-eq
	route = settings.BASE_DIR+"/plot"
	os.chdir(route)
	result = 0
	try:
		#result = int(subprocess.Popen(["sudo","python","ask_daqeq_status.py"], stdout=subprocess.PIPE).stdout.read().strip())
		result = int(os.popen("sudo python ask_daqeq_status.py").read().strip())
	except ValueError:
		result = -1
	if result == 0:
		return "Guardar"
	elif result == 1:
		return "Detener"
	else:
		return "Error"

@login_required(login_url="/plot/login/")
def view(request):
	ip = net.ifaddresses('eth0')[2][0]['addr']
	# ip = 'localhost'
	return render(request, 'plot/views.html', { "this_url" : "/plot/views/", "ip" : ip})

@csrf_exempt #This skips csrf validation. Use csrf_protect to have validation
@login_required(login_url="/plot/login/")
def sensor(request):
	"""
	Actualizar sensores, o agregar manualmente en vista de config
	"""
	if request.POST['command'] == 'refresh':
		ans = command_server("elg")
		print "Refresh"
	elif request.POST['command'] == 'add':
		ans = command_server("sms", request.POST['serial'])
		return JsonResponse(ans.split(";"), safe=False)
	sensor = command_server("cag")
	return JsonResponse(sensor, safe=False)

@csrf_exempt #This skips csrf validation. Use csrf_protect to have validation
@login_required(login_url="/plot/login/")
def download_one_file(request):
	"""
	Descargar un archivo
	"""
	file_path = request.POST['file']
	response = HttpResponse(file(file_path))
	response['Content-Type'] = 'application/force-download'
	response['Content-Length'] = os.path.getsize(file_path)
	response['Content-Disposition'] = 'attachment; filename=\"' + basename(file_path) + '\"'
	response['Accept-Ranges'] = 'bytes'
	return response

@csrf_exempt #This skips csrf validation. Use csrf_protect to have validation
@login_required(login_url="/plot/login/")
def download_multi_file(request):
	"""
	Descargar varios archivos, en un archivo comprimido con fecha en nombre
	"""
	filenames = json.loads(request.POST['files_array'])
	zip_subdir = "daqeq_files-" + (time.strftime("%d-%m-%Y_%H-%M-%S"))
	zip_filename = "%s.zip" % zip_subdir
	s = StringIO.StringIO()
	zf = zipfile.ZipFile(s, "w")

	for fpath in filenames:
		fdir, fname = os.path.split(fpath)
		zip_path = os.path.join(zip_subdir, fname)
		zf.write(fpath, zip_path)

	zf.close()
	response = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
	response['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
	return response

@login_required(login_url="/plot/login/")
def notificationVerification(request):
	"""
	Guardar configuraciones hechas en notification
	"""
	route = settings.BASE_DIR+"/plot"
	os.chdir(route)
	if request.method == "POST":
		if request.POST["this_url"] == "/plot/notification/":
			if "sendFrequency" in request.POST:
				command_server("nss",request.POST["sendFrequency"])
			if "verificationFrequency" in request.POST:
				command_server("nos",request.POST["verificationFrequency"])
			if "username" in request.POST:
				command_server("sis",request.POST["username"])
			if "password" in request.POST:
				command_server("sps",request.POST["password"])
			if "structure" in request.POST:
				command_server("sss",request.POST["structure"])
			if "email" in request.POST:
				command_server("ses",request.POST["email"])
			if "phoneNumber" in request.POST:
				command_server("sts",request.POST["phoneNumber"])
			if "authenticationURL" in request.POST:
				command_server("sas",request.POST["authenticationURL"])
			if "recordURL" in request.POST:
				command_server("srs",request.POST["recordURL"])
			if "structHealthURL" in request.POST:
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
			command_server("1")
			messages.success(request, 'Se han guardado configuraciones las configuraciones.')
			return redirect(view)
		else:
			return request
	return redirect(request.POST["this_url"])


@login_required(login_url="/plot/login/")
def configVerification(request):
	"""
	Guardar configuraciones hechas en config
	"""
	route = settings.BASE_DIR+"/plot"
	os.chdir(route)
	if request.method == "POST":
		if request.POST["this_url"] == "/plot/config/":
			print "It's working?"
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

			if "enableSecondTrigger" in request.POST:
				command_server("enst")
				# if request.POST["secondTriggerThresh"]:
				# 	command_server("nts",request.POST["secondTriggerThresh"])
			else:
				command_server("ensf")
			if "graphWindow" in request.POST:
				command_server("ngs",request.POST["graphWindow"])
			if "filterWindow" in request.POST:
				command_server("nfs",request.POST["filterWindow"])
			if "preEventTime" in request.POST:
				command_server("nas",request.POST["preEventTime"])
			if "postEventTime" in request.POST:
				command_server("nbs",request.POST["postEventTime"])
			if "minTimeRunning" in request.POST:
				command_server("nms",request.POST["minTimeRunning"])
			if "votes" in request.POST:
				command_server("nvs",request.POST["votes"])
			if "recordLength" in request.POST:
				command_server("nrs",request.POST["recordLength"])
			if "portNumber" in request.POST:
				command_server("nps",request.POST["portNumber"])
			if "filenameFormat" in request.POST:
				command_server("sfs",request.POST["filenameFormat"])
			if "serverURL" in request.POST:
				command_server("sus",request.POST["serverURL"])
			if "networkName" in request.POST:
				command_server("sns",request.POST["networkName"])
			if "outputDir" in request.POST:
				command_server("sos",request.POST["outputDir"])
			if "username" in request.POST:
				command_server("sis",request.POST["username"])
			if "password" in request.POST:
				command_server("sps",request.POST["password"])
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

					if request.POST.getlist("secondTriggerX")[i]:
						sensorParams = sensorParams + request.POST.getlist("secondTriggerX")[i].strip(";") + ";"
					if request.POST.getlist("secondTriggerY")[i]:
						sensorParams = sensorParams + request.POST.getlist("secondTriggerY")[i].strip(";") + ";"
					if request.POST.getlist("secondTriggerZ")[i]:
						sensorParams = sensorParams + request.POST.getlist("secondTriggerZ")[i].strip(";") + ";"
					if len(sensorParams.split(";"))==18:
						listSensorParams.append(sensorParams)
			command_server("cas",listSensorParams)
			command_server("1")
			messages.success(request, 'Se han guardado configuraciones las configuraciones.')
			return redirect(view)
		else:
			return request
	return redirect(request.POST["this_url"])

class ConfigurationFormView(FormView):
	"""
	Datos de vista de configuraciones
	"""
	template_name = 'plot/config.html'
	form_class = configForm

	def __init__(self, *args, **kwargs):
		route = settings.BASE_DIR+"/plot"
		os.chdir(route)
		if daqeq_is_running() == False:
			print "is_not_running"
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
			self.initial["username"] = command_server("sig")
			self.initial["password"] = command_server("spg")
			if command_server("eng") == "1":
				self.initial['enableSecondTrigger'] = 'on'
			else:
				self.initial['enableSecondTrigger'] = None
		super(ConfigurationFormView, self).__init__(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(ConfigurationFormView, self).get_context_data(**kwargs)
		context["page_title"] = "Configuración"
		context["this_url"] = "/plot/config/"
		context["action_text"] = ask_daqeq_status()
		command_server("elg")
		context["sensors"] = command_server("cag")
		return context


class NotificationFormView(FormView):
	"""
	Datos de vista de notificaciones
	"""
	template_name = 'plot/notification.html'
	form_class = notifyForm

	def __init__(self, *args, **kwargs):
		route = settings.BASE_DIR+"/plot"
		os.chdir(route)
		if daqeq_is_running() == False:
			print "is_not_running!"
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
