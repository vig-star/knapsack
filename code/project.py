#!/usr/bin/env python3

'''
This file consists of all the code and is the executable file. 
It takes in the command line input and calls the implemented functions as desired based on the parameters.
Written by Vignesh Sreedhar, Sai Manchikalapati, and Pranav Sreedhar.
'''

import argparse
import time
import random

# add argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-inst", "--instance", help="Instance File", dest="instance")
parser.add_argument("-alg", "--algorithm", help="[BnB|Approx|LS1|LS2]", dest="algorithm")
parser.add_argument("-time", "--time", help="Cutoff Time (seconds)", dest="time", type=float)
parser.add_argument("-seed", "--seed", help="Random Seed", dest="seed", type=int)

def read(filepath):
    W = None
    items = []
    # open instance filepath
    with open(filepath) as file:
        for i, line in enumerate(file):
            line = line.strip().split()

            if i == 0:
                # extract weight limit
                W = float(line[1])
            else:
                # each item in items is a tuple of value and weight
                items.append((float(line[0]), float(line[1])))
    
    return items, W

def write(args, selected, maximum):
    
    # create output file in output/solution for deterministic algorithms like BnB/Approx 
    if args.algorithm == "Approx" or args.algorithm == "BnB":
        first = args.instance.rfind("/") + 1
        if first < 0:
            first = 0
        file = open("../output/solution/" + args.instance[first:] + "_" + args.algorithm + "_" + str(args.time) + ".sol", "w")
    # create output file in output/solution for non-deterministic algorithms like BnB/Approx   
    else:
        first = args.instance.rfind("/") + 1
        if first < 0:
            first = 0
        file = open("../output/solution/" + args.instance[first:] + "_" + args.algorithm + "_" + str(args.time) + "_" + str(args.seed) + ".sol", "w")
    
    # write quality (maximum value), then the items selected
    file.write(str(maximum) + "\n")
    for i in range(len(selected)):
        if i == len(selected) - 1:
            file.write(str(selected[i]))
        else:
            file.write(str(selected[i]) + ", ")

def write_trace(args, trace):
    # create output file in output/solution_trace
    if args.algorithm != "Approx":
        first = args.instance.rfind("/") + 1
        if first < 0:
            first = 0
        file = open("../output/solution_trace/" + args.instance[first:] + "_" + args.algorithm + "_" + str(args.time) + "_" + str(args.seed) + ".trace", "w")
    
    # write quality (maximum value), then the items selected
    for time, val in trace:
        file.write(str(time) + ", " + str(val) + "\n")
    
def BnB(items, W, startTime, cutoffTime):
    return None, None, None

def Approx(items, W, startTime, cutoffTime):
    # L holds (heuristic ratio, index, value, and weight), note every item is identified by its index in items
    # The heuristic ratio is the quantity v_i / w_i for every item
    L = [None for i in range(len(items))]

    # Calculate heuristic ratio v_i / w_i, value per unit pound
    for i in range(len(items)):
        L[i] = (float(items[i][0]) / float(items[i][1]), i, items[i][0], items[i][1])
    
    # We sort the items by their heuristic in descending order
    L = sorted(L, key=lambda x : x[0], reverse=True)

    # Indices tracks whether the item identify by index i in 'items' is included in the knapsack or not
    indices = [0 for i in range(len(items))]
    total_weight = 0.0
    v_tot_X = 0.0
    i = 0
    # Continue adding items in order of decreasing heuristic ratio until adding another item exceeds W
    while i < len(items) and total_weight <= W:
        # stop if cutoff time passed
        if (time.time() - startTime) >= cutoffTime:
            break

        if total_weight + L[i][3] > W:
            break
        else:
            # Keep track of the running weight total and value total (total_weight and v_tot_X respectively)
            indices[L[i][1]] = 1
            total_weight += L[i][3]
            v_tot_X += L[i][2]
            i += 1
    
    # If every item is in the knapsack, simply return
    if i >= len(items) - 1:
        return indices, v_tot_X
    else:
        v_tot_k_plus_one = L[i + 1][2]

        # If including simply the next item provides higher value than the current solution, we do that instead
        # This guarentees the approximation is within 1/2 of the optimal solution
        if v_tot_k_plus_one > v_tot_X:
            indices = [0 for i in range(len(items))]
            indices[L[i + 1][1]] = 1
            return indices, v_tot_k_plus_one
        else:
            return indices, v_tot_X

