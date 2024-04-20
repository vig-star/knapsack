# Knapsack Problem

## Platform Description

All the algorithms were performed on two MacBook Airs with the Apple M1 and M2 chips respectively. The number of cores for both machines was 8 (4 performance and 4 efficiency) with 8 GB of RAM. The language used to write these algorithms was Python 3.11 and Anaconda 3 was the Python distribution used.

## Storing the inputs

Make sure to store the unzipped DATA folder from Canvas in the same directory as the `project.py` file. This is crucial for the code to run correctly as it writes to and reads from the dataset files in `DATA/DATASET/`.

## Running the code

```
python project.py -inst <DATASET_INSTANCE> -alg <ALGORITHM> -time <CUTOFF_TIME> -seed <RANDOM_SEED>
```

The dataset instance is a path to a dataset instance. For example, `small_scale/small_10` would be the path to the tenth small-scale dataset.

The algorithm has to be either "BnB", "Approx", "LS1", or "LS2" for Branch and Bound, Approximation, Local Search 1, and Local Search 2 respectively.

The cutoff time has to be some decimal number.

The random seed has to be some integer number. With the same random seed, the outputs should be reproducible.

## Example code inputs

```
python project.py -inst large_scale/large_15 -alg LS1 -time 30 -seed 32
python project.py -inst small_scale/small_3 -alg LS1 -time 10 -seed 32
python project.py -inst test/KP_s_06 -alg LS1 -time 5 -seed 32
```
