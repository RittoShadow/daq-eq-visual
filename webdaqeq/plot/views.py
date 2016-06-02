# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import FormView
import matplotlib
matplotlib.use('Agg')
import netifaces as net
import plot
import os
import io
import re
from PIL import Image
from matplotlib.backends.backend_agg import FigureCanvasAgg
from models import configForm, notifyForm

daqeq_home = "/home/rba/Downloads/RBA-DAQ_multisensor/"

def home(request):
	return render(request, "plot/home.html", {})

def index(request):
	daqeq_home = "/home/rba/Downloads/RBA-DAQ_multisensor/"
	files = sorted(map(lambda p : daqeq_home+'trunk/enviados/'+str(p), os.listdir(daqeq_home+'trunk/enviados')), key=os.path.getctime)
	files = files + os.listdir(daqeq_home+'trunk/')
	files = filter(lambda p : re.search("[\w_-]+TEST[\w_-]+\.txt",p),files)
	return render(request, "plot/index.html", { "buffer" : files , "page_title" : "Seleccione un archivo:" })
# Create your views here.

def formatData(request):
	if request.method == "POST":
		buff = request.POST["to_plot"]
		if buff:
			data = None
			try:
				data = plot.parse(daqeq_home+"trunk/"+buff) #Suppose there's a stream of data running.
			except IOError:
				data = plot.parse(daqeq_home+"trunk/enviados/"+buff)
			figure = plot.staticPlot(data)
			canvas = FigureCanvasAgg(figure)
			response = HttpResponse(content_type='image/png')
			canvas.print_png(response)
			return render(request, "plot/index.html", { "page_title" : "Visualización" , "plot" : True , "data" : data })
		else:
			files = sorted( map(lambda p : '/home/pi/Desktop/daqeq/trunk/enviados/'+str(p), os.listdir('/home/pi/Desktop/daqeq/trunk/enviados')), key=os.path.getctime)
			return render(request, 'plot/index.html', { "graph" : "Something to show, but no" , "file" : files[-1] })
	else:
		return render(request, 'plot/index.html',{ "graph" : "Nothing to show"})

def subscribe(request):
	ip = net.ifaddresses('eth0')[2][0]['addr']
	return render(request, 'plot/plot.html', { "ip" : ip })

def newPlot(request, data):
	figure = plot.staticPlot(data)
	canvas = FigureCanvasAgg(figure)
	response = HttpResponse(content_type='image/png')
	canvas.print_png(response)
	figure.close()
	return response

def config(request):
	if request.method == "POST":
		return request
	else:
		configData = parseConfigFile(request)
		return render(request, 'plot/config.html', configData)

def parseConfigFile(request):
	return {}

class ConfigurationFormView(FormView):
	template_name = 'plot/notification.html'
	form_class = configForm

	def get_context_data(self, **kwargs):
		context = super(ConfigurationFormView, self).get_context_data(**kwargs)
		self.initial = parseConfigFile(1)
		return context


class NotificationFormView(FormView):
	template_name = 'plot/notification.html'
	form_class = notifyForm
