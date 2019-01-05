#!/usr/bin/python3

def main():
    depth = 510
    target = (10,10)

#   depth = 5616
#   target = (10,785)

    system = make_system(depth, target)
    print_system(depth, target, system)
    answer = risk_level(depth, target, system)
    print("Part1: {}".format(answer))


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
    for y in range(ty + 1):
        row = []
        gindex.append(row)
#        print("Y: {}".format(y))
        for x in range(tx + 1):
#            print("X: {}".format(x))
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
