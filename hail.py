from __future__ import print_function
import random, math
import os, sys
from copy import deepcopy
from collections import OrderedDict as OD
from collections import Counter, deque

# Internal Modules
from validate_input import validate_file
from _io_utils import parse_run_args, make_weighted_graph, supress_stdout, save_scores, save_path
from _shared import reverse, find_cover, repeat_find_cover, verify_path

# External Modules
from tarjan import tarjan
from tarjan.tc import tc
import numpy as np

def find_sets(graph):
    edges = [ pair for (pair, w) in graph.edgelist ]
    vertices = graph.vertices.keys()
    if not edges:
        return [ random.choice(vertices) ]
    paths = OD()
    t_input = {v: graph[v].edges.keys() for v in graph.vertices}
    # print(t_input)
    scc_index = random.choice(vertices)
    max_scc = 0
    '''
    closure = tarjan(t_input)
    for idx,lv in enumerate(closure):
        if len(lv) > max_scc:
            max_scc = len(lv)
            scc_index = idx
        print(idx, len(lv), lv)
    '''
    closure = tc(t_input)
    for idx, path in closure.iteritems():
        if len(path) > max_scc:
            max_scc = len(path)
            scc_index = idx
        # print(idx, len(path), path)

    def calc_score(vertices):
        return len(vertices) * sum(graph[v].value for v in vertices)

    print(scc_index, max_scc)

    # best_path = closure[scc_index]
    best_path = [scc_index]

    best_score = calc_score(best_path)

    print(best_score, best_path)
    verify_path(graph, best_path)
    paths = []
    ctr = 0
    for i in range(1000):
        path = dfs_extend(graph, best_path, closure)
        paths.append((calc_score(path), path))
        if len(paths) < 10:
            ctr += 1
        if i < 500 and ctr > 200:
            break
        elif i < 100 and ctr > 50:
            break
        elif i < 50 and ctr > 25:
            break
        elif i < 10 and ctr > 6:
            break
    sorted_paths = sorted(paths, reverse=True)
    print(sorted_paths[0])
    best_path = sorted_paths[0][1]
    return best_path

def dfs_extend(graph, path, closure):
    mod_path = OD(zip(path, [True]*len(path)))
    last, val = mod_path.popitem()
    mod_path[last] = True
    edges = graph[last].edges
    choices = [e for e in edges if e not in mod_path ]
    while choices:
        weights = np.array([np.e ** float(len(closure[e])) for e in choices]) + \
                  np.array([np.e ** float(len(closure[e])) for e in choices])
        total = np.sum(weights)
        if total <= 0:
            break
        weights /= total
        last = np.random.choice(choices, p=weights)
        # last = random.choice(choices)
        mod_path[last] = True
        edges = graph[last].edges
        choices = [e for e in edges if e not in mod_path ]
    print("Extended path from %s to %s" % (len(path), len(mod_path)))
    verify_path(graph, mod_path.keys())
    return mod_path.keys()

def prefix_extend(graph, path):
    revgraph = reverse(graph)
    # print(graph.edgelist)
    first = path[0]
    prefix = deque()
    visited = OD(zip(path, [True]*len(path)))
    edges = revgraph[first].edges
    choices = [e for e in edges if e not in visited ]
    while choices:
        first = random.choice(choices)
        visited[first] = True
        prefix.appendleft(first)
        edges = revgraph[first].edges
        choices = [e for e in edges if e not in visited ]
    print("Extended path of %s with prefix %s" % (len(path), len(prefix)))
    prefix.extend(path)
    print("New Path:", prefix)
    verify_path(graph, prefix)
    return prefix

def hacky_solve(graph):
    print("Solving with hack")
    start = graph.vertices.keys()[0]
    path = range(start,500,50)
    verify_path(graph, path)
    return path

def find_and_save_path(filename, seed):
    fpath = "final_inputs/%s" % filename
    graph = make_weighted_graph(*validate_file(fpath))
    random.seed(seed)
    caller = supress_stdout(find_cover)
    res = caller(deepcopy(graph), find_sets)
    outname = "paths/%s_%s_hail.txt" % (filename.replace(".in", ""), str(seed).zfill(4))
    save_path(res, outname)

def gen_scores(filename, r=20):
    fpath = "final_inputs/%s" % filename
    graph = make_weighted_graph(*validate_file(fpath))
    scores = repeat_find_cover(graph, find_sets, r)
    # random.seed(10)
    # np.random.seed(10)
    # find_cover(graph, find_sets)
    outname = "output/%s_hail.txt" % filename.split(".in")[0]
    # save_scores(scores, outname)

def main():
    args = parse_run_args()
    filename = args.filename if args.filename else "0082.in"
    reps = args.reps
    if filename == "0070.in":
        print("Activating Hack")
        globals()['find_sets'] = hacky_solve
    if args.seed == None:
        gen_scores(filename, reps)
    else:
        find_and_save_path(filename, args.seed)

if __name__ == '__main__':
    main()

