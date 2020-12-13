import subprocess
import os

# Thread count combinations to use [1, 2, 4, ... , 32]
THREADS = [pow(2, x) for x in range(0, 6)]
# Setup programs and examples to benchmark
ATL_SOLVER_PATH = "cd ../OnTheFlyATL && cargo run --package atl-checker --bin atl-checker -- solver"
ATL_SOLVER_PROGRAMS = [{"model": "foo", "formula": "bar"},
                       {"model": "foo", "formula": "bar"}]

PRISM_PATH = "/some/path/prism-games --option --"
PRISM_PROGRAMS_PATH = "some/path"
PRISM_PROGRAMS = [{"model": "foo", "formula": "bar"},
                  {"model": "foo", "formula": "bar"}]

ATL_SOLVER_PROGRAMS_PATH = "docs/lcgs/working-examples/Mexican_Standoff_bigg"
ATL_SOLVER_PROGRAMS = [
    {"model": "Mexican_standoff_6.lcgs", "formula": "Mexican_Standoff_p1_is_alive_till_he_aint.json"},
    {"model": "Mexican_standoff_7.lcgs", "formula": "Mexican_Standoff_p1_is_alive_till_he_aint.json"}]

# make logdir
os.makedirs("logs", exist_ok=True)

# setup for atl_solver
for proc in ATL_SOLVER_PROGRAMS:
    for threads in THREADS:
        print(f"Running benchmark for atl_solver, program: {proc}, thread count: {threads}")
        # Setup the program to bench, such that the command reads 'python(3) bench-solver.py "program"'
        subprocess.run(
            f'python bench-solver.py \"{ATL_SOLVER_PATH} --model {ATL_SOLVER_PROGRAMS_PATH}/{proc["model"]} --formula '
            f'{ATL_SOLVER_PROGRAMS_PATH}/{proc["formula"]} --model-type lcgs --threads {threads}\"', shell=True)

exit(0)  # FIXME: prism not yet setup
# setup for prism
for proc in PRISM_PROGRAMS:
    for threads in THREADS:
        print(f"Running benchmark for prism, program: {proc}, thread count: {threads}")
        with open(f"logs/{proc['model']}-{proc['formula']}-{threads}_threads.txt", "w+") as f:
            subprocess.run(
                f'prism-binary --model path/to/{proc["model"]} --formula path/to/{proc["formula"]}',
                stdout=f, shell=True)
