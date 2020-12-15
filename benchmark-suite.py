import subprocess
import os

# Thread count combinations to use [1, 2, 4, ... , 32]
THREADS = [pow(2, x) for x in range(0, 7)]
THREADS = [1,2,3,4,5,6,7,8,9,10]
# Setup programs and examples to benchmark
ATL_SOLVER_PATH = "~/bench/OnTheFlyATL/target/release/atl-checker solver"
ATL_SOLVER_PROGRAMS_PATH = "~/bench/OnTheFlyATL/docs/lcgs/working-examples/Mexican_Standoff"
ATL_SOLVER_PROGRAMS = [
    {"model": "Mexican_Standoff_3_1hp.lcgs", "formula": "Mexican_Standoff_p1_is_alive_till_he_aint.json"},
    {"model": "Mexican_Standoff_3_2hp.lcgs", "formula": "Mexican_Standoff_p1_is_alive_till_he_aint.json"},
    {"model": "Mexican_Standoff_3_3hp.lcgs", "formula": "Mexican_Standoff_p1_is_alive_till_he_aint.json"},
    {"model": "Mexican_Standoff_4_1hp.lcgs", "formula": "Mexican_Standoff_p1_is_alive_till_he_aint.json"},
    {"model": "Mexican_Standoff_4_2hp.lcgs", "formula": "Mexican_Standoff_p1_is_alive_till_he_aint.json"},
    {"model": "Mexican_Standoff_4_3hp.lcgs", "formula": "Mexican_Standoff_p1_is_alive_till_he_aint.json"},
    {"model": "Mexican_Standoff_5_1hp.lcgs", "formula": "Mexican_Standoff_p1_is_alive_till_he_aint.json"},
    {"model": "Mexican_Standoff_5_2hp.lcgs", "formula": "Mexican_Standoff_p1_is_alive_till_he_aint.json"},
    {"model": "Mexican_Standoff_5_3hp.lcgs", "formula": "Mexican_Standoff_p1_is_alive_till_he_aint.json"}
    ]

PRISM_PATH = "/some/path/prism-games --option --"
PRISM_PROGRAMS_PATH = "some/path"
PRISM_PROGRAMS = [{"model": "foo", "formula": "bar"},
                  {"model": "foo", "formula": "bar"}]


# setup for atl_solver
for proc in ATL_SOLVER_PROGRAMS:
    for threads in THREADS:
        # Setup the program to bench, such that the command reads 'python(3) bench-solver.py "program"'
        model_name = proc['model'].split('_')
        print(f"mexi,{model_name[2]},{model_name[3][:1]},{proc['formula']},{threads}")
        subprocess.run(
            f'python3 ~/bench/bench-solver/bench-solver.py 10 \"{ATL_SOLVER_PATH} --model {ATL_SOLVER_PROGRAMS_PATH}/{proc["model"]} --formula '
            f'{ATL_SOLVER_PROGRAMS_PATH}/{proc["formula"]} --model-type lcgs --threads {threads}\"', shell=True)

exit(0)  # FIXME: prism not yet setup
# setup for prism
for proc in PRISM_PROGRAMS:
    for threads in THREADS:
        print(f"Running benchmark for prism, program: {proc}, thread count: {threads}")
        subprocess.run(
            f'python3 ~/bench/bench-solver/bench-solver.py prism-binary --model path/to/{proc["model"]} --formula path/to/{proc["formula"]}', shell=True)
