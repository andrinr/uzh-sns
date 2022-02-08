import sys
import numpy as np

class prioq:
    def __init__(self, size):
        self.data = []
        self.values = []
        self.size = size

        for i in range(self.size):
            self.data.append(0)
            self.values.append(sys.float_info.max)

    def getMax(self):
        return self.values[0]

    def replaceHead(self, value, data):
        #print(data)
        self.values[0] = value
        self.data[0] = np.array(data, copy=True)
        self.order()

    def order(self):
        max = 0
        index = -1
        for i in range(self.size):  
            if (self.values[i] > max):
                max = self.values[i]
                index = i

        tmpValue = self.values[0]
        tmpData = np.array(self.data[0], copy=True)
        self.values[0] = self.values[index]
        self.data[0] = self.data[index]
        self.values[index] = tmpValue
        self.data[index] = tmpData

        #print(self.data[0], self.data[index])
