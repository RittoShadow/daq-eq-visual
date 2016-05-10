from django.shortcuts import render
from django.http import HttpResponse
from django_socketio.events import *
import matplotlib
matplotlib.use('Agg')
import plot
from matplotlib.backends.backend_agg import FigureCanvasAgg

def index(request):
	return HttpResponse("This is not the greatest page in the world. \nThis is just an index.")
# Create your views here.

def formatData(request):
	if request.method == "POST":
		buff = request.POST["buffer"]
		if buff:
			data = plot.parse(buff) #Suppose there's a stream of data running.
			figure = plot.staticPlot(data)
			canvas = FigureCanvasAgg(figure)
			response = HttpResponse(content_type='image/png')
			canvas.print_png(response)
			return response
			#return render(request, 'plot/index.html',{ "graph" : response})
	else:
		return render(request, 'plot/index.html',{ "graph" : "Nothing to show"})
		
#def subscribe(request):
	
