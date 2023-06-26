import subprocess
import argparse
import statistics
from resource import getrusage, RUSAGE_CHILDREN
from timeit import timeit

parser = argparse.ArgumentParser(description="Benchmark a tool.")
parser.add_argument('num', type=int, nargs='?', help="Number of times to run command")
parser.add_argument('command', type=str, nargs=1,
                    help="The command to benchmark, e.g. \"cd ../solver && solv -arg a -foo b -bar z\"")


def bench(args, stats):
    proc = ''.join(args.command)
    try:
        wall_time = timeit(
            stmt=f"subprocess.run('{proc}', shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)",
            setup="import subprocess", number=1)
        stats["wall_time_S"].append(wall_time)
        stats["ru_maxrss_MB"].append(getrusage(RUSAGE_CHILDREN).ru_maxrss / 1024)
        return stats
    except subprocess.CalledProcessError:
        print(f"Failed to bench with args: '{''.join(args.command)}'")
        exit(1)


if __name__ == '__main__':
    args = parser.parse_args()
    print()

    stats = {"wall_time_S": [], "ru_maxrss_MB": []}

    # run once, and then repeat until at least 1 second has passed
    stats = bench(args, stats)
    while sum(stats["wall_time_S"]) < 1:
        stats = bench(args, stats)

    stats["times"] = len(stats["wall_time_S"])
    stats["wall_time_S"] = statistics.mean(stats["wall_time_S"])
    # maxrss for RUSAGE_CHILDREN is the resident set size of the largest child, not the entire process tree - e.g.
    # for multi-threaded CGAAL run, would only represent the thread with the largest memory usage
    stats["ru_maxrss_MB"] = max(stats["ru_maxrss_MB"])
    # flush to ensure stdout is not buffered
    print(f"{stats['wall_time_S']:.6f}, {stats['ru_maxrss_MB']:.6f}, {stats['times']}", flush=True)
