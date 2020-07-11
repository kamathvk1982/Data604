import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import time
import math
import random
from modsim import *
import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np

st.title('My Plinko Game App')

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
                     )  #returns a State objec

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
        st.write("\t\t    ", end="")
        #for i in range(state.cntBins):
        #        st.write(i+1,"", sep="      ", end="")
        #st.write()
        #for i in range(system.myMatrixRows):
        #        if (i % 2) == 0:
        #                st.write("\t\t|","*      " * (system.myMatrixCols-1),"* |", sep="")
        #        else:
        #                st.write("\t\t|", "   *   " * (system.myMatrixCols-1),"  |", sep="")

        #get value for the buckets
        mid =  math.ceil(state.cntBins/2)
        #st.write("\t\t  ", end="")
        for i in range(1, mid+1):
                state.valBucket.append(pow(10, i))
                state.cntBucket.append(0)
                #st.write("   $", pow(10, i), sep="",  end="")
        if (mid % 2) == 0:
                mid += 1
        for i in range(mid, 1, -1):
                state.valBucket.append(pow(10, i-1))
                state.cntBucket.append(0)
                #st.write("   $", pow(10, i-1), sep="",  end="")

        st.write("\n\n")
        #return 1

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

        #return 1


#creating the state object.
state = make_state()



state.cntBins = st.sidebar.slider('Which number do you like buckets?',1, 5, 3, 1)
state.intLane = st.sidebar.slider('Which number do you like Drop Lane?',1, 5, 3, 1)
state.cntSimulation = st.sidebar.slider('Which number do you like Simulation for?',1, 1000, 100, 1)

'You selected cntBins:', state.cntBins
'You selected intLane:', state.intLane
'You selected cntSimulation:', state.cntSimulation

draw_board(system, state)
run_simulation(system, state)

draw_hist(system, state)

#Prining the Bucket wise count
st.write("Bucket Wise Count:")
for i in range(state.cntBins):
	st.write("$ {:<10} : {:<10}".format( state.valBucket[i] , state.cntBucket[i]))
