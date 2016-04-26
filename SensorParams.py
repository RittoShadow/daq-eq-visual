class SensorParams:
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
