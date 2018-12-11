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
    
    gsn = 6042
    soln, tpl, size = part2(gsn)
    print("P2 coord {} size {} tpl".format(soln, size, tpl))
    


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

    step = 10
    g = Grid(width, height, step, lambda i, j: power_level(i, j, gsn))
    for size in range(3, 300):
#    for size in range(3, 10):
        start_time = time.time()
        for i in range(width-size):
            for j in range(height-size):
                tpl = g.rect_sum(i, j, size, size)
#                tpl = power_level_size(i, j, gsn, size)
                if tpl > max_tpl:
                    max_coord = (i, j)
                    max_tpl = tpl
                    max_size = size

        end_time = time.time()
        print("{}: {} {}".format(size, max_tpl, end_time - start_time))

    return max_coord, max_tpl, max_size


class Grid:
    def __init__(self, w, h, step, f):
        assert w % step == 0
        assert h % step == 0
        self.w = w
        self.h = h
        self.step = step
        self.f = f

        self._make_grid()


    def _make_grid(self):
        col = [0] * (self.h // self.step)
        self.g = [col.copy() for _ in range(self.w // self.step)]
        for i in range(0, self.w, self.step):
            for j in range(0, self.h, self.step):
                self.g[i//self.step][j//self.step] = self._rect_sum(i, j, self.step, self.step)


    def rect_sum(self, l, t, w, h):
        return self._rect_sum(l, t, w, h)


    def _rect_sum(self, l, t, w, h):
        s = 0
        for i in range(l, l+w):
            for j in range(t, t+h):
                s += self.f(i, j)

        return s


def power_level_size(i, j, gsn, size):
    tpl = 0
    for ii in range(i, i+size):
        for jj in range(j, j+size):
            tpl += power_level(ii, jj, gsn)

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
