import sys
import numpy as np

# Generel purpose max heap
# Each data intance has a coresponding value
# For the sake of consistency, value could be replaced by lambda function
class Heap:
    def __init__(self, size):
        self.data = []
        self.values = []
        self.size = size

        for i in range(self.size):
            self.data.append(0)
            self.values.append(sys.float_info.max)

    # Get maximum value, in this case at index 0
    def getMax(self):
        return self.values[0]

    # Replace head, meaning delete maximum value and place new value at proper place
    def replaceHead(self, value, data):
        self.values[0] = value
        self.data[0] = np.array(data, copy=True)
        self.bubbleDown(0)

    # O(log n), make sure tree conditions are met
    def bubbleDown(self, index):
        leftIndex = index * 2 + 1
        rightIndex = index * 2 + 2

        # Check weather index has left child
        if (leftIndex < self.size):
            childIndex = leftIndex
            # When right child is bigger than left child, go with right child
            if rightIndex < self.size and self.values[leftIndex] < self.values[rightIndex]:
                childIndex = rightIndex

            # When bigger of the two children is bigger than current, then swap
            if (self.values[childIndex] > self.values[index]):
                self.swap(index, childIndex)
                # And continue bubbling down
                self.bubbleDown(childIndex)
                
    # Swap helper function
    def swap(self, a, b):
        tmpValue = self.values[b]
        tmpData = np.array(self.data[b], copy=True)
        self.values[b] = self.values[a]
        self.data[b] = self.data[a]
        self.values[a] = tmpValue
        self.data[a] = tmpData
