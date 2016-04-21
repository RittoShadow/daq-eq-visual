#!/usr/bin/env python

"""Copyright 2010 Phidgets Inc.
This work is licensed under the Creative Commons Attribution 2.5 Canada License.
To view a copy of this license, visit http://creativecommons.org/licenses/by/2.5/ca/
"""

__author__ = 'Adam Stelmack'
__version__ = '2.1.8'
__date__ = 'May 17 2010'

#Basic imports
from ctypes import *
import sys
import Tkinter as tk
import numpy as np
#Phidget specific imports
from Phidgets.Phidget import Phidget
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import SpatialDataEventArgs, AttachEventArgs, DetachEventArgs, ErrorEventArgs
from Phidgets.Devices.Spatial import Spatial, SpatialEventData, TimeSpan
from Phidgets.Phidget import PhidgetLogLevel
from threading import Condition
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

dataBuffer = [[],[],[],[]]
subBuffer = [[],[],[],[]]
bufferSize = 5000
windowSize = 2500
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
mutex = Condition()
i = 0
j = windowSize

#Create an accelerometer object
try:
    spatial = Spatial()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

def transferToBuffer(buff, sub):
    for i in range (len(buff)):
        buff[i] = buff[i] + sub[i]
        buff[i] = buff[i][len(sub[i]):]

def animate(e):
    global dataBuffer, subBuffer, writing, i, j
    if len(dataBuffer[0]) < windowSize:
        return
    #mutex.acquire()
    # while len(dataBuffer[0]) < bufferSize or len(subBuffer[0]) < windowSize:
    #     mutex.wait()
    # transferToBuffer(dataBuffer,subBuffer)
    # subBuffer = [[],[],[],[]]
    start = i
    finish = (i+windowSize)%bufferSize
    xar = dataBuffer[0][start:finish]
    yar1 = dataBuffer[1][start:finish]
    yar2 = dataBuffer[2][start:finish]
    yar3 = dataBuffer[3][start:finish]
    if start > finish:
        xar = dataBuffer[0][start:] + dataBuffer[0][:finish]
        yar1 = dataBuffer[1][start:] + dataBuffer[1][:finish]
        yar2 = dataBuffer[2][start:] + dataBuffer[2][:finish]
        yar3 = dataBuffer[3][start:] + dataBuffer[3][:finish]
        thresh = max([max(yar1),max(yar2),max(yar3)])
        ax1.clear()
        plt.xlim([min(xar),max(xar)])
        plt.ylim([-thresh,thresh])
        ax1.plot(xar,yar1,'-',linewidth=0.3)
        ax1.plot(xar,yar2,'r-',linewidth=0.3)
        ax1.plot(xar,yar3,'g-',linewidth=0.3)
    else:
        xar = dataBuffer[0][start:finish]
        yar1 = dataBuffer[1][start:finish]
        yar2 = dataBuffer[2][start:finish]
        yar3 = dataBuffer[3][start:finish]
        thresh = max([max(yar1),max(yar2),max(yar3)])
        ax1.clear()
        plt.xlim([min(xar),max(xar)])
        plt.ylim([-thresh,thresh])
        ax1.plot(xar,yar1,'-',linewidth=0.3)
        ax1.plot(xar,yar2,'r-',linewidth=0.3)
        ax1.plot(xar,yar3,'g-',linewidth=0.3)
    #mutex.notify()
    #mutex.release()

#Information Display Function
def DisplayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (spatial.isAttached(), spatial.getDeviceName(), spatial.getSerialNum(), spatial.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of Acceleration Axes: %i" % (spatial.getAccelerationAxisCount()))
    print("Number of Gyro Axes: %i" % (spatial.getGyroAxisCount()))
    print("Number of Compass Axes: %i" % (spatial.getCompassAxisCount()))

#Event Handler Callback Functions
def SpatialAttached(e):
    attached = e.device
    print("Spatial %i Attached!" % (attached.getSerialNum()))

def SpatialDetached(e):
    detached = e.device
    print("Spatial %i Detached!" % (detached.getSerialNum()))

def SpatialError(e):
    try:
        source = e.device
        print("Spatial %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

def SpatialData(e):
    global dataBuffer, subBuffer, writing, i, j
    source = e.device
    #print("Spatial %i: Amount of data %i" % (source.getSerialNum(), len(e.spatialData)))
    for index, spatialData in enumerate(e.spatialData):
        #print("=== Data Set: %i ===" % (index))
        if len(spatialData.Acceleration) > 0:
            #print("Acceleration> x: %6f  y: %6f  z: %6f" % (spatialData.Acceleration[0], spatialData.Acceleration[1], spatialData.Acceleration[2]))
            x = spatialData.Acceleration[0]
            y = spatialData.Acceleration[1]
            z = spatialData.Acceleration[2]
            ts = spatialData.Timestamp.seconds + (spatialData.Timestamp.microSeconds)/1000000.0
            # if len(dataBuffer[0]) == bufferSize:
            #     #mutex.acquire()
            #     subBuffer[0].insert(i,ts)
            #     subBuffer[1].insert(i,x)
            #     subBuffer[2].insert(y)
            #     subBuffer[3].append(z)
            #     #mutex.notify()
            #     #mutex.release()
            # else:
            if len(dataBuffer[0]) < bufferSize:
                dataBuffer[0].append(ts)
                dataBuffer[1].append(x)
                dataBuffer[2].append(y)
                dataBuffer[3].append(z)
            else:
                dataBuffer[0][i] = ts
                dataBuffer[1][i] = x
                dataBuffer[2][i] = y
                dataBuffer[3][i] = z
                i = (i+1)%bufferSize



    #print("------------------------------------------")

#Main Program Code
try:
	#logging example, uncomment to generate a log file
    #spatial.enableLogging(PhidgetLogLevel.PHIDGET_LOG_VERBOSE, "phidgetlog.log")

    spatial.setOnAttachHandler(SpatialAttached)
    spatial.setOnDetachHandler(SpatialDetached)
    spatial.setOnErrorhandler(SpatialError)
    spatial.setOnSpatialDataHandler(SpatialData)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
    spatial.openPhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    spatial.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        spatial.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)
else:
    spatial.setDataRate(1)
    DisplayDeviceInfo()

print("Press Enter to quit....")

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()

while True:
    chr = sys.stdin.read(1)
    if chr != None:
        break


print("Closing...")

try:
    spatial.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
exit(0)
