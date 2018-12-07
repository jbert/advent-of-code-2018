#!/usr/bin/python3
import re
from collections import defaultdict
from heapq import *

def main():

    lines = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.""".split("\n")
    with open("day7-input.txt") as f:
        lines = f.readlines()

    (verts, edges) = parse_lines(lines)

#    print("V: {}".format(verts))
#    print("E: {}".format(edges))
    part1(verts, edges)


def reverse_edges(edges):
    # Ten pts to gryffindor for anyone who can do the whole
    # edge reverse in a single comprehension
    redges = defaultdict(list)
    for k, vs in edges.items():
        for v in vs:
            redges[v].append(k)

    return redges


def part1(verts, edges):

    redges = reverse_edges(edges)

    print_graph("Reverse edges", verts, redges)

    def find_a_root(v):
        while True:
            vs = redges.get(v)
            if not vs:
                break
            v = vs[0]
        return v

    roots = set([find_a_root(v) for v in verts])
    print("R: {}".format(roots))

    sequence = []
    possible = list(roots)
    heapify(possible)

    while possible:
        v = heappop(possible)
        sequence.append(v)
        for c in edges[v]:
            pre_reqs = redges[c]
            done = set(sequence)
            if all([pre_req in done for pre_req in redges[c]]) and (c not in done) and (c not in possible):
                heappush(possible, c)
        print("V {}: {}".format(v, possible))

    print("{}".format(len(sequence)))
    print("{}".format(''.join(sequence)))


def print_graph(title, verts, edges):
    print("digraph \"{}\" { ", title)
    for k, vs in sorted(edges.items()):
        print("{} -> {{{}}};".format(k, ' '.join(vs)))
    print("}")


def parse_lines(lines):

    def parse_line(i, line):
        pattern = r"^Step (\S*) must be finished before step (\S*) can begin.\n?$"
        match = re.search(pattern, line)
        if not match:
            raise RuntimeError("Failed to match line {}: {}".format(i, line))
        return match.groups()

    edges = defaultdict(list)
    verts = set()
    for i, line in enumerate(lines):
        (a, b) = parse_line(i, line)
        edges[a].append(b)
        verts.add(a)
        verts.add(b)

    print_graph("Forwrd edges", verts, edges)

    return verts, edges


if __name__ == "__main__":
    main()
