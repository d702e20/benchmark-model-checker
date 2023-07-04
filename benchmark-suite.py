import os
import subprocess
import time
from datetime import datetime
from resource import getrusage, RUSAGE_CHILDREN

import pandas as pd
import re
from datetime import timedelta

# VARIABLES
PRISM = True
SUITE = "prism-suite.csv"
# choice of ["bfs", "dfs", "los", "lps", "dhs", "ihs", "lrs", "global"]
SEARCH_STRATEGIES = ["bfs", "dfs", "los", "lps", "dhs", "ihs", "lrs", "global"] if not PRISM else ["none"]

ENV = 'PATH="/scratch/user@domain.aau.dk/prism-games/jdk/jdk-20.0.1/bin:$PATH"'

for SEARCH_STRATEGY in SEARCH_STRATEGIES:
    SUBCMD = SEARCH_STRATEGY if SEARCH_STRATEGY == "global" else "solver"
    SEARCH_STRATEGY_ARG = "" if SEARCH_STRATEGY == "global" else "--search-strategy"
    if PRISM:
        SEARCH_STRATEGY = "prism"


    def strip(text):
        try:
            return text.strip()
        except AttributeError:
            return text


    # Thread count combinations to use [1, 2, 4, ... , 32]
    THREADS = [pow(2, x) for x in range(0, 6)] if not PRISM else ["none"]

    PRISM_DIR = "../prism-games/"
    PRISM_EXAMPLES_DIR = "../Prism-modeling/benchmarking/"  # fixme
    PRISM_BIN = "../prism-games/prism/bin/prism"

    CGAAL_DIR = "../cgaal/"
    CGAAL_EXAMPLES_DIR = "../cgaal/lcgs-examples/"
    CGAAL_BIN = "../cgaal/target/release/atl-checker-cli"

    # compile solver if not already done (requires that 'cargo' is in PATH of shell which is running this script)
    # subprocess.run(f"cd {CGAAL_DIR} && cargo build --release", stdout=subprocess.PIPE, shell=True)

    # setup dataframe to store results
    if PRISM:
        df = pd.DataFrame(
            columns=['name', 'model', 'formula', 'time_s', 'memory_MB', 'total_reported', 'construction', 'checking'])
    else:
        df = pd.DataFrame(
            columns=['name', 'model', 'formula', 'threads', 'time_s', 'memory_MB', 'search_strategy'])

    # read in suite from csv
    suite = pd.read_csv(SUITE, skipinitialspace=True, converters={'name': strip, 'model': strip, 'formula': strip})

    error = False
    for i, test in suite.iterrows():
        try:
            os.stat(CGAAL_EXAMPLES_DIR if not PRISM else PRISM_EXAMPLES_DIR + test['model'])
        except FileNotFoundError:
            error = True
            print(
                f"ERROR: Could not find '{test['model']}' in '{CGAAL_EXAMPLES_DIR if not PRISM else PRISM_EXAMPLES_DIR}'.")

        try:
            os.stat(CGAAL_EXAMPLES_DIR if not PRISM else PRISM_EXAMPLES_DIR + test['formula'])
        except FileNotFoundError:
            error = True
            print(
                f"ERROR: Could not find '{test['formula']}' in '{CGAAL_EXAMPLES_DIR if not PRISM else PRISM_EXAMPLES_DIR}'.")

    if error:
        print(f"Please fix the above errors in {SUITE}.")
        exit(1)

    # benchmark each program in suite
    for index, row in suite.iterrows():
        for threads in THREADS:
            print(
                f"[{SEARCH_STRATEGY}|{index}/{len(suite)}] {row['name']}/{threads} with model: '{row['model']}' and formula: '{row['formula']}'")
            try:
                if not PRISM:
                    max_mem_before = getrusage(RUSAGE_CHILDREN).ru_maxrss / 1024
                    start_time = time.perf_counter()
                    proc = subprocess.run(
                        f'{CGAAL_BIN} {SUBCMD} '
                        f'-f {CGAAL_EXAMPLES_DIR}{row["formula"]} '
                        f'-m {CGAAL_EXAMPLES_DIR}{row["model"]} '
                        f'--threads {threads} '
                        f'{SEARCH_STRATEGY_ARG} {"" if SEARCH_STRATEGY == "global" else SEARCH_STRATEGY} '
                        f'--quiet"',
                        shell=True, check=True, capture_output=True, text=True)
                    end_time = time.perf_counter()
                    max_mem_after = getrusage(RUSAGE_CHILDREN).ru_maxrss / 1024

                    # 'name', 'model', 'formula', 'threads', 'time_s', 'memory_MB', 'search_strategy'
                    df.loc[len(df)] = [row['name'], row['model'], row['formula'], threads, end_time - start_time,
                                       max_mem_after - max_mem_before, SEARCH_STRATEGY]


                else:
                    max_mem_before = getrusage(RUSAGE_CHILDREN).ru_maxrss / 1024
                    start_time = time.perf_counter()
                    proc = subprocess.run(
                        f'{ENV} '
                        f'{PRISM_BIN} '
                        f'{PRISM_EXAMPLES_DIR}{row["model"]} '
                        f'{PRISM_EXAMPLES_DIR}{row["formula"]} ',
                        shell=True, check=True, capture_output=True, text=True)
                    end_time = time.perf_counter()
                    max_mem_after = getrusage(RUSAGE_CHILDREN).ru_maxrss / 1024
                    # extract time for model construction and model checking
                    prism_times = [(line.split()[3], timedelta(seconds=float(re.findall(r'[\d\.\d]+', line)[0]))) for
                                   line in
                                   proc.stdout.splitlines() if
                                   line.startswith("Time for model")]
                    # add total time
                    prism_times += [('total reported', sum([t[1] for t in prism_times], timedelta(seconds=0)))]

                    # 'name', 'model', 'formula', 'time_s', 'memory_MB', 'total_reported', construction', 'checking'
                    # add row to df
                    df.loc[len(df)] = [row['name'], row['model'], row['formula'],
                                       end_time - start_time,
                                       max_mem_before - max_mem_after,
                                       prism_times[2][1].total_seconds(),
                                       prism_times[0][1].total_seconds(),
                                       prism_times[1][1].total_seconds()]

            except subprocess.CalledProcessError as e:
                print(f"Failed to start bench. Error: {e}")
                continue

    filename = f'{SUITE.split(".")[0]}-{SEARCH_STRATEGY}-{datetime.now().strftime("%Y-%m-%d_%H-%M")}.csv'

    df.to_csv(filename, index=False)
    print(f"Benchmark {SEARCH_STRATEGY} on {SUITE} done, results written to: " + filename)
