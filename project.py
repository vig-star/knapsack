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
    # open instance filepath (assuming DATA folder from Canvas in root)
    with open("./DATA/DATASET/" + filepath) as file:
        for i, line in enumerate(file):
            line = line.strip().split()

            if i == 0:
                # extract weight limit
                W = int(line[1])
            else:
                # each item in items is a tuple of value and weight
                items.append((int(line[0]), int(line[1])))
    
    return items, W

def write(args, selected, maximum):
    # create output file in output/solution for deterministic algorithms like BnB/Approx 
    if args.algorithm == "Approx" or args.algorithm == "BnB":
        first = args.instance.find("/") + 1
        if first < 0:
            first = 0
        file = open("./output/solution" + args.instance[first:] + "_" + args.algorithm + "_" + str(args.time) + ".sol", "w")
    # create output file in output/solution for non-deterministic algorithms like BnB/Approx   
    else:
        first = args.instance.find("/") + 1
        if first < 0:
            first = 0
        file = open("./output/solution" + args.instance[first:] + "_" + args.algorithm + "_" + str(args.time) + "_" + str(args.seed) + ".sol", "w")
    
    # write quality (maximum value), then the items selected
    file.write(str(maximum) + "\n")
    for i in range(len(selected)):
        if i == len(selected) - 1:
            file.write(str(selected[i]))
        else:
            file.write(str(selected[i]) + "\n")
    
def BnB(items, W):
    return None, None

def Approx(items, W):
    L = [None for i in range(len(items))]

    for i in range(len(items)):
        L[i] = (float(items[i][0]) / float(items[i][1]), i, items[i][0], items[i][1])
    
    L = sorted(L, key=lambda x : x[0], reverse=True)

    indices = [0 for i in range(len(items))]
    total_weight = 0.0
    v_tot_X = 0.0
    i = 0
    while i < len(items) and total_weight <= W:
        if total_weight + L[i][3] > W:
            break
        else:
            indices[L[i][1]] = 1
            total_weight += L[i][3]
            v_tot_X += L[i][2]
            i += 1
    
    if i == len(items):
        return indices, v_tot_X
    else:
        v_tot_k_plus_one = L[i + 1][2]

        if v_tot_k_plus_one > v_tot_X:
            indices = [0 for i in range(len(items))]
            indices[L[i + 1][1]] = 1
            return indices, v_tot_k_plus_one
        else:
            return indices, v_tot_X

def LS1(items, W, startTime):
    return None, None

def LS2(items, W):
    return None, None

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


    start = time.time()

    if args.algorithm == "BnB":
        selected, maximum = BnB(items, W)
    elif args.algorithm == "Approx":
        selected, maximum = Approx(items, W)
    elif args.algorithm == "LS1":
        selected, maximum = LS1(items, W, start)
    elif args.algorithm == "LS2":
        selected, maximum = LS2(items, W)

    end = time.time()
    
    # print outputs and execution time before writing output file
    print(selected)
    print(maximum)
    print("Execution Time (seconds): " + str(end - start))
    
    # call write function to write algorithm output
    write(args, selected, int(maximum))


if __name__ == "__main__":
    main()