def LS1(items, W, startTime, cutoffTime, seed, maxRestarts = 1000000):
    # stores the best assignment and scores over multiple restarts
    bestAssignment = None
    bestScore = -1
    
    # initialize trace
    trace = []

    # iterate though 
    for i in range(maxRestarts):
        # initialize current assignment with random assignment with seed = seed * i
        random.seed(seed * i)

        # currAssignment = [random.choice([0, 1]) for _ in range(len(items))]

        # initialize with a good approximation with output from Approx and add randomization
        currScore = -1
        currAssignment = []
        approxAssignment = Approx(items, W, startTime, cutoffTime)[0]
        for value in approxAssignment:
            # If the random number is less than 1/len(items), flip the value
            if random.random() < float(1/len(items)):
                currAssignment.append(1 - value)
            else:
                currAssignment.append(value)  

        while True:
            neighbors = []

            # generate neighbors by adding or removing items (flipping the assignment value) 
            for i in range(len(currAssignment)):
                neighbor = currAssignment.copy()
                neighbor[i] = 0 if neighbor[i] == 1 else 1
                neighbors.append(neighbor)

            # initialize our evaluation score to -1
            evalScore = -1
            nextAssignment = None

            # evaluate each neighbor and choose the best one based on total value (with total_ weight <= W)
            for neighbor in neighbors:
                totalWeight = 0
                totalValue = 0
                # calculate total weight and value for each neighbor
                for i in range(len(items)):
                    totalWeight += items[i][1] * neighbor[i]
                    totalValue += items[i][0] * neighbor[i]
                neighborScore = -1
                if totalWeight <= W:
                    neighborScore = totalValue
                # store best neighbor and corresponding score
                if neighborScore > evalScore:
                    nextAssignment = neighbor
                    evalScore = neighborScore

            # evaluate current assignment
            totalWeight = 0
            totalValue = 0
            for i in range(len(items)):
                totalWeight += items[i][1] * currAssignment[i]
                totalValue += items[i][0] * currAssignment[i]
            if totalWeight <= W:
                currScore = totalValue
            
            # trace if evalScore is better than bestScore
            if currScore >= bestScore:
                if evalScore > currScore:
                    trace.append((time.time() - startTime, evalScore))

            # if current assignment is better than its neighbors, you have arrived at a local optima and break
            if evalScore <= currScore:
                break
            currAssignment = nextAssignment
            # stop if cutoff time passed and return the best of bestAssignment and currAssignment
            if (time.time() - startTime) >= cutoffTime:
                if bestScore > currScore:
                    return bestAssignment, bestScore, trace
                else:
                    return currAssignment, currScore, trace
        # update the best score and add to trace
        if currScore > bestScore:
            if len(trace) == 0:
                trace.append((time.time() - startTime, currScore))
            if len(trace) >= 1 and trace[-1][1] < currScore:
                trace.append((time.time() - startTime, currScore))
            bestScore = currScore
            bestAssignment = currAssignment
        
        # stop if cutoff time passed and return the bestAssignment
        if (time.time() - startTime) >= cutoffTime:
            return bestAssignment, bestScore, trace
    return bestAssignment, bestScore, trace




