# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import django.forms as forms
from django.forms import ModelForm
from django.core.validators import *
from django.utils.translation import ugettext_lazy as _

class Configuration(models.Model):
    graphWindow = models.IntegerField(default=5, validators=MinValueValidator(5))
    filterWindow = models.IntegerField(default=10, validators=MinValueValidator(10))
    preEventTime = models.IntegerField(default=10, validators=MinValueValidator(10))
    postEventTime = models.IntegerField(default=10, validators=MinValueValidator(10))
    minTimeRunning = models.IntegerField(default=20, validators=MinValueValidator(20))
    votes = models.IntegerField(default=1)
    enableRecording = models.BooleanField(default=False)
    recordLength = models.IntegerField(default=900, validators=MinValueValidator(100))
    filenameFormat = models.CharField(default="E-TEST-yyyyMMdd_hhmmss",max_length=50)
    enableTrigger = models.BooleanField(default=False)
    serverURL = models.CharField(default="http://www.shmrba.com", max_length=50)
    portNumber = models.IntegerField(default=7624,validators=MinValueValidator(0))
    networkName = models.CharField(default="Red0",max_length=50)
    enableAutoStart = models.BooleanField(default=False)
    outputDir = models.CharField(default="/home/",max_length=50)
    allowClient = models.BooleanField(default=False)
    username = models.CharField(max_length=20,blank=True)
    password = models.CharField(max_length=20,blank=True)

class Notification(models.Model):
    username = models.CharField(max_length=20,blank=True)
    password = models.CharField(max_length=20,blank=True)
    structure = models.CharField(max_length=10)
    email = models.EmailField(max_length=50, blank=True)
    phoneNumber = models.CharField(max_length=15,blank=True)
    sendSMS = models.BooleanField(default=False)
    sendRecord = models.BooleanField(default=False)
    compressRecord = models.BooleanField(default=False)
    authenticationURL = models.CharField(max_length=50,blank=True)
    recordURL = models.URLField(blank=True)
    sendStructHealth = models.BooleanField(default=False)
    structHealthURL = models.URLField(blank=True)
    sendFrequency = models.IntegerField(validators=MinValueValidator(1))
    verificationFrequency = models.IntegerField(validators=MinValueValidator(1))

class configForm(ModelForm):
    class Meta:
        model = Configuration
        fields = '__all__'
        labels = {
            'graphWindow': _('Ventana de gráfico:'),
            'filterWindow': _('Ventana de filtro:'),
            'preEventTime': _('Pre-evento:'),
            'postEventTime': _('Post-evento:'),
            'minTimeRunning': _('Minimum Time Running:'),
            'votes': _('Votos'),
            'enableRecording': _('Habilitar registro continuo'),
            'recordLength': _('Duración registro'),
            'filenameFormat': _('Formato nombre de archivo'),
            'enableTrigger': _('Habilitar Trigger Externo'),
            'serverURL': _('URL de Server:'),
            'portNumber': _('Puerto:'),
            'networkName': _('Nombre de Red:'),
            'enableAutoStart': _('Habilitar inicio automático'),
            'outputDir': _('Ruta destino:'),
            'allowClient': _('Permitir configuración de cliente'),
            'username': _('Usuario:'),
            'password': _('Password:'),
        }

class notifyForm(ModelForm):
    class Meta:
        model = Notification
        fields = '__all__'
        labels = {
            'username': _('Nombre de usuario:'),
            'password': _('Contraseña:'),
            'structure': _('Estructura:'),
            'email': _('Correo electrónico:'),
            'phoneNumber': _('Número de teléfono:'),
            'sendSMS': _('Enviar SMS'),
            'sendRecord': _('Habilitar envío de registros de evento'),
            'compressRecord': _('Enviar registro comprimido'),
            'authenticationURL': _('URL Autenticación:'),
            'recordURL': _('URL Envio de Registros:'),
            'sendStructHealth': _('Habilitar envío de registros de salud'),
            'structHealthURL': _('URL envío de estados de salud'),
            'sendFrequency': _('Frecuencia de envío de estado de salud:'),
            'verificationFrequency': _('Frecuencia de verificación de estado de salud:'),
        }

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
