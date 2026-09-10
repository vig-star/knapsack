# Knapsack: comparing four ways to choose the best items

This project explores the **0/1 knapsack problem**: given items with a value and a weight, choose the combination with the highest total value without exceeding a weight limit. Each item is either selected once or left out.

Think of packing a bag with limited capacity. The same model can represent choosing projects within a budget or selecting jobs within a resource limit.

The repository implements four algorithms in Python and includes datasets, saved solutions, and timing traces. Its purpose is to compare **solution quality against computation time**: how much value can each approach find, and how quickly? It is an educational command-line experiment.

## The four approaches

| CLI name | Approach | What it does |
| --- | --- | --- |
| `BnB` | Branch and bound | Starts with the greedy result, explores include/exclude decisions, and prunes branches using a fractional-knapsack bound. Intended to search for an optimal solution when time permits. |
| `Approx` | Greedy approximation | Sorts by value per unit weight, takes a prefix that fits, and compares it with a single-item alternative. Provides a fast baseline. |
| `LS1` | Local search with restarts | Perturbs the greedy selection, then improves it by adding or removing one item at a time. Restarts to explore other selections. |
| `LS2` | Stochastic local search with restarts | Adds item swaps to the single-item moves and uses randomized neighbor selection. Swaps are disabled for instances with 5,000 or more items. |

These describe the implementations' intended roles. The current code has correctness limitations; see [Current limitations](#current-limitations) before treating a result as optimal or using an approximation guarantee.

## Run your first example

Requires **Python 3** and Git to clone the repository. The original project used Python 3.11; the commands below were also checked with Python 3.9.6. All imports are from the Python standard library, so there are no packages to install.

1. Clone the repository and enter its `code` directory:

   ```bash
   git clone https://github.com/vig-star/knapsack.git
   cd knapsack/code
   ```

   If you already have the repository locally, enter its `code` directory. **Run the program from there:** output paths are relative to the current working directory.

2. Solve the first test instance with branch and bound:

   ```bash
   python3 project.py -inst ../DATA/DATASET/test/KP_s_01 -alg BnB -time 1
   ```

   This instance has 10 items and a capacity of 165. The checked run found value `309.0`, matching the supplied reference selection. The program also prints elapsed time in seconds.

3. Read the saved solution:

   ```bash
   cat ../output/solution/KP_s_01_BnB_1.0.sol
   ```

   Expected contents for this example:

   ```text
   309.0
   1, 1, 1, 1, 0, 1, 0, 0, 0, 0
   ```

   The selected items weigh exactly 165. A `1` selects the item at that position in the input; a `0` leaves it out.

## Try the other algorithms

Run these from `code/` on the same instance:

```bash
python3 project.py -inst ../DATA/DATASET/test/KP_s_01 -alg Approx -time 1
python3 project.py -inst ../DATA/DATASET/test/KP_s_01 -alg LS1 -time 1 -seed 32
python3 project.py -inst ../DATA/DATASET/test/KP_s_01 -alg LS2 -time 1 -seed 32
```

In a smoke check, `Approx` returned value 266; `BnB`, `LS1`, and `LS2` returned 309. All four selections fit the capacity and matched their reported values on this instance. These are example results, not a benchmark or a guarantee for other inputs.

| Argument | Meaning |
| --- | --- |
| `-inst`, `--instance` | Required path to an input file. |
| `-alg`, `--algorithm` | Required, case-sensitive choice: `BnB`, `Approx`, `LS1`, or `LS2`. |
| `-time`, `--time` | Required time budget in seconds; use a positive number. Decimals are accepted. |
| `-seed`, `--seed` | Required for `LS1` and `LS2`; use a nonzero integer such as `32`. Not needed for `BnB` or `Approx`. |

Use `python3 project.py --help` to display the command-line options. Start with a test or small instance before trying the larger datasets.

## Inputs and included datasets

Each input is a whitespace-separated text file:

```text
number_of_items capacity
value_of_item_1 weight_of_item_1
value_of_item_2 weight_of_item_2
...
```

Values and weights are read as floating-point numbers. Item order determines the positions in the output selection vector. The parser reads the capacity from the header but does not validate the declared item count. Use positive weights; ratio calculations divide by weight.

All datasets are already included under `DATA/DATASET/`:

| Input directory | Instances | Items per instance | Reference directory and format |
| --- | --- | --- | --- |
| `test/` | 8 | 5–24 | `test_solution/`: one `0` or `1` per item, one per line. |
| `small_scale/` | 10 | 4–23 | `small_scale_solution/`: a single reference objective value. |
| `large_scale/` | 21 | 100–10,000 | `large_scale_solution/`: a single reference objective value. |

For comparison, calculate the selected items' total weight and value, check that the weight is within capacity, then compare the value with the supplied reference. Reference files are separate from the solver's generated `.sol` files.

## Outputs and repository layout

```text
knapsack/
├── README.md                 # Project overview and usage
├── code/
│   ├── project.py            # CLI, four algorithms, input/output helpers
│   └── README.md             # Short running guide and original platform notes
├── DATA/DATASET/             # 39 input instances and matching references
└── output/
    ├── solution/             # Saved .sol results
    └── solution_trace/       # Saved .trace progress records
```

A `.sol` file contains the reported total value on the first line and comma-separated binary selection flags on the second line. The flags follow the original input order; they are not item IDs.

A `.trace` file contains `elapsed_seconds, solution_value` records as the search reports progress. `BnB`, `LS1`, and `LS2` produce traces; `Approx` does not.

| Algorithms | Filename pattern |
| --- | --- |
| `BnB`, `Approx` | `<instance>_<algorithm>_<time>.sol` |
| `LS1`, `LS2` | `<instance>_<algorithm>_<time>_<seed>.sol` |

Trace files use the same base name with a `.trace` extension. Time is formatted as a float, so `-time 1` produces `1.0` in filenames. Output directories must exist; both are included in this repository. Reusing the same instance, algorithm, time, and seed overwrites the matching output files.

The committed outputs are results from earlier runs with different time budgets. They provide examples to inspect, but do not constitute a controlled comparison at equal budgets.

## Current limitations

The repository preserves the original algorithm implementations. There is no automated test suite; the four-command smoke check above covers only `KP_s_01`.

- **Approximation correctness:** `Approx` stops at the first item that does not fit, but its single-item comparison uses the following item and does not check that item's weight against capacity. The code comment's claimed 1/2 approximation guarantee should not be relied on.
- **Branch-and-bound correctness:** `BnB` uses `Approx` as its starting result, and its bound calculation truncates a fractional contribution to an integer even though fractional values are accepted. Do not assume every returned result is feasible or proven optimal.
- **Local-search cutoff results:** a cutoff can return a newly selected assignment with the previous assignment's score. Recalculate the value and weight from the selection flags before comparing results.
- **Timing and repeatability:** cutoffs are checked between portions of work, so expensive sorting or neighbor evaluation can exceed the requested budget. A fixed seed controls random choices, but time-based stopping can change the final result across runs or machines.

## Authors and original environment

Written by **Vignesh Sreedhar, Sai Manchikalapati, and Pranav Sreedhar**.

The original experiments used Python 3.11 through Anaconda 3 on MacBook Air machines with Apple M1 and M2 chips, 8 CPU cores, and 8 GB RAM. Anaconda is not required to run the program.
