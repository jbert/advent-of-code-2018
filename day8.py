#!/usr/bin/python3
import string

def main():

#    line = """2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2\n"""
    with open("day8-input.txt") as f:
        line = f.readline()

    line = line.rstrip()

    tokens = [int(s) for s in line.split(" ")]

    tree, _ = read_tree(make_names, tokens)

    part1(tree)
    part2(tree)


def make_names():
    yield from iter(string.ascii_lowercase)


class Node:

    def __init__(self, name):
        self.name = name
        self.children = []
        self.mdata = []

    def tree_sum_mdata(self):
        return sum(self.mdata + [n.tree_sum_mdata() for n in self.children])

    def value(self):
        if self.children:
            child_values = [self.children[i].value() for i in self._value_indices()]
            return sum(child_values)
        else:
            return sum(self.mdata)

    def _value_indices(self):
            indices = [m-1 for m in self.mdata if m > 0 and m <= len(self.children)]
#            print("M: {} lc: {} I: {}".format(self.mdata, len(self.children), indices))
            return indices

    def print(self):
        self._print(0)

    def _print(self, depth):
        prefix = " " * (depth * 2)
        print("{}{}".format(prefix, self))
        for c in self.children:
            c._print(depth+1)

    def __repr__(self):
        return "C: {} M: {} V: {} VI: {}".format(len(self.children), self.mdata, self.value(), self._value_indices())


def read_tree(namer, tokens):
    if not tokens:
        return 0, []

    name = namer()
    node = Node(name)

#    print("{}: {}".format(name, tokens))

    (num_children, num_node_mdata) = tokens[0:2]
    tokens = tokens[2:]

    for i in range(num_children):
        child, tokens = read_tree(namer, tokens)
        node.children.append(child)

    mdata = tokens[0:num_node_mdata]
    node.mdata += mdata

    tokens = tokens[num_node_mdata:]

    return node, tokens

def part1(tree):
    print("Total metadata: {}".format(tree.tree_sum_mdata()))

def part2(tree):
#    tree.print()
    print("Value : {}".format(tree.value()))


if __name__ == "__main__":
    main()
