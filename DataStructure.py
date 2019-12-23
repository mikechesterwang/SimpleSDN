from heapq import *

class Stack(object):
    def __init__(self):
        self.list = []
        self.ptr = 0
        self._s = set()

    def isEmpty(self):
        return self.ptr == 0

    def push(self, obj):
        self._s.add(obj)
        self.list[self.ptr] = obj
        self.ptr += 1

    def pop(self):
        rtn = self.list[self.ptr - 1]
        self.ptr -= 1
        self._s.remove(rtn)
        return rtn

    def peek(self):
        return self.list[self.ptr - 1]

    def contains(self, obj):
        return obj in self._s

class Queue(object):
    def __init__(self):
        self.list = []
    
    def isEmpty(self):
        return len(self.list) == 0
    
    def enQueue(self, obj):
        self.list.append(obj)

    def deQueue(self):
        rtn = self.list[0]
        del self.list[0]
        return rtn

class PriorityQueue(object):
    def __init__(self):
        self.pq = []
        self.set = set()
        self.hash_id = 0
    
    def enQueue(self, obj, priority):
        self.set.add(obj)
        heappush(self.pq, [priority, self.hash_id, obj])
        self.hash_id += 1

    def deQueue(self):
        rtn = heappop(self.pq)[2]
        self.set.remove(rtn)
        return rtn

    def isEmpty(self):
        return len(self.pq) == 0

    def contains(self, obj):
        return obj in self.set

class Heap(object):
    def __init__(self):
        self.array = []
        self.heapIndex = {}
        self.value = {}
        self.empty = 1
        self.len = 0
        self._s = set()
        self.array.append(None)

    def swapValue(self, i, j):
        tmp = self.array[i]
        self.array[i] = self.array[j]
        self.array[j] = tmp
        self.heapIndex[self.array[i]] = i
        self.heapIndex[self.array[j]] = j

    def isEmpty(self):
        return self.len == 0
    
    def downAdjust(self):
        i = 1
        while 2 * i <= self.len:
            smaller = 0
            if 2 * i + 1 <= self.len: # right child exists
                smaller = 2 * i if self.value[self.array[2 * i]] < self.value[self.array[2 * i + 1]] else 2 * i + 1
            else: # only left child exists
                smaller = 2 * i
            #
            if self.value[self.array[i]] > self.value[self.array[smaller]] :
                self.swapValue(i, smaller)
                i = smaller
            else:
                break

    def upAdjust(self, index):
        i = index
        while i > 1:
            if self.value[self.array[i]] < self.value[self.array[i//2]]:
                self.swapValue(i, i//2)
                i //= 2
            else:
                break
    
    def add(self, obj, priority):
        if obj in self._s:
            raise KeyError("{} is already in the heap.".format(str(obj)))
        self._s.add(obj)
        self.array.append(obj)
        self.value[obj] = priority
        self.upAdjust(self.empty)
        self.heapIndex[self.array[self.empty]] = self.empty
        self.empty += 1
        self.len += 1

    def poll(self):
        rtn = self.array[1]
        self._s.remove(rtn)
        self.swapValue(1, self.len)
        del self.array[self.len]
        self.empty -= 1
        self.len -= 1
        if self.len != 0:
            self.downAdjust()
        return rtn
    
    def ascent(self, obj, newPriority):
        self.value[obj] = newPriority
        if not obj in self._s:
            raise KeyError("{} is not in the heap.".format(str(obj)))
        heapIndex = self.heapIndex[obj]
        self.upAdjust(heapIndex)

    def contains(self, obj):
        return obj in self._s

    def __str__(self):
        rtn = ""
        for i in range(1, len(self.array)):
            rtn += str(self.array[i]) + " "

        return rtn


