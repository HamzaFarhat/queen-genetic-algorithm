from random import randint, uniform
from copy import deepcopy

#Initialize mutation probability, crossover rate, and population size
mutationRate = 0.01
crossoverRate = 0.7
populationSize = 10

#92 solutions in total, counter starts at 0 so reaching 91 will result in 92 solutions
target = 91
# solutionsCounter = 0
solutionSet = set()

#board class to contain all methods related to the board
class Board:

    #Board constructor to generate random board and calculate fitness
    def __init__(self):
        self.board = [randint(0,7) for x in range(8)]
        self.weakness = self.numberOfAttacks()

    #fitness function to determine the number of attacks possible by a given board, want to minimize this value
    #returns number of times queens can attack eachother for a given board
    def numberOfAttacks(self):
        #initialize total number of attacks counter
        numberOfAttacks = 0
        i = 0

        #loop through each index on the board
        while i <=6:
            currentPiece = self.board[i]
            
            j=i+1

            #simulate attacks for all other columns on the board
            while j <=  7: 

                #difference between two locations determines if attack is possible
                diagonal = j -i
                defender = self.board[j]

                #increment attack counter if queen in same row
                if currentPiece == defender:
                    numberOfAttacks +=1
                #increment attack coutner if queen can attack another piece diagonally upward
                if currentPiece == defender + diagonal:
                    numberOfAttacks +=1
                #increment attack counter if queen can attack diagonally downward
                if currentPiece == defender - diagonal:
                    numberOfAttacks+=1
                j=j+1
            i=i+1

        return numberOfAttacks
    
    #mutate a random gene within a given chromosome (board), and recalculate its fitness
    def chromosomeMutation(self):
        self.board[randint(0,7)] = randint(0,7)
        # print("MUTATION BEFORE:", self.weakness)
        self.weakness = self.numberOfAttacks()
        # print("MUTATION AFTER:", self.weakness)


#determine if mutation will occur or not based on mutation rate global variable
def toMutate():
    mutation = uniform(0,1)
    if  mutation <= mutationRate:
        return True
    else:
        return False

def crossover(mom, dad):
    child1 = deepcopy(mom)
    child2 = deepcopy(dad)

    crossover = uniform(0,1)

    if  crossover <= crossoverRate:
        splitLocation = randint(1,6)
        temp = child1.board[splitLocation:]
        child1.board[splitLocation:] = child2.board[splitLocation:]
        child2.board[splitLocation:] = temp
    
    # print("CROSSOVER WEAKNESS BEFORE:", child1.weakness, child2.weakness)
    child1.weakness = child1.numberOfAttacks()
    child2.weakness = child2.numberOfAttacks()
    # print("CROSSOVER WEAKNESS AFTER:", child1.weakness, child2.weakness)


    return child1, child2

def completed():
    # if solutionsCounter == target:
    if len(solutionSet) == target:
        return True
    else:
        return False


def roulette(populationArray):

    weaknessSum = sum(board.weakness for board in populationArray)
    ratios = [board.weakness/weaknessSum for board in populationArray]
    wheel = []

    for i in range(len(populationArray)):
        if i == 0:
            wheel.append(ratios[i])
        if i != 0:
            wheel.append(ratios[i] + ratios[i-1])
    # print(wheel)

    momProbability = uniform(0,1)
    dadProbability = uniform(0,1)
    mom = Board()
    dad = Board()

    for i in reversed(range(len(wheel))):
        if momProbability ==1:
            mom = populationArray[len(populationArray)]
        if momProbability <= wheel[i]:
            mom = populationArray[i]
    
    for i in reversed(range(len(wheel))):
        if dadProbability ==1:
            dad = populationArray[len(populationArray)]
        if dadProbability <= wheel[i]:
            dad = populationArray[i]
 
    return mom, dad

def solutionChecker(arr):
    for board in arr:
        if board.weakness == 0:
            # solutionsCounter+=1
            if tuple(board.board) not in solutionSet:
                print("solution",len(solutionSet), "found =", board.board)

            solutionSet.add(tuple(board.board))
            # print("Solution", "=", board.board)

if __name__ == '__main__':

    populationArray = []
    generation = 0

    for i in range(populationSize):
        populationArray.append(Board())


    complete = completed()
    
    while not complete:
        generation += 1

        newPopulation =[]
        
        for i in range(int(populationSize/2)):
            mom, dad = roulette(populationArray)
    
            child1, child2 = crossover(mom,dad)
            
            if toMutate():
                child1.chromosomeMutation()
            if toMutate():
                child2.chromosomeMutation()

            newPopulation.append(child1)
            newPopulation.append(child2)
        
        solutionChecker(newPopulation)
        populationArray = newPopulation

    print(solutionSet)

        
            






