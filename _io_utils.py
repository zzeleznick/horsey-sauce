from __future__ import print_function
import os, sys
import random
import argparse
from copy import deepcopy
from collections import OrderedDict as OD

# Internal Modules
from validate_input import validate_file

DATA_DIR = "data"

target = os.path.expanduser("~/cs170")
sys.path.append(target)

from Graph import *

def make_graph(edges, perfs):
    custom_labels = OD()
    for (k,v) in perfs.iteritems():
        custom_labels[k] = "%s_%s" % (k,v)
    return Graph(edges, custom_labels)

def make_weighted_graph(edges, perfs):
    g = make_graph(edges, perfs)
    for (k,v) in perfs.iteritems():
        g[k].value = v
    return g

def convert(graph, perfs=None):
    size = len(graph.vertices)
    lines = ["%s" % size]
    for (idx, v) in enumerate(graph.vertices.itervalues()):
        row = []
        for i in range(size):
            if i in v.edges:
                row.append(1)
            elif i == idx:
                if perfs:
                    row.append(perfs[idx])
                else:
                    row.append(graph[idx].value)
            else:
                row.append(0)
        lines.append(" ".join("%s" % val for val in row))
    return "\n".join(lines)

def save_repr(graph, outname):
    text = convert(graph)
    with open(outname, "w") as outfile:
        outfile.write(text)

def save_scores(scores, outname):
    pairs = sorted(zip(scores, range(len(scores))))
    text = "\n".join("%s, %s" % (t[0], t[1]) for t in pairs)
    with open(outname, "w") as outfile:
        outfile.write(text)

def save_path(res, outname):
    paths = [ list(path) for (score, path) in res.itervalues() ]
    lengths = [ len(path) for path in paths ]
    scores = [ score for (score, path) in res.itervalues() ]
    total = sum(scores)
    l1 = "Paths: %s, Score: %s" % (len(res), total)
    l2 = "Vertex Max: %s | Total: %s" % (max(lengths), sum(lengths))
    body = "\n".join("%s: %s" % (score, path) for (score, path) in zip(scores, paths))
    text = "\n".join([l1, l2, body])
    with open(outname, "w") as outfile:
        outfile.write(text)

def make_datafile(size=20):
    random.seed(10)
    perfs = [random.randint(0,99) for i in range(size)]
    g = Graph.generate(v=size, e=int(size**1.25))
    text = convert(g, perfs)
    print(text)
    location = os.path.join(DATA_DIR, "generated1.in")
    with open(location, "w") as outfile:
        outfile.write(text)

def supress_stdout(func):
    class DummyFile(object):
        def write(self, x): pass
    def wrapper(*args, **kwargs):
        save_stdout = sys.stdout
        sys.stdout = DummyFile()
        res = func(*args, **kwargs)
        sys.stdout = save_stdout
        return res
    return wrapper

def parse_run_args():
    parser = argparse.ArgumentParser(add_help=True, description="Run algorithm against graph input")
    parser.add_argument('-f', '--filename', type=str, help='filename to run')
    return parser.parse_args()

def main():
    # filename = "data/sample2.in"
    filename = "data/generated1.in"
    edges, perfs = validate_file(filename)
    graph = make_graph(edges, perfs)
    graph.display()

if __name__ == '__main__':
    make_datafile()
    main()


