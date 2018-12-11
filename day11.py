#!/usr/bin/python3
import time

def main():

    with open("day10-input.txt") as f:
        lines = f.readlines()

#    pts = parse_lines(lines)
#    part1(pts)
    test_cases = [
            ((3, 5), 8, 4),
            ((122, 79), 57, -5),
            ((217, 196), 39, 0),
            ((101, 153), 71, 4),
            ]
    for tc in test_cases:
        print(tc)
        (coord, gsn, expected_pl) = tc
        pt = Pt(coord[0], coord[1])
        pl = pt.power_level(gsn)
        print("pl: {} {}: {}".format(pl, expected_pl, pl == expected_pl))
        assert pl == expected_pl

    print("---")

#    gsn = 18
#    soln, tpl = part1(gsn)
#    print("gsn: {} {}: {}".format(gsn, soln, tpl))
#    
#    gsn = 42
#    soln, tpl = part1(gsn)
#    print("gsn: {} {}: {}".format(gsn, soln, tpl))
#
#    gsn = 6042 
#    soln, tpl = part1(gsn)
#    print("gsn: {} {}: {}".format(gsn, soln, tpl))
#    
    soln, tpl, size = part2(gsn)
    print("P2 coord {} size {} tpl".format(soln, size, tpl))
    

#    soln = 0, 0
#    for dj in range(40, 50):
#        print(" ".join(["{:2}".format(power_level(soln[0] + di, soln[1] + dj, gsn)) for di in range(30, 40)]))



def part1(gsn):
    width, height = 300,300
    max_tpl = 0
    max_coord = None
    for i in range(width-2):
        for j in range(height-2):
            tpl = power_level_size(i, j, gsn, 3)
            if tpl > max_tpl:
                max_coord = (i, j)
                max_tpl = tpl

    return max_coord, max_tpl


def part2(gsn):
    width, height = 300,300
    max_tpl = 0
    max_coord = None
    max_size = None
    last_time = None
    for size in range(3, 300):
        now = time.time()
        if last_time is not None:
            print("{}: {}".format(size, now - last_time))
        else:
            print("{}:".format(size))
        last_time = now

        for i in range(width-size):
            for j in range(height-size):
                tpl = power_level_size(i, j, gsn, size)
                if tpl > max_tpl:
                    max_coord = (i, j)
                    max_tpl = tpl
                    max_size = size

    return max_coord, max_tpl, max_size


def power_level_size(i, j, gsn, size):
    tpl = 0
    for di in range(size):
        for dj in range(size):
            tpl += power_level(i + di, j + dj, gsn)

    return tpl


def power_level(x, y, gsn):
    rack_id = x + 10
    pl = rack_id * y
    pl += gsn
    pl *= rack_id
    pl %= 1000
    pl //= 100
    pl -= 5
    return pl


class Pt():

    def __init__(self,x,y):
        self.x = x
        self.y = y


    def __repr__(self):
        return "({},{})".format(self.x,self.y)


    def power_level(self, gsn):
        return power_level(self.x, self.y, gsn)


if __name__ == "__main__":
    main()
