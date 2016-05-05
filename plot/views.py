from django.shortcuts import render
from django.http import HttpResponse
from django_socketio.events import *
from plot import staticPlot
from matplotlib.backends.backend_agg import FigureCanvasAgg

def index(request):
	return HttpResponse("This is not the greatest page in the world. \nThid is just an index.")
# Create your views here.

def formatData(request):
	data = parse() #Suppose there's a stream of data running.
	figure = staticPlot(data)
	canvas = FigureCanvasAgg(figure)
	response = HttpResponse(content_type='image/png')
	canvas.print_png(response)
	figure.clear()
	return render(request, 'plot/index.html',{ graph : response})

def parse(filePath):
    f = open(filePath,'r')
    n = 0
    epoch = 0
    #Find when data begins
    for line in f:
        match = re.search("%-*DATA-*",line)
        if match:
            #When the data is found, we want to know how many sensors were used
            data = next(f).split(";")
            d = (len(data)-2)/3.0
            if not (d.is_integer()):
                print "Invalid data file"
            else:
                n = int(d)
                epoch = float(data[0])
            break
        else:
            continue
    #Given the number of sensors 'n' we can initialize our variables
    timeStamps = []
    xAxis = [[] for i in range(n)]
    yAxis = [[] for i in range(n)]
    zAxis = [[] for i in range(n)]

    #We proceed from the first data line
    for line in f:
        data = line.split(";")
        if (len(data)-2)/3 == n:
            #Cast from string to float
            data = map((lambda p: float(p)), data[:len(data)-1])
            timeStamps.append(data[0]-epoch)
            for i in range(0, n):
                xAxis[i].append(data[i+1])
                yAxis[i].append(data[i+2])
                zAxis[i].append(data[i+3])
        else:
            print "Invalid data file 2"
            break
    #We need the return, so we craft it using append
    dataCollection = [timeStamps]
    for i in range(0, n):
        dataCollection.append(xAxis[i])
        dataCollection.append(yAxis[i])
        dataCollection.append(zAxis[i])
    return dataCollection
