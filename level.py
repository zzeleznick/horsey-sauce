from __future__ import print_function
import random, math
import os, sys
from copy import deepcopy
from collections import OrderedDict as OD
from collections import Counter, deque
from heapq import *
# Internal Modules
from validate_input import validate_file
from _io_utils import parse_run_args, make_weighted_graph, supress_stdout, save_scores, save_path
from _shared import reverse, find_cover, repeat_find_cover, verify_path

# External Modules
from tarjan import tarjan
from tarjan.tc import tc
import numpy as np
'''
Heap with shuffled vertices and level 1
Dict of visited vertices (explored), and highest level
Heap acts as the fringe
Add all vertices to the heap with path distances as values
Only add children if we haven't already popped it
once the heap is empty, we want to construct a path from the highest vertex
'''
def find_sets(graph):
    edges = [ pair for (pair, w) in graph.edgelist ]
    vertices = graph.vertices.keys()
    if not edges:
        return [ random.choice(vertices) ]
    def calc_score(vertices):
        return len(vertices) * sum(graph[v].value for v in vertices)

    visited = OD()

    t_input = {v: graph[v].edges.keys() for v in graph.vertices}
    scc_index = random.choice(vertices)
    max_scc = 0
    closure = tc(t_input)
    for idx, path in closure.iteritems():
        if len(path) > max_scc:
            max_scc = len(path)
            scc_index = idx

    best_path = [scc_index]
    '''
    h = [ (1,v) for v in vertices ]
    random.shuffle(h)
    '''
    h = [(1, scc_index)]

    levels = OD()
    levels[1] = OD(zip([t[1] for t in h], ['NULL']*len(h)))
    heapify(h)

    best_path = [random.choice(vertices)]
    best_score = calc_score(best_path)
    i = 0
    while h:
        print("Iteration %s" % i)
        i += 1
        lv, node = heappop(h)
        nxt = abs(lv)+1
        if node in visited:
            continue
        visited[node] = True
        children = graph[node].edges.keys()
        random.shuffle(children)
        for child in children:
            if not levels.get(nxt):
                levels[nxt] = OD([(child, node)])
            else:
                levels[nxt][child] = node
            if child not in visited:
                heappush(h, (-nxt, child))

    for (k,v) in levels.iteritems():
        print(k,v)

    depth = max(levels.keys())
    start = random.choice(levels[depth].keys())
    prev = levels[depth][start]
    path = OD([(start, True)])
    print("Backtracking")
    for j in range(depth-1, 0, -1):
        print(j, prev, path.keys())
        if prev != 'NULL':
            if prev in path:
                print("ERROR: Prev in path")
            if prev == path.keys()[0]:
                path.popitem(last=False)
            # print("Adding %s to %s" % (prev, path.keys()))
            path[prev] = True
        else:
            break
        prev = levels[j][prev]

    best_path = [k for k in reversed(path.keys())]
    best_score = calc_score(best_path)

    print(best_score, best_path)
    verify_path(graph, best_path)

    if 0.99 > random.random():
        best_path = dfs_extend(graph, best_path, closure)
    if 0.99 > random.random():
        best_path = prefix_extend(graph, best_path)
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
        if random.random() > 0.5:
            last = random.choice(choices)
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
    # REQUIRED for DFS!
    np.random.seed(seed)
    caller = supress_stdout(find_cover)
    res = caller(deepcopy(graph), find_sets)
    outname = "paths/%s_%s_level.txt" % (filename.replace(".in", ""), str(seed).zfill(4))
    save_path(res, outname)

def gen_scores(filename, r=20):
    fpath = "final_inputs/%s" % filename
    graph = make_weighted_graph(*validate_file(fpath))
    # random.seed(10)
    # find_sets(graph)
    scores = repeat_find_cover(graph, find_sets, r)
    outname = "output/%s_level.txt" % filename.split(".in")[0]
    save_scores(scores, outname)

def main():
    args = parse_run_args()
    filename = args.filename if args.filename else "0026.in"
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
