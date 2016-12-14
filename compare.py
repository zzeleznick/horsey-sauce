from __future__ import print_function
import random, math
import os, sys
import numpy as np
from copy import deepcopy
from collections import OrderedDict as OD
from collections import Counter, deque

# Internal Modules
from validate_input import validate_file
from _io_utils import parse_run_args, make_weighted_graph, supress_stdout, save_scores, save_path
from _shared import reverse, find_cover, repeat_find_cover, verify_path

def read_best_paths(filename='best.out'):
    with open(filename) as infile:
        lines = infile.readlines()
    covers = OD()
    for idx,line in enumerate(lines, 1):
        paths = []
        for path in line.split(';'):
            subpath = [int(v) for v in path.split()]
            paths.append(subpath)
        print("(%s): Found %s paths" % (idx, len(paths)))
        covers[idx] = paths
    return covers

def compute_score(filename, paths):
    fpath = "final_inputs/%s" % filename
    graph = make_weighted_graph(*validate_file(fpath))
    def calc_score(vertices):
        return len(vertices) * sum(graph[v].value for v in vertices)
    if type(paths[0]) == list:
        score = sum(calc_score(p) for p in paths)
    else:
        score = sum(paths)
    return score

def compute_all_scores():
    covers = read_best_paths()
    scores = OD()
    for filename in os.listdir('final_inputs'):
        idx = int(filename.split('.in')[0])
        paths = covers[idx]
        scores[idx] = compute_score(filename, paths)
    print(scores)
    text ="\n".join("%s, %s" % (t[0], t[1]) for t in scores.items())
    with open('best.csv', 'w') as outfile:
        outfile.write(text)

def main():
    compute_all_scores()

if __name__ == '__main__':
    main()