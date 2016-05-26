from __future__ import unicode_literals

from django.db import models
from django.forms import ModelForm

class Configuration(models.Model):
    graphWindow = models.IntegerField(default=5)
    filterWindow = models.IntegerField(default=10)
    preEventTime = models.IntegerField(default=10)
    postEventTime = models.IntegerField(default=10)
    minTimeRunning = models.IntegerField(default=20)
    votes = models.IntegerField(default=1)
    enableRegistry = models.BooleanField(default=False)
    recordLength = models.IntegerField(default=900)
    filenameFormat = models.CharField(max_length=50)
    enableTrigger = models.BooleanField(default=False)
    serverURL = models.URLField()
    portNumber = models.IntegerField()
    networkName = models.CharField(max_length=50)
    enableAutoStart = models.BooleanField()
    outputDir = models.FilePathField()

    def __save__(self):
        self.save()
        createConfigFile()

class Notification(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    structure = models.CharField(max_length=10)
    email = models.EmailField(max_length=50)
    phoneNumber = models.CharField(max_length=15)
    sendSMS = models.BooleanField()
    sendRecord = models.BooleanField()
    compressRegistry = models.BooleanField()
    authenticationURL = models.CharField(max_length=50)
    recordURL = models.URLField()
    sendStructHealth = models.BooleanField()
    structHealthURL = models.URLField()
    sendFrequency = models.IntegerField()
    verificationFrequency = models.IntegerField()

class configForm(ModelForm):
    class Meta:
        model = Configuration
        fields = ['graphWindow','filterWindow','preEventTime','postEventTime','minTimeRunning','votes','enableRegistry','registryLength','filenameFormat','enableTrigger','serverURL','portNumber','enableAutoStart','outputDir']



class SensorParams(models.Model):
    def __init__(self, serialNum):
        self.dataBuffer = [[],[],[],[]]
        self.index = 0
        self.serialNum = serialNum
        self.axis = None
        self.bufferSize = 5000
        self.windowSize = 1000

    def getIndex(self):
        return self.index

    def addIndex(self):
        self.index = (self.index + 1)%self.bufferSize

    def getSerialNum(self):
        return self.serialNum

    def getSubplot(self):
        return self.axis

    def setSubplot(self, axis):
        self.axis = axis

    def setBufferSize(self, bufferSize):
        self.bufferSize = bufferSize

    def setWindowSize(self, windowSize):
        self.windowSize = windowSize

    def appendToTimestamp(self, ts):
        if len(self.getTimestamp()) < self.bufferSize:
            self.dataBuffer[0].append(ts)
        else:
            self.dataBuffer[0][self.index] = ts

    def appendToXAxis(self, x):
        if len(self.getXAxis()) < self.bufferSize:
            self.dataBuffer[1].append(x)
        else:
            self.dataBuffer[1][self.index] = x

    def appendToYAxis(self, y):
        if len(self.getYAxis()) < self.bufferSize:
            self.dataBuffer[2].append(y)
        else:
            self.dataBuffer[2][self.index] = y

    def appendToZAxis(self, z):
        if len(self.getZAxis()) < self.bufferSize:
            self.dataBuffer[3].append(z)
        else:
            self.dataBuffer[3][self.index] = z

    def appendData(self, ts, x, y, z):
        self.appendToTimestamp(ts)
        self.appendToXAxis(x)
        self.appendToYAxis(y)
        self.appendToZAxis(z)

    def getTimestamp(self):
        return self.dataBuffer[0]

    def getXAxis(self):
        return self.dataBuffer[1]

    def getYAxis(self):
        return self.dataBuffer[2]

    def getZAxis(self):
        return self.dataBuffer[3]

    def getPlotData(self):
        start = self.index
        finish = (start+self.windowSize)%self.bufferSize
        if start > finish:
            xar = self.getTimestamp()[start:] + self.getTimestamp()[:finish]
            yar1 = self.getXAxis()[start:] + self.getXAxis()[:finish]
            yar2 = self.getYAxis()[start:] + self.getYAxis()[:finish]
            yar3 = self.getZAxis()[start:] + self.getZAxis()[:finish]
        else:
            xar = self.getTimestamp()[start:finish]
            yar1 = self.getXAxis()[start:finish]
            yar2 = self.getYAxis()[start:finish]
            yar3 = self.getZAxis()[start:finish]
        thresh = max([max(yar1),max(yar2),max(yar3)])
        return [xar,yar1,yar2,yar3,thresh]

# Create your models here.
