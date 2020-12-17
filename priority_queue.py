import heapq # min-heap by default

class PriorityQueue:
    def  __init__(self):
        self.Heap = []
        self.Count = 0

    def push(self, item, priority):
        entry = (priority, self.Count, item)
        heapq.heappush(self.Heap, entry)
        self.Count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.Heap) # heapq is a minheap so node with lowest priority/(heutistic+cost) will be popped first
        return item

    def get_last(self):
        (_, _, item) = self.Heap[0]
        return item
