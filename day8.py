#!/usr/bin/python3
import string

def main():

    line = """2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2\n"""
#    with open("day8-input.txt") as f:
#        line = f.readline()

    part1(line)

class Node:

    def __init__(self, name):
        self.name = name
        self.children = []
        self.mdata = []

    def tree_sum_mdata(self):
        return sum(self.mdata + [n.tree_sum_mdata() for n in self.children])

def read_tree(namei, tokens):
    if not tokens:
        return 0, []

    name = next(namei)
    node = Node(name)

#    print("{}: {}".format(name, tokens))

    (num_children, num_node_mdata) = tokens[0:2]
    tokens = tokens[2:]

    for i in range(num_children):
        child, tokens = read_tree(namei, tokens)
        node.children.append(child)

    mdata = tokens[0:num_node_mdata]
    node.mdata += mdata

    tokens = tokens[num_node_mdata:]

    return node, tokens

def part1(line):
    line = line.rstrip()

    tokens = [int(s) for s in line.split(" ")]
    namei = iter(string.ascii_lowercase)

    tree, _ = read_tree(namei, tokens)

    print("Total metadata: {}".format(tree.tree_sum_mdata()))


if __name__ == "__main__":
    main()
