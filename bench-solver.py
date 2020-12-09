import argparse
from resource import getrusage, RUSAGE_CHILDREN
from timeit import timeit

parser = argparse.ArgumentParser(description="Benchmark a tool.")
parser.add_argument('command', type=str, nargs='*',
                    help="The command to benchmark, e.g. \"cd ../solver && solv -arg a -foo b -bar z\"")
parser.add_argument('num', type=int, nargs='?', help="Number of times to run command")


def bench(args):
    proc = ''.join(args.command)
    print("Running: " + proc)
    wall_time = timeit(
        stmt=f"subprocess.run('{proc}', shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)",
        setup="import subprocess", number=1)
    stats = getrusage(RUSAGE_CHILDREN)
    print(f"wall time: {wall_time}, usertime: {stats.ru_utime}, systime: {stats.ru_stime}, peak {stats.ru_maxrss} KiB")
    return wall_time, stats.ru_utime, stats.ru_stime, stats.ru_maxrss


if __name__ == '__main__':
    args = parser.parse_args()
    # args.command = "cargo run --package atl-checker --bin atl-checker -- solver --formula benches/lcgs/Mexican_Standoff/Mexican_Standoff_p1_is_alive_till_he_aint.json --model benches/lcgs/Mexican_Standoff/Mexican_Standoff.lcgs --model-type lcgs"
    bench(args)
