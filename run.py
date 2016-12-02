from __future__ import print_function
import subprocess

start = 1
end = 100

for i in range(start, end):
    args = ["python", "sets.py", "-f", "%s.in" % i ]
    print("Running %s" % args)
    subprocess.check_call(args)
