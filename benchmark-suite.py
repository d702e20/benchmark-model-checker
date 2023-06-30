import os
import subprocess
from datetime import datetime
import pandas as pd

# VARIABLES
SUITE = "criterion-suite.csv"
SEARCH_STRATEGY = "lps"
SUBCMD = SEARCH_STRATEGY if SEARCH_STRATEGY == "global" else "solver"
SEARCH_STRATEGY_ARG = "" if SEARCH_STRATEGY == "global" else "--search-strategy"


def strip(text):
    try:
        return text.strip()
    except AttributeError:
        return text


# Thread count combinations to use [1, 2, 4, ... , 32]
THREADS = [pow(2, x) for x in range(0, 6)]

CGAAL_DIR = "../cgaal/"
CGAAL_EXAMPLES_DIR = "../cgaal/lcgs-examples/"
CGAAL_BIN = "../cgaal/target/release/atl-checker-cli"

# compile solver if not already done (requires that 'cargo' is in PATH of shell which is running this script)
# subprocess.run(f"cd {CGAAL_DIR} && cargo build --release", stdout=subprocess.PIPE, shell=True)

# setup dataframe to store results
df = pd.DataFrame(columns=['name', 'model', 'formula', 'threads', 'time_s', 'memory_MB', 'runs'])

# read in suite from csv
suite = pd.read_csv(SUITE, skipinitialspace=True, converters={'name': strip, 'model': strip, 'formula': strip})

error = False
for i, test in suite.iterrows():
    try:
        os.stat(CGAAL_EXAMPLES_DIR + test['model'])
    except FileNotFoundError:
        error = True
        print(f"ERROR: Could not find '{test['model']}' in '{CGAAL_EXAMPLES_DIR}'.")

    try:
        os.stat(CGAAL_EXAMPLES_DIR + test['formula'])
    except FileNotFoundError:
        error = True
        print(f"ERROR: Could not find '{test['formula']}' in '{CGAAL_EXAMPLES_DIR}'.")

if error:
    print(f"Please fix the above errors in {SUITE}.")
    exit(1)

# benchmark each program in suite
for index, row in suite.iterrows():
    for threads in THREADS:
        print(f"{row['name']}/{threads} with model: '{row['model']}' and formula: '{row['formula']}'")
        try:
            proc = subprocess.run(
                f'python3 bench-solver.py "'
                f'{CGAAL_BIN} {SUBCMD} '
                f'-f {CGAAL_EXAMPLES_DIR}{row["formula"]} '
                f'-m {CGAAL_EXAMPLES_DIR}{row["model"]} '
                f'--threads {threads} '
                f'{SEARCH_STRATEGY_ARG} {"" if SEARCH_STRATEGY == "global" else SEARCH_STRATEGY} '
                f'--quiet"',
                shell=True, check=True, capture_output=True, text=True)
            out = [e.strip() for e in proc.stdout.split(',')]
            # add row to df
            df.loc[len(df)] = [row['name'], row['model'], row['formula'], threads, out[0], out[1], out[2]]

            print(proc.stdout.strip())
        except subprocess.CalledProcessError as e:
            print(f"Failed to start bench. Error: {e}")
            continue

filename = f'{SUITE.split(".")[0]}-{SEARCH_STRATEGY}-{datetime.now().strftime("%Y-%m-%d_%H-%M")}.csv'

df.to_csv(filename, index=False)
print("Benchmark done, results written to: " + filename)
