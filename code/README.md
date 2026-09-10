# Running the knapsack solver

[← Project overview](../README.md)

Run all commands below **from this `code/` directory**. Python 3 is required; all dependencies are in the standard library. Datasets and output directories are included in the repository.

## Commands

```bash
python3 project.py -inst ../DATA/DATASET/test/KP_s_01 -alg BnB -time 1
python3 project.py -inst ../DATA/DATASET/test/KP_s_01 -alg Approx -time 1
python3 project.py -inst ../DATA/DATASET/test/KP_s_01 -alg LS1 -time 1 -seed 32
python3 project.py -inst ../DATA/DATASET/test/KP_s_01 -alg LS2 -time 1 -seed 32
```

| Argument | Meaning |
| --- | --- |
| `-inst`, `--instance` | Required path to an input file. |
| `-alg`, `--algorithm` | Required, case-sensitive choice: `BnB`, `Approx`, `LS1`, or `LS2`. |
| `-time`, `--time` | Required time budget in seconds; use a positive number. Decimals are accepted. |
| `-seed`, `--seed` | Required for `LS1` and `LS2`; use a nonzero integer such as `32`. Not needed for `BnB` or `Approx`. |

Use `python3 project.py --help` for the available flags. A seed controls random choices, but time-based stopping means identical results across runs are not guaranteed.

## Input format

Each instance is a whitespace-separated text file:

```text
number_of_items capacity
value_of_item_1 weight_of_item_1
value_of_item_2 weight_of_item_2
...
```

Values and weights are read as floating-point numbers. Item order determines the positions in the output selection vector. The parser reads the capacity from the header but does not validate the declared item count. Use positive weights; ratio calculations divide by weight.

The `test_solution/` reference files contain one binary selection flag per line. The `small_scale_solution/` and `large_scale_solution/` references contain a single objective value. These reference formats differ from generated `.sol` files.

## Output format

The program prints the reported value and execution time, then writes files under `../output/`, relative to the working directory.

| Directory | Contents |
| --- | --- |
| [`output/solution/`](../output/solution/) | `.sol`: total value on line 1, comma-separated binary selection flags on line 2. |
| [`output/solution_trace/`](../output/solution_trace/) | `.trace`: `elapsed_seconds, solution_value` records as the search reports progress. |

Selection flags follow the original input order: `1` selects an item, `0` leaves it out. They are not item IDs. `BnB`, `LS1`, and `LS2` produce traces; `Approx` does not.

| Algorithms | Solution filename |
| --- | --- |
| `BnB`, `Approx` | `<instance>_<algorithm>_<time>.sol` |
| `LS1`, `LS2` | `<instance>_<algorithm>_<time>_<seed>.sol` |

Trace files use the same base name with a `.trace` extension. Time is formatted as a float: `-time 1` produces `1.0` in filenames.

For example, the first command above writes:

```text
../output/solution/KP_s_01_BnB_1.0.sol
../output/solution_trace/KP_s_01_BnB_1.0.trace
```

> [!NOTE]
> Output directories must exist; both are included in the repository. Reusing the same instance, algorithm, time, and seed overwrites the matching output files.

## Checking a result

1. Match each selection flag to the corresponding input item.
2. Sum the selected weights and confirm they do not exceed capacity.
3. Sum the selected values and confirm they match the reported value.
4. Compare that total with the supplied reference value or selection.

Read the [project notes](../README.md#project-notes) for known correctness issues and timing limitations before interpreting the results.
