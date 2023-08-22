# bench-solver
Ad-hoc runtime benchmarking tool supporting model-checkers [CGAAL](https://github.com/d702e20/CGAAL/) and [PRISM-games](https://github.com/prismmodelchecker/prism-games).
Benchmark results for paper(pending publication) are found at [results-model-checker](https://github.com/d702e20/results-model-checker).

# Setup
1. Install model-checkers as described by their instructions. 
  1. For CGAAL, we use Rust 1.69.0 (MSRV is 1.65.0) and compile from [64624f6](https://github.com/d702e20/CGAAL/tree/64624f687d0d3684a28ebe28375713008e8515ea) with `cargo build --release`. 
  1. For `PRISM-games` we compile from the [6dcd804](https://github.com/prismmodelchecker/prism-games/tree/6dcd804e26c4d8c0f37d1512f92a79abf455e839) to include a required bugfix from the authors and follow the [PRISM-games installation guide](http://www.prismmodelchecker.org/games/installation.php) for compiling from source with PPL.
1. Make a python3 virtual environment `python3 -m venv venv` and install requirements `pip3 install -rrequirements.txt`. Lastly source it `source venv/bin/activate`.
1. Change variables in `benchmark-suite.py` such as which `SUITE` or `SEARCH_STRATEGY` to suit your needs.
1. Run benchmarks by `python3 benchmark-suite.py` which will show the currently running benchmark, and will emit intermediate results when each test completes.
1. When suite has been benchmarked, find resulting CSV by the following format `results/$suitename-$search-strategy-$timestamp.csv`.

## Suites
The suites (set of tests the benchmark will run) are defined by a CSV file found in `suites/` with the columns `name,model,formula`.
Multiple suites exist for our purposes due to some benchmarks taking days to complete. The full benchmark suite for both model-checkers can be found in `suites/cgaal-full.csv` and `suites/prism-full.csv`, respectively.

## Limitations
- Measurement of memory by way of using `ru_maxrss` in previous tests are flawed and may be ignored. Would be nice to include this, although results upper bound on memory usage exists.
- Very quick benchmarks (<100ms), may have noise in results. Preferably each test should be run for a minimum of some time, and the average of the completed runs be used as results.


