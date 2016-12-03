from __future__ import print_function
import subprocess
import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(add_help=True, description="Run algorithm on graph inputs")
    parser.add_argument('-s', '--start', type=int, default=1, help='start index to run')
    parser.add_argument('-e', '--end', type=int, default=601, help='end index to run')
    parser.add_argument('-r', '--reps', type=int, default=20, help='number of trials')
    parser.add_argument('-d', '--dfs', action='store_true', help='uses non-default dfs')
    parser.add_argument('-g', '--gather', action='store_true', help='gather runs into submission')
    return parser.parse_args()

def main():
    args = parse_args()
    start = args.start # if args.start else start
    end = args.end # if args.end else end
    reps = args.reps
    if args.gather:
        target = "output"
        name = "_seeds.txt"
        with open(os.path.join(target, name)) as f:
            lines = f.readlines()
        for (idx, line) in enumerate(lines, 1):
            if idx < start or idx >= end:
                continue
            seed = line.split(",")[-1].strip()
            if int(seed) == -1:
                print("%s: No seed found" % idx)
                continue
            method = line.split(",")[1].strip()
            program = "dfs.py" if method == 'D' else "sets.py"
            fname = "%s.in" % str(idx).zfill(4)
            args = ["python", program, "-f", fname, "-s", seed]
            print("Running %s" % args)
            subprocess.check_call(args)
    else:
        program = "sets.py" if not args.dfs else "dfs.py"
        for i in range(start, end):
            args = ["python", program, "-f", "%s.in" % str(i).zfill(4), "-r", str(reps)]
            print("Running %s" % args)
            subprocess.check_call(args)

if __name__ == '__main__':
    main()
