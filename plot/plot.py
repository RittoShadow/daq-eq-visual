"""
Demo of a simple plot with a custom dashed line.

A Line object's ``set_dashes`` method allows you to specify dashes with
a series of on/off lengths (in points).
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from main import *
from sys import *

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


def staticPlot(dataCollection):
    numSensors = (len(dataCollection)-1)/3
    fig1 = plt.figure()
    #Calculate rate of data acquisition. Returns a vector with data per second.
    for i in range(numSensors):
        #4 graphs per sensor. First one shows acceleration in all three axes. Second to fourth represent acceleration in x, y and z axis, respectively.
        b = fig1.add_subplot(numSensors, 1, i+1)
        b.plot(dataCollection[0],dataCollection[i+1], 'r-', linewidth=0.1)
        b.plot(dataCollection[0],dataCollection[i+2], 'g-', linewidth=0.1)
        b.plot(dataCollection[0],dataCollection[i+3], 'b-', linewidth=0.1)
        b.set_xlabel('Time')
        b.set_ylabel('G')
    return fig1


def main(fileName, fig0, fig1):
    #fig, axes = plt.subplots(nrows = 3, ncols = 1, sharex = True, sharey = True)
    dataCollection = parse(fileName)
    numSensors = (len(dataCollection)-1)/3
    print "Number of sensors: "+str(numSensors)
    a = fig0.add_subplot(111)
    a.set_title('Frecuencia de Datos')
    #Calculate rate of data acquisition. Returns a vector with data per second.
    frequency = freq(dataCollection[0])
    stDev = np.std(frequency)
    print "Filesize is: "+str(os.path.getsize(fileName))
    print "Runtime is: "+str(dataCollection[0][-1])+" seconds"
    print "Mean value is: "+str(np.mean(frequency))
    print "Standard Deviation is: "+str(stDev)
    a.plot(range(len(frequency)),frequency, '-', linewidth=0.5)
    for i in range(numSensors):

        #4 graphs per sensor. First one shows acceleration in all three axes. Second to fourth represent acceleration in x, y and z axis, respectively.
        b = fig1.add_subplot(numSensors, 1, i+1)
        b.plot(dataCollection[0],dataCollection[i+1], 'r-', linewidth=0.1)
        b.plot(dataCollection[0],dataCollection[i+2], 'g-', linewidth=0.1)
        b.plot(dataCollection[0],dataCollection[i+3], 'b-', linewidth=0.1)
        b.set_xlabel('tiempo')
        b.set_ylabel('aceleracion')
        # b = fig1.add_subplot(numSensors, 4, 4*i+2)
        # b.plot(dataCollection[0],dataCollection[i+1], 'r-', linewidth=0.1)
        # b = fig1.add_subplot(numSensors, 4, 4*i+3)
        # b.plot(dataCollection[0],dataCollection[i+2], 'g-', linewidth=0.1)
        # b = fig1.add_subplot(numSensors, 4, 4*i+4)
        # b.plot(dataCollection[0],dataCollection[i+3], 'b-', linewidth=0.1)
