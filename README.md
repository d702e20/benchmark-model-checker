# bench-solver
Homebrewed runtime benchmarking tool supporting model-checkers (CGAAL)[https://github.com/d702e20/CGAAL/] and (PRISM-games)[https://github.com/prismmodelchecker/prism-games].

## Setup
Define a suite - a collection of tests - in a CSV-file with the columns; name, model, formula. Model and formula are paths relative to the model-checker dirs set in `benchmark-suite.py`. For examples, look in `suites/`.

Once installation of modelchecker is complete, set binary path, examples path, timeout, and lastly search strategy if applicable.

Finally run `python benchmark-suite.py` where results are written after each test to CSV named by suite-name concatenated with timestamp. This allows for reading results while benchmarks are being run, as some suites may take multiple days.

## Limitations
1. Measurement of memory by way of using `ru_maxrss` in previous tests are flawed and may be ignored. Would be nice to include this, although results upper bound on memory usage exists.
1. For quick benchmarks (<1s), may have noise in results. Preferably each test should be run for a minimum of some time, and the average of the completed runs be used as result. 


