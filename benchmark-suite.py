import subprocess

# Thread count combinations to use [1, 2, 4, ... , 32]
THREADS = [pow(2, x) for x in range(0, 6)]
LCGS_PROGRAMS = [{"program_path": "foo", "formula_path": "bar", "model-type": "lcgs"},
                 {"program_path": "foo", "formula_path": "bar", "model-type": "lcgs"}]

# Denote test programs, e.g. 'atl_checker solver --option foo', omit any formula and model arguments here
ENVS = ["ls solver", "ls prism"]

# subprocess.run('python bench-solver.py 3 "cd ../OnTheFlyATL/ && cargo run --package atl-checker --bin atl-checker -- solver --formula benches/lcgs/Mexican_Standoff/Mexican_Standoff_p1_is_alive_till_he_aint.json --model benches/lcgs/Mexican_Standoff/Mexican_Standoff.lcgs --model-type lcgs"', shell=True)
# subprocess.run("ls", shell=True)

for env in ENVS:
    for proc in LCGS_PROGRAMS:
        for thread in THREADS:
            print(f"Running benchmark for env: {env}, program: {proc}, thread count: {thread}")
            subprocess.run(
                f'{env} --model path/to/{proc["program_path"]} --formula path/to/{proc["formula_path"]} --model-type {proc["model-type"]}',
                shell=True)
