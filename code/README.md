# Knapsack Problem

## Platform Description

All the algorithms were performed on two MacBook Airs with the Apple M1 and M2 chips respectively. The number of cores for both machines was 8 (4 performance and 4 efficiency) with 8 GB of RAM. The language used to write these algorithms was Python 3.11 and Anaconda 3 was the Python distribution used.

## Running the code

```
python project.py -inst <DATASET_INSTANCE> -alg <ALGORITHM> -time <CUTOFF_TIME> -seed <RANDOM_SEED>
```

The dataset instance is a path to a dataset instance. For example, `../DATA/DATASET/small_scale/small_10` would be the path to the tenth small-scale dataset if the `DATA` folder from Canvas was in the root directory.

The algorithm has to be either "BnB", "Approx", "LS1", or "LS2" for Branch and Bound, Approximation, Local Search 1, and Local Search 2 respectively.

The cutoff time has to be some decimal number.

The random seed has to be some integer number. With the same random seed, the outputs should be reproducible.

## Example code inputs

```
python project.py -inst ../DATA/DATASET/large_scale/large_15 -alg LS1 -time 30 -seed 32
python project.py -inst ../DATA/DATASET/small_scale/small_3 -alg BnB -time 50 -seed 64
python project.py -inst ../DATA/DATASET/test/KP_s_06 -alg Approx -time 5 -seed 16
```
