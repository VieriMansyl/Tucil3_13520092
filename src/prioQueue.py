class prioQueue:
    # construct Priority Queue
    def __init__(self):
        self.heap = []
        self.length = 0
        self.countNode = 0
 
    # head of Priority Queue
    def head(self):
        return self.heap[0]

    def printCost(self):
        print("path with cost")
        for puzzle in self.heap:
            print(puzzle.cost() , end=" ")
        print()

    # enqueue
    def enqueue(self, val):
        if self.isEmpty():
            self.heap.append(val)
            self.length += 1
        else:
            i = 0
            while i < self.length:
                if(self.heap[i].cost() > val.cost()):
                    break
                else:
                    i += 1
            self.heap.insert(i , val)
            self.length += 1
        self.countNode += 1
 
    # dequeue
    def dequeue(self):
        head = self.heap.pop(0)
        self.length -= 1
        return head

    # if the Queue is empty
    def isEmpty(self):
        return self.length == 0