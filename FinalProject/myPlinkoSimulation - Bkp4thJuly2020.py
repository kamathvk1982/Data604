#importing the module
import time
import math
import random

#welcoming the user
name = input("What is your name? ")
print("Hello, " + name, "Time to play Plinko!")
print("\n\n\n")

#wait for 1 second
time.sleep(1)

#get inputs from user
cntBins = int(input("Number of Buckets(4 or 5)? "))
print("\n\n")

#calculate the matrix for draring the game board
myMatrixCols = cntBins + 1
myMatrixRows = (cntBins * 2) +1

#Draw the game board
print("\t\t    ", end="")
for i in range(cntBins):
        print(i+1,"", sep="      ", end="")
print()
for i in range(myMatrixRows):
    if (i % 2) == 0:
        print("\t\t|","*      " * (myMatrixCols-1),"* |", sep="")
    else:
        print("\t\t|", "   *   " * (myMatrixCols-1),"  |", sep="")

#get value for the buckets
mid =  math.ceil(cntBins/2)
valBucket = []
cntBucket = []
print("\t\t  ", end="")
for i in range(1, mid+1):
    valBucket.append(pow(10, i))
    cntBucket.append(0)
    print("   $", pow(10, i), sep="",  end="")
if (mid % 2) == 0:
    mid += 1
for i in range(mid, 1, -1):
        valBucket.append(pow(10, i-1))
        cntBucket.append(0)
        print("   $", pow(10, i-1), sep="",  end="")


#get inputs from user
print("\n\n")
cntSimulation = int(input("Number of Simulations(10 to 1000)? "))
intLane = int(input("Enter Drop Lane(Less then equal to buckets)? "))
print("\n\n")
    
#get random path    
#n character binary number
directionList=['L','R']
minWall = 0.5
maxWall = cntBins + 0.5

for i in range(0, cntSimulation):
    recordList = []
    direction =[]
    scoreWall = intLane
    for j in range(0, myMatrixRows-1):
        direction = directionList[random.randint(0,1)]
        if direction == 'L':
            scoreWall -= 0.5
        else:
            scoreWall += 0.5

        #print('calc:', direction, scoreWall)
        if scoreWall < minWall:
            scoreWall = minWall
            direction = 'R'
            
        if scoreWall > maxWall:
            scoreWall = maxWall
            direction = 'L'
            
        #print('done:', direction, scoreWall) 
        recordList.append(direction)
    #print(str(recordList), " : ", scoreWall, "$ ", valBucket[int(scoreWall)-1])
    cntBucket[int(scoreWall)-1] += 1

print("Bucket Wise Count:")
for i in range(cntBins):
        print("$ {:<10} : {:<10}".format( valBucket[i] , cntBucket[i]))

print("\n\n")
print("Good bye, " + name, " Come Back Again!")
print("\n\n")
