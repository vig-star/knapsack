# Running the knapsack solver

Read the [project README](../README.md) for the problem description, algorithm comparison, dataset and output formats, and current correctness limitations.

## Quick start

Run these commands **from this `code/` directory**. The program writes to `../output/solution/` and `../output/solution_trace/`, relative to the current working directory.

```bash
python3 project.py -inst ../DATA/DATASET/test/KP_s_01 -alg BnB -time 1
python3 project.py -inst ../DATA/DATASET/test/KP_s_01 -alg Approx -time 1
python3 project.py -inst ../DATA/DATASET/test/KP_s_01 -alg LS1 -time 1 -seed 32
python3 project.py -inst ../DATA/DATASET/test/KP_s_01 -alg LS2 -time 1 -seed 32
```

Python 3 is required; there are no third-party dependencies. All datasets and output directories are included in the repository.

Choose `BnB`, `Approx`, `LS1`, or `LS2` with `-alg`. Supply an input path with `-inst` and a positive time budget in seconds with `-time`. Local search (`LS1` and `LS2`) also requires a nonzero integer `-seed`. A seed controls random choices, but time-based stopping means identical results across runs are not guaranteed.

Use `python3 project.py --help` for the available flags. Repeating a command overwrites its matching output files.

## Original platform

The original experiments used Python 3.11 with Anaconda 3 on two MacBook Air machines, with Apple M1 and M2 chips respectively. Both machines had 8 CPU cores (4 performance and 4 efficiency) and 8 GB RAM. Anaconda is not required to run the code.
