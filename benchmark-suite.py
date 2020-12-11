import subprocess
import os

# Thread count combinations to use [1, 2, 4, ... , 32]
THREADS = [pow(2, x) for x in range(0, 6)]

ATL_SOLVER_PATH = "/some/path/atl-solver --option --"
ATL_SOLVER_PROGRAMS = [{"program_path": "foo", "formula_path": "bar", "model-type": "lcgs"},
                       {"program_path": "foo", "formula_path": "bar", "model-type": "lcgs"}]

PRISM_PATH = "/some/path/prism-games --option --"
PRISM_PROGRAMS = [{"program_path": "foo", "formula_path": "bar", "model-type": "lcgs"},
                  {"program_path": "foo", "formula_path": "bar", "model-type": "lcgs"}]


# make logdir
os.makedirs("logs", exist_ok=True)

# setup for atl_solver
for proc in ATL_SOLVER_PROGRAMS:
    for thread in THREADS:
        print(f"Running benchmark for atl_solver, program: {proc}, thread count: {thread}")
        with open(f"logs/{proc['program_path']}-{proc['formula_path']}-{thread}_threads.txt", "w+") as f:
            subprocess.run(
                f' --model path/to/{proc["program_path"]} --formula path/to/{proc["formula_path"]} --model-type {proc["model-type"]}',
                stdout=f, shell=True)

# setup for prism
for proc in PRISM_PROGRAMS:
    for thread in THREADS:
        print(f"Running benchmark for prism, program: {proc}, thread count: {thread}")
        with open(f"logs/{proc['program_path']}-{proc['formula_path']}-{thread}_threads.txt", "w+") as f:
            subprocess.run(
                f'prism-binary --model path/to/{proc["program_path"]} --formula path/to/{proc["formula_path"]}',
                stdout=f, shell=True)
