import argparse
import statistics
from resource import getrusage, RUSAGE_CHILDREN
from timeit import timeit

parser = argparse.ArgumentParser(description="Benchmark a tool.")
parser.add_argument('num', type=int, nargs='?', help="Number of times to run command")
parser.add_argument('command', type=str, nargs=1,
                    help="The command to benchmark, e.g. \"cd ../solver && solv -arg a -foo b -bar z\"")


def bench(args):
    proc = ''.join(args.command)
    wall_time = timeit(
        stmt=f"subprocess.run('{proc}', shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)",
        setup="import subprocess", number=1)
    stats = getrusage(RUSAGE_CHILDREN)
    return wall_time, stats.ru_utime, stats.ru_stime, stats.ru_maxrss


if __name__ == '__main__':
    args = parser.parse_args()

    if args.num is not None and args.num > 1:
        stats = {"wall_time": [], "ru_utime": [], "ru_stime": [], "ru_maxrss": []}
        for n in range(0, args.num):
            wall_time, ru_utime, ru_stime, ru_maxrss = bench(args)
            stats["wall_time"].append(wall_time)
            stats["ru_utime"].append(ru_utime)
            stats["ru_stime"].append(ru_stime)
            stats["ru_maxrss"].append(ru_maxrss)

        stats["wall_time"] = statistics.mean(stats["wall_time"])
        stats["ru_utime"] = statistics.mean(stats["ru_utime"]) / args.num # ru_u/stime is accumulative across runs
        stats["ru_stime"] = statistics.mean(stats["ru_stime"]) / args.num
        stats["ru_maxrss"] = max(stats["ru_maxrss"])
        print(f"{stats['wall_time']:.6f},{stats['ru_utime']:.6f},{stats['ru_stime']:.6f},{stats['ru_maxrss']:.6f}")
    else:
        wall_time, ru_utime, ru_stime, ru_maxrss = bench(args)
        print(f"{wall_time:.6f},{ru_utime:.6f},{ru_stime:.6f},{ru_maxrss:.6f}")
    
