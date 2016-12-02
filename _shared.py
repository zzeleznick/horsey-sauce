from __future__ import print_function
import os, sys
import random
from copy import deepcopy
from collections import OrderedDict as OD

try:
    import numpy as np
except ImportError:
    print("No Numpy Installed")


# Internal Modules
from _io_utils import supress_stdout

def reverse(graph):
    rev = deepcopy(graph)
    edges = rev.edgelist
    # delete all previous edges
    rev.remove_all_edges()
    # now add the reversed edges
    for ((u,v), w) in edges:
        rev.add_edge(v, u, w)
    return rev

def find_cover(graph, find_path):
    paths = OD()
    idx = 0
    total = 0
    def calc(vertices):
        return len(vertices) * sum(graph[v].value for v in vertices)
    while graph.vertices:
        print("Cover Iteration %s" % idx)
        path = find_path(graph)
        score = calc(path)
        paths[idx] = (score, path)
        for v in path:
            # print("Removing vertex %s" % v)
            graph.remove_vertex(v)
        idx +=1
        total += score
    print(paths)
    print(total)
    return paths

def repeat_find_cover(graph, find_path, r=100):
    scores = []
    verts = graph.vertices
    edges = graph.edgelist
    print("V: %s, E: %s" % (len(verts), len(edges)))
    limit = len(verts) * sum(graph[v].value for v in (verts))
    for i in range(r):
        caller = supress_stdout(find_cover)
        random.seed(i)
        try:
            np.random.seed(i)
        except Exception:
           pass # no numpy
        res = caller(deepcopy(graph), find_path)
        total = sum(score for (score, path) in res.itervalues())
        print("Score for R-%s: %s" %(i, total))
        scores.append(total)
        if total == limit:
            print("Reached theoretical limit of %s" % limit)
            break
    print(scores)
    try:
        print(np.median(scores), np.mean(scores), np.max(scores))
    except Exception:
        print("Max Score: %s" % max(scores))
    return scores

def verify_path(graph, path):
    for i in range(0, len(path)-1):
        u,v = path[i], path[i+1]
        message = "Edge (%s->%s) missing" % (u,v)
        assert graph[u].get(v) != None, message
    print("Valid Path")
