#!/usr/bin/python3
import re

def main():
    lines = """
 0,0,0,0
 3,0,0,0
 0,3,0,0
 0,0,3,0
 0,0,0,3
 0,0,0,6
 9,0,0,0
12,0,0,0
""".split("\n")

    with open("day25-input.txt") as f:
        lines = f.readlines()


    stars = parse_lines(lines)
    for s in stars:
        s.remember_neighbours(stars)
    part1(stars)


def part1(stars):

    print(stars)

    still_finding = True
    constellations = []
    while stars:
        # Pick any star
        c = Constellation(stars.pop())
        c.expand()
        constellations.append(c)
        stars = [s for s in stars if s not in c.stars]

    print("{} constellations".format(len(constellations)))


class Constellation:
    def __init__(self, star):
        self.stars = [star]


    def expand(self):
        assert len(self.stars) == 1
        seen = set([self.stars[0]])
        todo = self.stars[0].neighbours
        while todo:
            s = todo.pop()
            self.stars.append(s)
            seen.add(s)
            todo += [n for n in s.neighbours if n not in seen]


class Star():
    def __init__(self, idx, coords):
        self.id = idx
        self.x, self.y, self.z, self.t = coords


    def __repr__(self):
        return "<{}, {}, {}, {}> ({} neighbours)".format(self.x, self.y, self.z, self.t, len(self.neighbours))


    def distance_to(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z) + abs(self.t - other.t)


    def remember_neighbours(self, stars):
        self.neighbours = [s for s in stars if s.id != self.id and self.distance_to(s) <= 3]


def parse_lines(lines):
    lines = [l for l in lines if len(l) > 0]

    idx = 0
    def _parse_line(line):
        coords = [int(d.lstrip()) for d in line.split(",")]
        nonlocal idx
        idx += 1
        return Star(idx, coords)

    return [_parse_line(l) for l in lines]


if __name__ == '__main__':
    main()
