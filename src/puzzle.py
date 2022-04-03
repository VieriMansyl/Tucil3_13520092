import copy

class fifteenpuzzle:

    # construct puzzle
    '''
    mat     : matrix of 15-puzzle
    x , y   : 'null' slot position
    path    : path from 'root' matrix up to current matrix
    '''
    def __init__(self , mat , x , y , path):
        self.matrix = copy.deepcopy(mat)
        self.emptyslot = [x,y]
        self.kurang = self.sumOfKurang()
        self.xValue = self.valueOfX()
        self.path = copy.deepcopy(path)

    def __lt__(self, next):
        return self.cost() < next.cost()

    # change to Array
    def toArray(self):
        return [elmt for elmts in self.matrix for elmt in elmts]

    # SOLVABILITY
    # sum of Kurang(i)
    def sumOfKurang(self):
        count = 0
        arr = self.toArray()
        for i in range(16):
            pointer = arr[i]
            for idx in range(i , 16):
                if (pointer > arr[idx]):
                    count += 1
        return count

    # value of X
    def valueOfX(self):
        row , col = self.emptyslot[0] , self.emptyslot[1]
        return 1 if ((row % 2 == 0 and col %2 == 1) or (row % 2 == 1 and col %2 == 0)) else 0

    def solvable(self):
        total = self.sumOfKurang() + self.valueOfX()
        return total % 2 == 0


    # MOVEMENT
    def illegalMove(self , movement):
        lastIdx = len(self.path)-1
        if(lastIdx >= 0):
            diff = abs(self.path[lastIdx] - movement)
            if (diff == 2):
                return True
        else :
            return False


    def move(self , newX , newY):
        x , y = self.emptyslot[0] , self.emptyslot[1]
        self.emptyslot[0] += newX
        self.emptyslot[1] += newY
        self.matrix[x][y] , self.matrix[self.emptyslot[0]][self.emptyslot[1]] = self.matrix[self.emptyslot[0]][self.emptyslot[1]] , self.matrix[x][y]
        self.kurang = self.sumOfKurang()
        self.xValue = self.valueOfX()

    # DISPLAY INFO
    def displayMat(self):
        print("+ -- -- -- -- +")
        for i in range(4):
            print("| ", end="")
            for j in range(4):
                if(self.matrix[i][j] == 16) : print("**",end="")
                else : 
                    if(self.matrix[i][j] < 10):
                        print("0" + str(self.matrix[i][j]),end="")
                    else :
                        print(self.matrix[i][j],end="")
                if(j != 3) : print(" ", end= "")
            print(" |")
        print("+ -- -- -- -- +")

    # Display all Info
    def printInfo(self):
        print(f"empty Position: {self.emptyslot}")
        print(f"Path          : ", end="")
        if(len(self.path) == 0):
            print("None", end="")
        else:
            for i in range (len(self.path)):
                if(self.path[i] == 0):
                    print("bottom", end="")
                elif(self.path[i] == 1):
                    print("left", end="")
                elif(self.path[i] == 2):
                    print("top", end="")
                elif(self.path[i] == 3):
                    print("right", end="")

                if(i+1 != len(self.path)):
                    print(" -> ",end="")
        print()
        self.displayMat()
        print("============================================")
        print("  i      | Kurang(i)")
        print("============================================")
        self.kurangI()
        print("============================================")
        print()
        print(f"sum of Kurang : {self.kurang}")
        print(f"value of X    : {self.xValue}")
        print("--------------------------  +")
        print(f"cost          : {self.xValue + self.kurang}")

    # show Kurang(i)
    def kurangI(self):
        arr = self.toArray()
        lessValue = [0 for i in range(16)]
        for i in range(16):
            count = 0
            for idx in range(i , 16):
                if (arr[i] > arr[idx]):
                    count += 1
            lessValue[arr[i]-1] = count

        for i in range(len(lessValue)):
            if(i < 9):
                print(f"  i = {i+1}  | Kurang({i+1})  = {lessValue[i]}")
            else:
                print(f"  i = {i+1} | Kurang({i+1}) = {lessValue[i]}")

    # COUNT COST
    # puzzle's goal
    goal = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]

    # count g(p)
    def calculateGoal(self):
        count = 0
        for i in range(4):
            for j in range(4):
                if(self.matrix[i][j] != 16):
                    if self.matrix[i][j] != fifteenpuzzle.goal[i][j]:
                        count += 1
        return count
    
    def cost(self):
        return len(self.path) + self.calculateGoal()
