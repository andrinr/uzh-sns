import sys
import numpy as np

# max heap
class heap:
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
        self.values[0] = value
        self.data[0] = np.array(data, copy=True)
        self.bubbleDown(0)

    def bubbleDown(self, index):
        leftIndex = index * 2 + 1
        rightIndex = index * 2 + 2

        if (leftIndex < self.size):
            childIndex = leftIndex
            if rightIndex < self.size and self.values[leftIndex] < self.values[rightIndex]:
                childIndex = rightIndex

            if (self.values[childIndex] > self.values[index]):
                self.swap(index, childIndex)
                self.bubbleDown(childIndex)
                

    def swap(self, a, b):
        tmpValue = self.values[b]
        tmpData = np.array(self.data[b], copy=True)
        self.values[b] = self.values[a]
        self.data[b] = self.data[a]
        self.values[a] = tmpValue
        self.data[a] = tmpData
