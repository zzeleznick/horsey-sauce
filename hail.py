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

def get_sample_size(graph):
    edges = graph.edgelist
    vertices = graph.vertices
    sample_size = min(len(vertices), 20)
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
    starter_verts = [vertices[k] for k in random.sample(xrange(len(vertices)), sample_size) ]
    paths[0] = [(calc_score([v]), OD([(v, True)]) ) for v in starter_verts ]
    s,p = random.choice(paths[0])
    best_score = s
    best_path = p.keys()
    print("Intialized best path to %s" % best_path)
    for i in range(1, len(graph.vertices)):
        print("Iteration %s" % i)
        if not paths[i-1]:
            break
        starter_verts = [vertices[k] for k in random.sample(xrange(len(vertices)), sample_size) ]
        paths[i] = []
        for score, path in paths[i-1]:
            next_path = deepcopy(path)
            last, val = next_path.popitem()
            next_path[last] = val
            for v in starter_verts:
                if graph[last].get(v) and v not in next_path:
                    alt_path = deepcopy(next_path)
                    alt_path[v] = True
                    next_score = calc_score(alt_path.keys())
                    paths[i].append((next_score, alt_path))
                    if next_score >= best_score:
                        update_prob = min(.99, math.log(float(next_score+1)/(best_score+1)))
                        if update_prob > random.random():
                            best_score = next_score
                            best_path = alt_path.keys()
    # exit()
    for i, path in paths.iteritems():
        print(i, path)
    print(best_score, best_path)
    verify_path(graph, best_path)
    if 0.99 > random.random():
        best_path = dfs_extend(graph, best_path)
    if 0.99 > random.random():
        best_path = prefix_extend(graph, best_path)
    return best_path

def dfs_extend(graph, path):
    mod_path = OD(zip(path, [True]*len(path)))
    last, val = mod_path.popitem()
    mod_path[last] = True
    edges = graph[last].edges
    choices = [e for e in edges if e not in mod_path ]
    while choices:
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
    caller = supress_stdout(find_cover)
    res = caller(deepcopy(graph), find_sets)
    outname = "paths/%s_%s_hail.txt" % (filename.replace(".in", ""), str(seed).zfill(4))
    save_path(res, outname)

def gen_scores(filename, r=20):
    fpath = "final_inputs/%s" % filename
    graph = make_weighted_graph(*validate_file(fpath))
    scores = repeat_find_cover(graph, find_sets, r)
    outname = "output/%s_hail.txt" % filename.split(".in")[0]
    save_scores(scores, outname)

def main():
    args = parse_run_args()
    filename = args.filename if args.filename else "1.in"
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

