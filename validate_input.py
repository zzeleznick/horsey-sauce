from __future__ import print_function
import os, sys
import argparse
from collections import OrderedDict as OD

DATA_DIR = "data"
ERROR_DIR = "error"

class ExtraSpaces(Exception):
     def __init__(self, *args, **kws):
         super(ExtraSpaces, self).__init__(*args, **kws)

class TooManyHorses(Exception):
     def __init__(self, *args, **kws):
         super(TooManyHorses, self).__init__(*args, **kws)

class CountMismatch(Exception):
     def __init__(self, *args, **kws):
         super(CountMismatch, self).__init__(*args, **kws)

class InvalidPerformanceRating(Exception):
     def __init__(self, *args, **kws):
         super(InvalidPerformanceRating, self).__init__(*args, **kws)

class InvalidEdge(Exception):
     def __init__(self, *args, **kws):
         super(InvalidEdge, self).__init__(*args, **kws)

def parse_args():
    parser = argparse.ArgumentParser(add_help=True, description="Validate Input")
    parser.add_argument('-f', '--filename', type=str, help='filename to validate')
    parser.add_argument('-e', '--error', action="store_true", help='example error files to validate')
    return parser.parse_args()

def validate_file(filename):
    with open(filename) as infile:
        text = infile.read().split('\n')
    idx = 0
    results = OD()
    perfs = OD()
    try:
        if text[0] != text[0].strip():
            print("Found extra spaces on line 0")
            # raise(ExtraSpaces("Found extra spaces on line 0"))
        horses = int(text[0])
        if horses > 500:
            raise(TooManyHorses("%s horses is too damn high" % horses))
        for (idx, line) in enumerate(text[1:], 0):
            if idx == horses:
                break
            line = line.strip() # a la sample1.in
            values = [int(val) for val in line.split(" ")]
            if len(values) != horses:
                raise(CountMismatch("Expected %s not %s" % (horses, len(values))))
            results[idx] = []
            for (i,val) in enumerate(values, 0):
                if i == idx:
                    perfs[idx] = val
                    if val < 0 or val > 99:
                        raise(InvalidPerformanceRating("Invalid Performance %s" % (val) ))
                elif not (val == 0 or val == 1):
                    raise(InvalidEdge("Invalid Edge %s" % (val) ))
                elif val:
                    results[idx].append(i)

    except Exception as e:
        print("ERROR [%s] (Line: %s): %s" % (filename, idx+1, e))
    else:
        print("VALID [%s]" % filename)
    return (results, perfs)

def main():
    args = parse_args()
    test = args.error
    filename = args.filename
    if test:
        print("Will show all example error input files in error directory")
        filenames = [ os.path.join(ERROR_DIR, f) for f in os.listdir(ERROR_DIR) if f.endswith(".in") ]
        for filename in filenames:
            validate_file(filename)
    elif not filename:
        print("Will check all input files in data directory")
        filenames = [ os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR) if f.endswith(".in") ]
        for filename in filenames:
            validate_file(filename)
    else:
        validate_file(filename)

if __name__ == '__main__':
    main()

