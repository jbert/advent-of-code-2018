#!/usr/bin/python3
import time
import collections
import functools

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
        self.f = f
        self._last_rect = None

        self._make_grid()


    def _make_grid(self):
        col = [0] * self.h
        self.g = [col.copy() for _ in range(self.w)]
        for i in range(self.w):
            for j in range(self.h):
                self.g[i][j] = self.f(i, j)


    def rect_sum(self, l, t, w, h):
        if self._last_rect and self._last_rect == (l+1, t, w, h):
            s = self._last_rect_sum
            s -= self._rect_sum(l, t, 1, h)
            s += self._rect_sum(l+w+1, t, 1, h)
        else:
            s = self._rect_sum(l, t, w, h)

        self._last_rect = (l, t, w, h)
        self._last_rect_sum = s
        return s


    def _grid_round_up(self, n):
        return (n-1) - (n-1) % self.step + self.step


    def _grid_round_down(self, n):
        return n - n % self.step


    def _rect_sum(self, l, t, w, h):
        if w == 0 or h == 0:
            return 0
#        print("_RS: l {} t {} w {} h {} step {}".format(l, t, w, h, self.step))
        assert w > 0
        assert h > 0
        s = 0
        for i in range(l, l+w):
            for j in range(t, t+h):
                s += self.g[i][j]

        return s


def power_level_size(i, j, gsn, size):
    tpl = 0
    for ii in range(i, i+size):
        for jj in range(j, j+size):
            tpl += power_level(ii, jj, gsn)

    return tpl


class memoized(object):
    '''Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    '''
    def __init__(self, func):
       self.func = func
       self.cache = {}
    def __call__(self, *args):
       if not isinstance(args, collections.Hashable):
          # uncacheable. a list, for instance.
          # better to not cache than blow up.
          return self.func(*args)
       if args in self.cache:
          return self.cache[args]
       else:
          value = self.func(*args)
          self.cache[args] = value
          return value
    def __repr__(self):
       '''Return the function's docstring.'''
       return self.func.__doc__
    def __get__(self, obj, objtype):
       '''Support instance methods.'''
       return functools.partial(self.__call__, obj)


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
