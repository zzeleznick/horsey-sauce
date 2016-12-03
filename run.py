from __future__ import print_function
import subprocess
import os
import argparse

start = 341
end = 361

def parse_args():
    parser = argparse.ArgumentParser(add_help=True, description="Run algorithm on graph inputs")
    parser.add_argument('-s', '--start', type=int, help='start index to run')
    parser.add_argument('-e', '--end', type=int, help='end index to run')
    parser.add_argument('-g', '--gather', action='store_true', help='gather runs into submission')
    return parser.parse_args()

def main():
    args = parse_args()
    if args.gather:
        target = "output"
        name = "_seeds.txt"
        with open(os.path.join(target, name)) as f:
            lines = f.readlines()
            for (idx, line) in enumerate(lines, 1):
                seed = line.split(",")[-1].strip()
                if int(seed) == -1:
                    print("%s: No seed found" % idx)
                    continue
                fname = "%s.in" % str(idx).zfill(4)
                args = ["python", "sets.py", "-f", fname, "-s", seed]
                print("Running %s" % args)
                subprocess.check_call(args)
    else:
        start = args.start if args.start else start
        end =  args.end if args.end else end
        for i in range(start, end):
            args = ["python", "sets.py", "-f", "%s.in" % str(i).zfill(4) ]
            print("Running %s" % args)
            subprocess.check_call(args)

if __name__ == '__main__':
    main()
