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

daqeq_home = "/home/rba/Downloads/RBA-DAQ_multisensor/"

def home(request):
	return render(request, "plot/home.html", {})

def index(request):
	daqeq_home = "/home/rba/Downloads/RBA-DAQ_multisensor/"
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

def configVerification(request):
	route = settings.BASE_DIR+"/plot"
	os.chdir(route)
	if request.method == "POST":
		if request.POST["this_url"] == "/plot/config/":
			if "enableAutoStart" in request.POST:
				os.popen("sudo python command_client.py ast")
			else:
				os.popen("sudo python command_client.py asf")
			os.popen("sudo python command_client.py 0")
		elif request.POST["this_url"] == "/plot/notification/":
			print "yay"
		else:
			return request
	return redirect(request.POST["this_url"])


class ConfigurationFormView(FormView):
	template_name = 'plot/notification.html'
	form_class = configForm

	def __init__(self, *args, **kwargs):
		route = settings.BASE_DIR+"/plot"
		os.chdir(route)
		a = os.popen("sudo python command_client.py ag").read().strip()
		if a == "1":
			self.initial['enableAutoStart'] = 'on'
		else:
			self.initial['enableAutoStart'] = None
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
