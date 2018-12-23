#!/usr/bin/python3
import re

def main():

    lines = """
pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1
""".split("\n")

    with open("day23-input.txt") as f:
        lines = f.readlines()

    bots = parse_lines(lines)
    strongest_bot = max(bots, key=lambda b: b.r)
    print(strongest_bot)
    print(bots)
    in_range = [b for b in bots if strongest_bot.range_includes(b)]
    print("{} bots in range of strongest".format(len(in_range)))

class Bot:
    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z
        self.r = r

    def __repr__(self):
        return "<{},{},{}> r={}".format(self.x, self.y, self.z, self.r)

    def range_includes(self, other):
        return self.distance_to(other) <= self.r

    def distance_to(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

def parse_lines(lines):
    pattern = r'^pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)'
    def _parse_line(line):
        match = re.search(pattern, line)
        if not match:
            raise RuntimeError("Can't match line: {}".format(line))
        (x, y, z, r) = [int(s) for s in match.groups()]
        return Bot(x, y, z, r)

    bots = [_parse_line(l) for l in lines if l]
    return bots


if __name__ == '__main__':
    main()