def LS2(items, W, startTime, cutoffTime, seed, maxRestarts = 1000000, p=0.3):
    # stores the best assignment and scores over multiple restarts
    bestAssignment = None
    bestScore = -1
    
    # initialize trace
    trace = []

    # iterate though 
    for i in range(maxRestarts):
        # initialize current assignment with random assignment with seed = seed * i
        random.seed(seed * i)

        # currAssignment = [random.choice([0, 1]) for _ in range(len(items))]

        # initialize with a good approximation with output from Approx and add randomization
        currScore = -1
        currAssignment = []
        approxAssignment = Approx(items, W, startTime, cutoffTime)[0]
        for value in approxAssignment:
            # If the random number is less than 1/len(items), flip the value
            if random.random() < float(1/len(items)):
                currAssignment.append(1 - value)
            else:
                currAssignment.append(value)  

        while True:
            neighbors = []

            # generate neighbors by adding or removing items (flipping the assignment value) 
            for i in range(len(currAssignment)):
                neighbor = currAssignment.copy()
                neighbor[i] = 0 if neighbor[i] == 1 else 1
                neighbors.append(neighbor)
            # due to timeout concerns with exceptionally large >5000-10000 items, we will not swap
            if len(items) < 5000:
                # generate neighbors by swapping items in and out of the knapsack 
                for i in range(len(currAssignment)):
                    for j in range(len(currAssignment)):
                        if currAssignment[i] == 1 and currAssignment[j] == 0:
                            neighbor = currAssignment.copy()
                            neighbor[i] = 0
                            neighbor[j] = 1
                            neighbors.append(neighbor)
            # initialize our evaluation score to -1
            evalScore = -1
            nextAssignment = None

            # evaluate each neighbor, with probability p, don't update next assignment to better scoring neighbor 
            for n, neighbor in enumerate(neighbors):
                totalWeight = 0
                totalValue = 0
                # calculate total weight and value for each neighbor
                for i in range(len(items)):
                    totalWeight += items[i][1] * neighbor[i]
                    totalValue += items[i][0] * neighbor[i]
                neighborScore = -1
                if totalWeight <= W:
                    neighborScore = totalValue
                # update next assignment with better neighbor if above p
                random.seed(seed + n)
                if neighborScore > evalScore and random.random() > p:
                    nextAssignment = neighbor
                    evalScore = neighborScore

            # evaluate current assignment
            totalWeight = 0
            totalValue = 0
            for i in range(len(items)):
                totalWeight += items[i][1] * currAssignment[i]
                totalValue += items[i][0] * currAssignment[i]
            if totalWeight <= W:
                currScore = totalValue
            
            # trace if evalScore is better than bestScore
            if currScore >= bestScore:
                if evalScore > currScore:
                    trace.append((time.time() - startTime, evalScore))

            # if current assignment is better than its neighbors, you have arrived at a local optima and break
            if evalScore <= currScore:
                break
            currAssignment = nextAssignment
            # stop if cutoff time passed and return the best of bestAssignment and currAssignment
            if (time.time() - startTime) >= cutoffTime:
                if bestScore > currScore:
                    return bestAssignment, bestScore, trace
                else:
                    return currAssignment, currScore, trace
        # update the best score and add to trace
        if currScore > bestScore:
            if len(trace) == 0:
                trace.append((time.time() - startTime, currScore))
            if len(trace) >= 1 and trace[-1][1] < currScore:
                trace.append((time.time() - startTime, currScore))
            bestScore = currScore
            bestAssignment = currAssignment
        
        # stop if cutoff time passed and return the bestAssignment
        if (time.time() - startTime) >= cutoffTime:
            return bestAssignment, bestScore, trace
    return bestAssignment, bestScore, trace


def main():
    # parse arguments
    args = parser.parse_args()

    # error handle arguments to ensure all required arguments are passed in and valid
    if args.algorithm is None:
        print("Enter a valid algorithm")
        exit()
    if args.instance is None:
        print("Enter a valid instance")
        exit()
    if args.time is None:
        print("Enter a valid cutoff time")
        exit()
    if args.algorithm not in set(["BnB", "Approx", "LS1", "LS2"]):
        print("You need to enter a valid algorithm of choice: BnB, Approx, LS1, LS2!")
        exit()
    if args.algorithm == "LS1" or args.algorithm == "LS2":
        if args.seed:
            random.seed(args.seed)
        else:
            print("You need to enter a random seed for Local Search!")
            exit()
    try:
        # call read function to get items and weight limit
        items, W = read(args.instance)
    except Exception as e:
        print("Error reading instance: ", e)
        exit()
    
    # check one last time that items and W are not None
    if items is None:
        print("Error reading items from instance")
        exit()
    if W is None:
        print("Error reading weight from instance")
        exit()

    # initialize start and cutoff time
    start = time.time()
    cutoff = float(args.time)

    # call algorithms based on input and pass items, W, start and cutoff
    if args.algorithm == "BnB":
        selected, maximum, trace = BnB(items, W, start, cutoff)
    elif args.algorithm == "Approx":
        selected, maximum = Approx(items, W, start, cutoff)
    elif args.algorithm == "LS1":
        selected, maximum, trace = LS1(items, W, start, cutoff, args.seed)
    elif args.algorithm == "LS2":
        selected, maximum, trace = LS2(items, W, start, cutoff, args.seed)
    
    # calculate total time for algorithm to end
    end = time.time()
    
    # print outputs and execution time before writing output file
    print(selected)
    print(maximum)
    print("Execution Time (seconds): " + str(end - start))
    
    # call write function to write algorithm output
    try:
        write(args, selected, float(maximum))
        if args.algorithm != "Approx":
            write_trace(args, trace)
    except Exception as e:
        print("Error writing solution: ", e)
        exit()
    


if __name__ == "__main__":
    main()