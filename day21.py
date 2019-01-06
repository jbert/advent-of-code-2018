#!/usr/bin/python3
def main():
    depth = 510
    target = (10, 10)

    depth = 5616
    target = (10, 785)

    system = make_system(depth, target)
    print_system(depth, target, system)
    answer = risk_level(depth, target, system)
    print("Part1: {}".format(answer))

    target = target[0] + target[1] * 1j
    path = find_path(depth, target, system)
    print("Part2: {} minutes".format(path.minutes))
    node = path
    while node:
        print(node)
        node = node.prev


def find_path(depth, target, system):
    # We run A*, but consider each tooling option as a separate path
    # with the cost of switching built into the heuristic

    class Node:
        def __init__(self, pt, tool, prev):
            self.pt = pt
            self.tool = tool

            self.prev = prev
            self.minutes = 0
            t = 1
            if prev:
                if self.tool != prev.tool:
                    t += 7
                self.minutes = prev.minutes + t

        def __lt__(self, other):
            if self.minutes < other.minutes:
                return True
            if self.minutes > other.minutes:
                return False
            if self.pt.real < other.pt.real:
                return True
            if self.pt.real > other.pt.real:
                return False
            return self.pt.imag < other.pt.imag

        def __eq__(self, other):
            return self.pt == other.pt and self.tool == other.tool

        def __hash__(self):
            return hash((self.pt, self.tool))

        def __repr__(self):
            return "{}: {} {} mins".format(self.pt, self.tool, self.minutes)

        def adjacent_pts(self):
            adj = [self.pt + 1, self.pt - 1, self.pt + 1j, self.pt - 1j]
            return [a for a in adj if a.real >= 0 and a.imag >= 0
                    and a.real < int(target.real) + 60 and a.imag < int(target.imag) + 60]

    def _viable(n):
        if n.pt == target:
            return n.tool == 'torch'
        try:
            gindex = system[int(n.pt.imag)][int(n.pt.real)]
        except IndexError as e:
            print("Failed to lookup {}".format(n.pt))
            raise e
        t = gindex_to_elevel(depth, gindex) % 3
        if t == 0:
            # rocky
            return n.tool != 'none'
        elif t == 1:
            # wet
            return n.tool != 'torch'
        elif t == 2:
            # narrow
            return n.tool != 'gear'
        else:
            raise RuntimeError("wtf")

    # Don't go back where we've been
    visited = set()
    start = Node(0+0j, 'torch', None)

    # Edge we are exploring
    fringe = dict()
    fringe[str(start)] = start

    while True:
        if len(fringe) <= 0:
            # No path
            return None

        node = min(fringe.values())

#        print("N: {}".format(node))
        if node.pt == target:
            # Found it
            break
        next_steps = [Node(next_pt, tool, node) for tool in ['none', 'torch', 'gear'] for next_pt in node.adjacent_pts()]
        next_steps = [ns for ns in next_steps if ns not in visited and _viable(ns)]
#        print("NS: {}".format(next_steps))
        for next_step in next_steps:
            try:
                existing = fringe[str(next_step)]
                if existing and existing.minutes < next_step.minutes:
                    next_step = existing
            except KeyError:
                pass
            fringe[str(next_step)] = next_step
        del(fringe[str(node)])
        visited.add(node)

    assert node.pt == target
    return node


def risk_level(depth, target, system):
    rows = system[0:target[1]+1]
    level = sum([gindex_to_elevel(depth, gindex) % 3 for row in rows for gindex in row[0:target[0]+1]])
    return level


def print_system(depth, target, system):
    for row in system:
        print("".join([elevel_to_type(gindex_to_elevel(depth, gindex)) for gindex in row]))


def elevel_to_type(elevel):
    m = elevel % 3
    if m == 0:
        return '.'
    elif m == 1:
        return '='
    else:
        return '|'


def gindex_to_elevel(depth, gindex):
    return (gindex + depth) % 20183


def make_system(depth, target):
    tx, ty = target

    gindex = []
    for y in range(ty + 60):
        row = []
        gindex.append(row)
#        print("Y: {}".format(y))
        for x in range(tx + 60):
            # print("X: {}".format(x))
            if x == 0 and y == 0:
                row.append(0)
            elif x == tx and y == ty:
                row.append(0)
            elif y == 0:
                row.append(x * 16807)
            elif x == 0:
                row.append(y * 48271)
            else:
                row.append(gindex_to_elevel(depth, gindex[y-1][x]) * gindex_to_elevel(depth, gindex[y][x-1]))
#        print("GINDEX: {}".format(gindex))
    return gindex


if __name__ == '__main__':
    main()
