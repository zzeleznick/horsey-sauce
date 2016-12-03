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

MAX_SAMPLES = 22

def get_sample_size(graph, max_samples=MAX_SAMPLES):
    edges = graph.edgelist
    vertices = graph.vertices
    ratio = float(len(edges))/len(vertices)
    # float(len(edges))/len(keys) * math.log(len(keys)**.55)
    sample_size = int(min(max((ratio, len(vertices))), max_samples, len(edges)))
    print(len(vertices), len(edges), sample_size)
    return sample_size

def find_sets(graph):
    edges = [ pair for (pair, w) in graph.edgelist ]
    vertices = graph.vertices.keys()
    if not edges:
        return [ random.choice(vertices) ]
    paths = OD()
    sample_size = get_sample_size(graph)
    # print(edges)
    def calc_score(vertices):
        return len(vertices) * sum(graph[v].value for v in vertices)
    starter_edges = [edges[k] for k in random.sample(xrange(len(edges)), sample_size) ]
    paths[0] = [(calc_score(pair), OD(((pair[0], True), (pair[1], True)))) for pair in starter_edges ]
    """
    weights = np.array([float(score+1) for (score, p) in  paths[0]])
    total = np.sum(weights)
    weights /= total
    idx = np.random.choice(np.arange(len(starter_edges)), p=weights)
    s,p = paths[0][idx]
    """
    s,p = random.choice(paths[0])
    best_score = s
    best_path = p.keys()
    print("Intialized best path to %s" % best_path)
    verify_path(graph, best_path)
    if 0.99 > random.random():
        best_path = dfs_extend(graph, best_path)
    if 0.99 > random.random():
        best_path = prefix_extend(graph, best_path)
    return best_path

def dfs_extend(graph, path):
    revgraph = reverse(graph)
    mod_path = OD(zip(path, [True]*len(path)))
    last, val = mod_path.popitem()
    mod_path[last] = True
    edges = graph[last].edges
    choices = [e for e in edges if e not in mod_path ]
    while choices:
        # """
        weights = np.array([np.e ** -float(len(graph[e].edges)) for e in choices]) + \
                  np.array([np.e ** -float(len(revgraph[e].edges)) for e in choices])
        total = np.sum(weights)
        if total <= 0:
            break
        weights /= total
        last = np.random.choice(choices, p=weights)
        # """
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
        # """
        weights = np.array([np.e ** -float(len(graph[e].edges)) for e in choices]) + \
                  np.array([np.e ** -float(len(revgraph[e].edges)) for e in choices])
        total = np.sum(weights)
        if total <= 0:
            break
        weights /= total
        first = np.random.choice(choices, p=weights)
        # """
        # first = random.choice(choices)
        visited[first] = True
        prefix.appendleft(first)
        edges = revgraph[first].edges
        choices = [e for e in edges if e not in visited ]
    print("Extended path of %s with prefix %s" % (len(path), len(prefix)))
    prefix.extend(path)
    print("New Path:", prefix)
    verify_path(graph, prefix)
    return prefix

def find_and_save_path(filename, seed):
    fpath = "final_inputs/%s" % filename
    graph = make_weighted_graph(*validate_file(fpath))
    random.seed(seed)
    # REQUIRED for DFS!
    np.random.seed(seed)
    caller = supress_stdout(find_cover)
    res = caller(deepcopy(graph), find_sets)
    outname = "paths/%s_%s_dfs.txt" % (filename.replace(".in", ""), str(seed).zfill(4))
    save_path(res, outname)

def gen_scores(filename, r=20):
    fpath = "final_inputs/%s" % filename
    graph = make_weighted_graph(*validate_file(fpath))
    scores = repeat_find_cover(graph, find_sets, r)
    outname = "output/%s_dfs.txt" % filename.split(".in")[0]
    save_scores(scores, outname)

def main():
    args = parse_run_args()
    filename = args.filename if args.filename else "1.in"
    reps = args.reps
    if args.seed == None:
        gen_scores(filename, reps)
    else:
        find_and_save_path(filename, args.seed)

if __name__ == '__main__':
    main()

