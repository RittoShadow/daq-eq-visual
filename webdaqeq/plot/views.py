# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import FormView
from django.conf import settings

import matplotlib
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
			files = sorted( map(lambda p : '/home/pi/Desktop/daqeq/trunk/enviados/'+str(p), os.listdir('/home/pi/Desktop/daqeq/trunk/enviados')), key=os.path.getctime)
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
	    # Enviar signal SIG_USR1 a app en c++, para iniciar/detener adquirir datos
		os.kill(int(pid), signal.SIGUSR1) # Unix version only...
	if request.POST["this_url"]:
		return redirect(request.POST["this_url"])

def ask_daqeq_status():
	import os

	# Obtener PID del proceso de app en c++ de daq-eq
	route = settings.BASE_DIR+"/plot"
	os.chdir(route)
	result = int(os.popen("sudo python ask_daqeq_status.py").read())
	if result == 0:
		return "Reiniciar"
	elif result == 1:
		return "Detener"
	else:
		return "Error"

def view(request):
	return render(request, 'plot/views.html', {})

def sensor(request):
	return render(request, 'plot/sensors.html', {})

def configVerification(request):
	route = settings.BASE_DIR+"/plot"
	os.chdir(route)
	if request.method == "POST":
		if request.POST["this_url"] == "/plot/config/":
			if "enableAutoStart" in request.POST:
				command_server("east")
			else:
				command_server("easf")
			if "enableTrigger" in request.POST:
				command_server("etst")
			else:
				command_server("etsf")
			if "enableRecording" in request.POST:
				os.popen("sudo python command_client.py erst")
			else:
				os.popen("sudo python command_client.py ersf")
			if request.POST["graphWindow"]:
				command_server("ngs",int(request.POST["graphWindow"]))
			if request.POST["filterWindow"]:
				command_server("nfs",int(request.POST["filterWindow"]))
			if request.POST["preEventTime"]:
				command_server("nas",int(request.POST["preEventTime"]))
			if request.POST["postEventTime"]:
				command_server("nbs",int(request.POST["postEventTime"]))
			if request.POST["minTimeRunning"]:
				command_server("nms",int(request.POST["minTimeRunning"]))
			if request.POST["votes"]:
				command_server("nvs",int(request.POST["votes"]))
			if request.POST["recordLength"]:
				command_server("nrs",int(request.POST["recordLength"]))
			if request.POST["portNumber"]:
				command_server("nps",int(request.POST["portNumber"]))
			command_server("0")
		elif request.POST["this_url"] == "/plot/notification/":
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
		if command_server("erg") == "1":
			self.initial['enableRecording'] = 'on'
		self.initial['graphWindow'] = command_server("ngg")
		self.initial['filterWindow'] = command_server("nfg")
		self.initial['preEventTime'] = command_server("nag")
		self.initial['postEventTime'] = command_server("nbg")
		self.initial['minTimeRunning'] = command_server("nmg")
		self.initial['votes'] = command_server("nvg")
		self.initial['recordLength'] = command_server("nrg")
		self.initial['portNumber'] = command_server("npg")
		super(ConfigurationFormView, self).__init__(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(ConfigurationFormView, self).get_context_data(**kwargs)
		context["page_title"] = "Configuración"
		context["this_url"] = "/plot/config/"
		context["action_text"] = ask_daqeq_status()
		return context


class NotificationFormView(FormView):
	template_name = 'plot/notification.html'
	form_class = notifyForm

	def get_context_data(self, **kwargs):
		context = super(NotificationFormView, self).get_context_data(**kwargs)
		context["page_title"] = "Notificaciones"
		context["this_url"] = "/plot/notification/"
		context["action_text"] = ask_daqeq_status()
		return context
