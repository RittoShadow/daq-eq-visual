"""
Demo of a simple plot with a custom dashed line.

A Line object's ``set_dashes`` method allows you to specify dashes with
a series of on/off lengths (in points).
"""
import numpy as np
import matplotlib.pyplot as plt
import os
from main import *

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
