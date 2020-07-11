#Student Name: Vinayak Kamath
#Class: Data 604 - Final Project - "Plinko" Game Simulation
#Date: 4th July 2020

#importing the modules/libraries
import time
import math
import random
from modsim import *
import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np

# set the random number generator
np.random.seed(7)

#Defining System Object with required variables defined 
system = System(inp_BoardDimension="BOARD_DIMENSION", 
                inp_CountOfSimulation="COUNT_OF_SIMULATION",
                inp_Hello="HELLO",
                inp_GoodBye="GOODBYE",
                myMatrixCols =0,
                myMatrixRows =0,
                minWall = 0.5,
                maxWall = 0,
                directionList=['L','R']
                )

#Function make_state()
def make_state():
        """Creates a `State` object with the the state variables
        to hold name, count of buckets, count of simulations,
        and other required variables.

        returns: a State object.
        """
        return State(name="", cntBins=0, cntSimulation=0
                     , intLane=0, valBucket = [], cntBucket = []
                     , pathDirectionList = []
                     , pathScoreList = []
                     )  #returns a State object

#Function greet_user()
def greet_user(system, state, inp_type ):
        """Function call to welcome user or wishing good bye to user
        and capture his/her name.
        
        system: System object
        state: State object
        inp_type: to determine if the call is Hello or GoodBye.
                  
        returns: a dummy numeric value of 1
        """
        if inp_type == system.inp_Hello:
                #welcoming the user
                state.name = input("What is your name? ")
                print("Hello " + state.name, ", Time to play Plinko!")
                print("\n\n")

        if inp_type == system.inp_GoodBye:
                #Good Bye 
                print("Good bye " + state.name, ", Come back again!")
                print("\n\n")

        #wait for 1 second
        time.sleep(1)
        return 1

#Function get_input()        
def get_input(system, state, inp_type):
        """Function call to get inputs from the user. 

        system: System object
        state: State object
        inp_type: to determine if the call is for getting board dimension
                  or count of simulation.

        returns: a dummy numeric value of 1
        """
        #get inputs from user
        if inp_type == system.inp_BoardDimension:
                state.cntBins = int(input("Number of Buckets(4 or 5)? "))
                state.intLane = int(input("Enter Drop Lane(Less then equal to buckets)? "))
        elif inp_type == system.inp_CountOfSimulation:
                state.cntSimulation = int(input("Number of Simulations(10 to 1000)? "))
        print("\n\n")
        return 1

#Function draw_board()  
def draw_board(system, state):
        """Function call to draw the Plinko Board based on the
        number of  buckets input by user.
        
        Also calculates Dollar value of each bucket.

        system: System object
        state: State object

        returns: a dummy numeric value of 1
        """
        #calculate the matrix for draring the game board
        system.myMatrixCols = state.cntBins + 1
        system.myMatrixRows = (state.cntBins * 2) +1
        system.maxWall = state.cntBins + 0.5

        #Draw the game board:
        print("\t\t    ", end="")
        for i in range(state.cntBins):
                print(i+1,"", sep="      ", end="")
        print()
        for i in range(system.myMatrixRows):
                if (i % 2) == 0:
                        print("\t\t|","*      " * (system.myMatrixCols-1),"* |", sep="")
                else:
                        print("\t\t|", "   *   " * (system.myMatrixCols-1),"  |", sep="")

        #get value for the buckets
        mid =  math.ceil(state.cntBins/2)
        print("\t\t  ", end="")
        for i in range(1, mid+1):
                state.valBucket.append(pow(10, i))
                state.cntBucket.append(0)
                print("   $", pow(10, i), sep="",  end="")
        if (mid % 2) == 0:
                mid += 1
        for i in range(mid, 1, -1):
                state.valBucket.append(pow(10, i-1))
                state.cntBucket.append(0)
                print("   $", pow(10, i-1), sep="",  end="")

        print("\n\n")
        return 1

#Function run_simulation()
def run_simulation(system, state):
        """Simulate the game.
        system: System object
        state: State object
    
        returns: a dummy numeric value of 1
        """   
        #get random path        
                
        for i in range(0, state.cntSimulation):
            direction =[]
            pathList =[]
            scoreWall = state.intLane
            for j in range(0, system.myMatrixRows-1):
                direction = system.directionList[random.randint(0,1)]
                if direction == 'L':
                    scoreWall -= 0.5
                else:
                    scoreWall += 0.5

                #print('calc:', direction, scoreWall)
                if scoreWall < system.minWall:
                    scoreWall += 1.0
                    direction = 'R'
                    
                if scoreWall > system.maxWall:
                    scoreWall -= 1.0
                    direction = 'L'
                    
                #print('done:', direction, scoreWall) 
                pathList.append(direction)

          
            state.pathDirectionList.append(pathList)
            state.pathScoreList.append(scoreWall)
            #print(str(pathList), " : ", scoreWall, "$ ", state.valBucket[int(scoreWall)-1])
            state.cntBucket[int(scoreWall)-1] += 1

        return 1

#Function draw_board()  
def draw_hist(system, state):
        """Function call to draw the histogram.
        
        system: System object
        state: State object
    
        returns: a dummy numeric value of 1
        """

        x_min = 0.0
        x_max = state.cntBins + 1
        mean = state.intLane 
        std = 2.0

        x = np.linspace(x_min, x_max, state.cntBins)
        y = scipy.stats.norm.pdf(x,mean,std) * (state.cntSimulation/2)
        plt.plot(x,y, 'r-')

        counts, bins = np.histogram(state.pathScoreList)
        plt.hist(bins[:-1], bins, weights=counts)
        plt.xlim(x_min,x_max)
        plt.xlabel('Buckets')
        plt.ylabel('Frequency')        
        plt.title('My Plinko Simulation Histogram for\n{} with drop lane {} and {} simulations'.format(state.name , state.intLane, state.cntSimulation))

        plt.show()
        return 1

        
#Function main()
def main():
        """Main function.
    
        returns: a dummy numeric value of 1
        """   
        #creating the state object.
        state = make_state()

        #greeting the user Hello
        greet_user(system, state, system.inp_Hello )

        #getting user input on the board dimension
        get_input(system, state, system.inp_BoardDimension )

        #draw the baord
        draw_board(system, state)

        #getting user input on the count of simulation
        get_input(system, state, system.inp_CountOfSimulation )

        #running the simulation(s)
        run_simulation(system, state)

        #Prining the Bucket wise count
        print("Bucket Wise Count:")
        for i in range(state.cntBins):
                print("$ {:<10} : {:<10}".format( state.valBucket[i] , state.cntBucket[i]))


        print("\n\n")
        #Prining the path and score/amount of each simulation
        print("Simulation Wise Path/Score:")
        for i in range(state.cntSimulation):
                print("path taken", state.pathDirectionList[i] , "With Score of", state.pathScoreList[i])


        print("\n\n")

        #drawing the histogram
        draw_hist(system, state)

        #greeting the user GoodBye
        greet_user(system, state, system.inp_GoodBye )

        return 1

#running main code now.
main()


