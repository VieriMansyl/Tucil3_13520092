#15 Puzzle Game menggunakan algoritma Branch and Bound
from random import shuffle
from puzzle import fifteenpuzzle
from prioQueue import prioQueue
import copy
import time

# movement value : bottom, left, top, right
moveRow = [ 1, 0, -1, 0 ]
moveCol = [ 0, -1, 0, 1 ]

# membaca file .txt
# mengembalikan array berisikan nilai dari matriks yang terbaca

def readFile(filename):
    arr = []
    with open(filename,'r') as f:
        lines=f.read().splitlines()
        for line in lines:
            words = line.split(" ")
            for word in words:
                arr.append(word)
    
    for i in range(len(arr)):
        try:
            arr[i] = int(arr[i])
        except ValueError:
            arr[i] = 16
    return arr


def toMatrix(arr):
    return [arr[i:i+4] for i in range(0,len(arr), 4)]


def find16(mat):
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if(mat[i][j] == 16):
                return i , j


def isSafe(x, y):
	return (x >= 0 and x < 4) and (y >= 0 and y < 4)


def movement(i):
    print("Movement      : ", end="")
    if(i == 0):
        print("Down")
    elif(i == 1):
        print("Left")
    elif(i == 2):
        print("Up")
    elif(i == 3):
        print("Right")


def childNode(parent , direction):
    prev = copy.deepcopy(parent)
    prevRow = prev.emptyslot[0]
    prevCol = prev.emptyslot[1]
    prevPath = prev.path
    
    # create child node
    row = prevRow + moveRow[direction]
    col = prevCol + moveCol[direction]
    path = prevPath + [direction]
    prev.matrix[prevRow][prevCol] , prev.matrix[row][col] = prev.matrix[row][col] , prev.matrix[prevRow][prevCol]

    child = fifteenpuzzle(prev.matrix , row , col , path)
    return child


def solve(puzzle) -> fifteenpuzzle:             # implement Branch and Bound Algorithm
    pq = prioQueue()
    pq.enqueue(puzzle)
    currentNode = puzzle
    while not pq.isEmpty():                     # there's child node left to be checked
        currentNode = pq.dequeue()
        if currentNode.calculateGoal() == 0:    # reach goal
            return currentNode , pq.countNode
        else:                                   # have not reach goal
            for i in range(4):
                newNullPositon = [currentNode.emptyslot[0] + moveRow[i] , currentNode.emptyslot[1] + moveCol[i]]
                check = currentNode.illegalMove(i)
                if isSafe(newNullPositon[0], newNullPositon[1]) and not check:
                    child = childNode(currentNode , i)
                    if(child.solvable()):       # if child node is solvable -> ∑KURANG(i) + X is even
                        pq.enqueue(child)
    return currentNode , pq.countNode

# INTERFACE TERMINAL
def welcome():
    print("============================================")
    print("|           ~ 15 PUZZLE SOLVER ~           |")
    print("============================================")
    print("|              by VIERI MANSYL             |")
    print("============================================")

def choose():
    print("| INPUT PUZZLE OPTION :                    |")
    print("============================================")
    print("| 1. Load File                             |")
    print("| 2. Read input                            |")
    print("| 3. Random Value                          |")
    print("============================================")
    print("  Choose , either 1 , 2 , or 3")
    print("============================================")

def process(puz):
    print("\n")
    print("============================================")
    print("  PUZZLE :")
    print("============================================")
    print()
    puz.printInfo()
    print("============================================")
    print("  SOLUTION :")

def failed():
    print("  It's Unsolvable !!!")
    print("============================================")

def success():
    print("  We found the path !!!")
    print("============================================")


#ALGORITMA UTAMA
# "Opening" Interface
welcome()
choose()

# INPUT
option = input("COMMAND : ")
if(option == "1"):                                              # LOAD FILE
    filepath = input("Input file name : ")
    arr = readFile(filepath)
    mat = toMatrix(arr)
elif(option == "2"):                                            # READ INPUT
    print(" P.S. : to input empty slot, use '16'")
    mat = [[0 for col in range(4)] for row in range(4)]
    for i in range(4):
        for j in range(4):
            puzzleVal = int(input(f"[{i+1}][{j+1}] value : "))
            mat[i][j] = puzzleVal
else :                                                          # RANDOM VALUE
    arr = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    shuffle(arr)
    mat = toMatrix(arr)
    

# CREATE PUZZLE
i , j = find16(mat)
puzzle = fifteenpuzzle(mat, i , j , [])

#"Process" Interface
process(puzzle)

# SOLVE
start = time.time()
answer , nodes= solve(puzzle)
end = time.time()

answerPath = copy.deepcopy(answer.path)
if(answer.cost() > 0):      # FAILED
    failed()
else:                       # SUCCESS
    success()

# OUTPUT
# first puzzle
print("puzzle :")
print(f"sum of Kurang : {puzzle.kurang}")
print(f"value of X    : {puzzle.xValue}")
puzzle.displayMat()
print()

# each movement's path
for path in answerPath:
    movement(path)
    puzzle.move(moveRow[path] , moveCol[path])
    print(f"sum of Kurang : {puzzle.kurang}")
    print(f"value of X    : {puzzle.xValue}")
    puzzle.displayMat()
    print()

print("============================================")
print(f" COST                         : {answer.cost()}")
print(f" TOTAL PATH(S)                : {len(answerPath)}")
print(f" DURATION                     : {round(end - start , 8) * 1000} millisecond(s)")
print(f" TOTAL NODE YANG DIBANGKITKAN : {nodes}")
print("============================================")
close = input("<<Type anything to close program>>")