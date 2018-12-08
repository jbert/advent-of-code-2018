#!/usr/bin/python3
import string

def main():

#    line = """2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2\n"""
    with open("day8-input.txt") as f:
        line = f.readline()

    part1(line)


def read_tree_mdata(namei, tokens):
    if not tokens:
        return 0, []

#    name = next(namei)
#    print("{}: {}".format(name, tokens))

    (num_children, num_node_mdata) = tokens[0:2]
    tokens = tokens[2:]

    mdata_sum = 0
    for i in range(num_children):
        child_mdata_sum, tokens = read_tree_mdata(namei, tokens)
        mdata_sum += child_mdata_sum

    mdata = tokens[0:num_node_mdata]
#    print("{}: M: {}".format(name, mdata))
    mdata_sum += sum(mdata)
    tokens = tokens[num_node_mdata:]

    return mdata_sum, tokens

def part1(line):
    line = line.rstrip()

    tokens = [int(s) for s in line.split(" ")]
    namei = string.ascii_lowercase

    total_mdata_sum, _ = read_tree_mdata(namei, tokens)

    print(total_mdata_sum)


if __name__ == "__main__":
    main()
