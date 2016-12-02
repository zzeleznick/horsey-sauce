from __future__ import print_function
import random, math
import os, sys
import numpy as np
from copy import deepcopy
from collections import OrderedDict as OD
from collections import Counter, deque

# Internal Modules
from validate_input import validate_file
from _io_utils import make_weighted_graph, supress_stdout, save_scores, save_path
from _shared import reverse, find_cover, repeat_find_cover, verify_path

def get_sample_size(graph):
    edges = graph.edgelist
    vertices = graph.vertices
    ratio = float(len(edges))/len(vertices)
    # float(len(edges))/len(keys) * math.log(len(keys)**.55)
    sample_size = int(min(max((ratio, len(vertices))), 20, len(edges)))
    print(len(vertices), len(edges), sample_size)
    return sample_size

def check_compat(p1, p2):
    for k in p1:
        if p2.get(k):
            return False
    return True


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
    s,p = random.choice(paths[0])
    best_score = s
    best_path = p.keys()
    print("Intialized best path to %s" % best_path)
    for i in range(1, len(graph.vertices)):
        print("Iteration %s" % i)
        if not paths[i-1]:
            break
        # sample_size = get_sample_size(graph, min(MAX_SAMPLES*5, max(MAX_SAMPLES, MAX_SAMPLES*5-len(paths[i-1]))))
        starter_verts = [vertices[k] for k in random.sample(xrange(len(vertices)), sample_size) ]
        paths[i] = []
        # maybe check if some paths can be joined
        for score, path in paths[i-1]:
            next_path = deepcopy(path)
            first = next_path.keys()[0]
            last, val = next_path.popitem()
            next_path[last] = val
            for v in starter_verts:
                if graph[last].get(v) and v not in next_path:
                    alt_path = deepcopy(next_path)
                    alt_path[v] = True
                    next_score = calc_score(alt_path.keys())
                    paths[i].append((next_score, deepcopy(alt_path)))
                    if next_score >= best_score:
                        update_prob = min(.99, 0.20 + math.log(float(next_score+1)/(best_score+1)))
                        if update_prob > random.random():
                            best_score = next_score
                            best_path = alt_path.keys()
            else:
                alt_path = deepcopy(next_path)
                alt_path.popitem()
                next_score = calc_score(alt_path.keys())
                update_prob = min(.99, 0.25 + math.log(float(next_score+1)/(best_score+1)))
                if update_prob > random.random() and alt_path:
                    paths[i].append((next_score, deepcopy(alt_path)))

            # ~ max of 20 hail-maries
            # E(X) = 20; |X|*P(x) = 20
            '''
            update_prob = min(.5, 20*(1.0/(len(paths[i-1]))**2))
            if update_prob > random.random():
                if 0.5 > random.random():
                    xx = dfs_extend(graph, next_path.keys())
                else:
                    xx = prefix_extend(graph, next_path.keys())
                if len(xx) != next_path.keys():
                    # yy = OD(zip(xx, [True]*len(xx)))
                    ns = calc_score(xx)
                    if ns >= best_score:
                        best_score = ns
                        best_path = xx
            '''
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

def find_and_save_path(name, seed):
    edges, perfs = validate_file(name)
    graph = make_weighted_graph(edges, perfs)
    caller = supress_stdout(find_cover)
    random.seed(seed)
    res = caller(deepcopy(graph), find_sets)
    outname = "%s_path_%s.txt" % (name.replace(".in", ""), str(seed).zfill(4))
    save_path(res, outname)

def main():
    # filename =  "generated1.in" # "sample3.in" # "generated3.in"
    # path = "data/%s" % filename
    # filename =  "02_01_00.in" #"3.in" #"0037.in"
    # path = "proposals/%s" % filename
    filename =  "1.in" #"3.in" #"0037.in"
    path = "final_inputs/%s" % filename
    # """
    edges, perfs = validate_file(path)
    graph = make_weighted_graph(edges, perfs)
    scores = repeat_find_cover(graph, find_sets, 20)
    # outname = "%s.txt" % path.split(".in")[0]
    # save_scores(scores, outname)
    # """
    # find_and_save_path(path, 4)

if __name__ == '__main__':
    main()

