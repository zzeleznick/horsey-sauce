from __future__ import print_function
import subprocess
import os

start = 1
end = 10

for i in range(start, end):
    args = ["python", "sets.py", "-f", "%s.in" % str(i).zfill(4) ]
    print("Running %s" % args)
    subprocess.check_call(args)
