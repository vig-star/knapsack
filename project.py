import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument("-inst", "--instance", help="Instance", dest="instance")
parser.add_argument("-alg", "--algorithm", help="[BnB|Approx|LS1|LS2]", dest="algorithm")
parser.add_argument("-time", "--time", help="Cutoff Time (seconds)", dest="time", type=float)
parser.add_argument("-seed", "--seed", help="Random Seed", dest="seed", type=int)

def read(filepath):
    W = None
    items = []

    with open("./DATA/DATASET/" + filepath) as file:
        for i, line in enumerate(file):
            line = line.strip().split()

            if i == 0:
                W = int(line[1])
            else:
                items.append((int(line[0]), int(line[1])))
    
    return items, W

def write(args, selected):
    if args.algorithm == "Approx":
        first = args.instance.index("/") + 1
        file = open(args.instance[first:] + "_" + args.algorithm + "_" + str(args.time) + ".sol", "w")
    
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

def LS1(items, W):
    return None, None

def LS2(items, W):
    return None, None

def main():
    args = parser.parse_args()

    if args.algorithm not in set(["BnB", "Approx", "LS1", "LS2"]):
        exit()
    
    items, W = read(args.instance)
    
    start = time.time()
    if args.algorithm == "BnB":
        selected, maximum = BnB(items, W)
    elif args.algorithm == "Approx":
        selected, maximum = Approx(items, W)
    elif args.algorithm == "LS1":
        selected, maximum = LS1(items, W)
    elif args.algorithm == "LS2":
        selected, maximum = LS2(items, W)
    end = time.time()
    
    print(selected)
    print(maximum)
    print("Execution Time (seconds): " + str(end - start))
    
    write(args, selected)


if __name__ == "__main__":
    main()