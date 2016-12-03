from __future__ import print_function
import os, sys
import re
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
    parser.add_argument('-s', '--seed', type=int, help='random seed and then save')
    return parser.parse_args()

def standardize_input_names():
    target = "final_inputs"
    filenames = [file for file in os.listdir(target) if file.endswith(".in") ]
    mapper = lambda f: (os.path.join(target,f), os.path.join(target, f.split(".in")[0].zfill(4) + ".in" ))
    [os.rename(*mapper(f)) for f in filenames]

def segment_easy_graphs():
    target = "output"
    outname = "_easy.txt"
    is_match = lambda f: re.compile(r'\d*.*\.txt').match(f)
    filenames = [file for file in os.listdir(target) if is_match(file) ]
    expected_size = 20
    easy = []
    for fname in filenames:
        with open(os.path.join(target, fname)) as f:
            for i, l in enumerate(f, 1):
                pass
        if i < expected_size:
            easy.append(fname)
    with open(os.path.join(target, outname), "w") as outfile:
        outfile.write("\n".join(easy))

def segment_targets():
    target = "output"
    outname = "_segments.txt"
    is_match = lambda f: re.compile(r'\d+.*\.txt').match(f)
    filenames = [file for file in os.listdir(target) if is_match(file) ]
    parse = lambda line: int(line.strip().split(',')[0])
    targets = []
    for fname in filenames:
        idx = int(fname.split("_")[0])
        with open(os.path.join(target, fname)) as f:
            lines = f.readlines()
            scores = [ parse(line) for line in lines if line.strip() ]
            delta  = (idx, max(scores) - min(scores))
        targets.append(delta)
    with open(os.path.join(target, outname), "w") as outfile:
        st = sorted(targets, key=lambda x: -x[1])
        outfile.write("\n".join("%s, %s" % (t[0], t[1]) for t in st))

def get_best_seeds():
    target = "output"
    outname = "_seeds.txt"
    is_match = lambda f: re.compile(r'\d+.*\.txt').match(f)
    filenames = [file for file in os.listdir(target) if is_match(file) ]
    results = OD(zip(range(1, 601), [(0,-1)]*600))
    for fname in filenames:
        idx = int(fname.split("_")[0])
        with open(os.path.join(target, fname)) as f:
            lines = f.readlines()
            # assume sorted lo -> hi
            best, seed = lines[-1].split(",")
        results[idx] = (best, seed)
    with open(os.path.join(target, outname), "w") as outfile:
        outfile.write("\n".join("%s, %s" % (t[0], t[1]) for t in results.values()))

def condense_paths():
    target = "paths"
    outname = "_condensed.txt"
    is_match = lambda f: re.compile(r'\d+.*\.txt').match(f)
    filenames = [file for file in os.listdir(target) if is_match(file) ]
    results = OD(zip(range(1, 601), ['MISSING']*600))
    for fname in filenames:
        idx = int(fname.split("_")[0])
        with open(os.path.join(target, fname)) as f:
            lines = f.readlines()
            path_cover = []
            for line in lines[2:]:
                path = " ".join("%s" % el for el in eval(line.split(':')[-1]))
                path_cover.append(path)
            text = "; ".join(path for path in path_cover)
        results[idx] = text
    with open(os.path.join(target, outname), "w") as outfile:
        outfile.write("\n".join(results.values()))

def find_57():
    target = "final_inputs"
    is_match = lambda f: re.compile(r'\d+.*\.in').match(f)
    filenames = [file for file in os.listdir(target) if is_match(file) ]
    hits = []
    for fname in filenames:
        idx = int(fname.split(".in")[0])
        with open(os.path.join(target, fname)) as f:
            lines = f.readlines()
            fingerprints = [57, 42, 57, 20]
            c = 0
            for i,x in enumerate(fingerprints):
                if i >= len(lines)-1:
                    continue
                val = int(lines[i+1].split()[i])
                if val == x:
                    c += 1
            if c == len(fingerprints):
                print("Potential match:", idx)

def main():
    # filename = "data/sample2.in"
    filename = "data/generated1.in"
    edges, perfs = validate_file(filename)
    graph = make_graph(edges, perfs)
    graph.display()

if __name__ == '__main__':
    # standardize_input_names()
    segment_easy_graphs()
    segment_targets()
    get_best_seeds()
    condense_paths()