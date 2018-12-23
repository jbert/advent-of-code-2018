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
    #part1(bots)
    part2(bots)


def part1(bots):
    strongest_bot = max(bots, key=lambda b: b.r)
    print(strongest_bot)
    print(bots)
    in_range = [b for b in bots if strongest_bot.range_includes(b)]
    print("{} bots in range of strongest".format(len(in_range)))


def part2(bots):
    xmin = 0
    xmax = 0
    ymin = 0
    ymax = 0
    zmin = 0
    zmax = 0
    for b in bots:
        if b.x < xmin:
            xmin = b.x
        if b.y < ymin:
            ymin = b.y
        if b.z < zmin:
            zmin = b.z

        if b.x > xmax:
            xmax = b.x
        if b.y > ymax:
            ymax = b.y
        if b.z > zmax:
            zmax = b.z

    
    while True:
        steps = 10
        grid_best = None
        grid_best_count = 0
        xstep = (xmax-xmin) // steps
        if xstep < 1:
            break
        ystep = (ymax-ymin) // steps
        zstep = (zmax-zmin) // steps
        for x in range(xmin, xmax+1, xstep):
            for y in range(ymin, ymax+1, ystep):
                for z in range(zmin, zmax+1, zstep):
                    count = len([b for b in bots if b.coords_in_range(x, y, z)])
                    if count > grid_best_count:
                        grid_best = (x, y, z)
                        grid_best_count = count
        print("xstep {} grid best {} count {}".format(xstep, grid_best, grid_best_count))

        xmin = grid_best[0] - (steps // 3) * xstep
        xmax = grid_best[0] + (steps // 3) * xstep
        ymin = grid_best[0] - (steps // 3) * ystep
        ymax = grid_best[0] + (steps // 3) * ystep
        zmin = grid_best[0] - (steps // 3) * zstep
        zmax = grid_best[0] + (steps // 3) * zstep

                
#
    #print("xmin {} xmax {} ymin {} ymax {} zmin{} zmax {}".format(xmin, xmax, ymin, ymax, zmin, zmax))
    #for x in range(xmin, xmax+1):
        #for y in range(ymin, ymax+1):
            #for z in range(zmin, zmax+1):

#    xorder = sorted(bots, key=lambda b: b.x)
#    xchanges = [(b.x-b.r, b.x+b.r) for b in bots]
#    ychanges = [(b.y-b.r, b.y+b.r) for b in bots]
#    zchanges = [(b.z-b.r, b.z+b.r) for b in bots]
#    print(xchanges)




class Bot:
    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z
        self.r = r

    def __repr__(self):
        return "<{},{},{}> r={}".format(self.x, self.y, self.z, self.r)

    def coords_in_range(self, x, y, z):
        return abs(self.x - x) + abs(self.y - y) + abs(self.z - z) <= self.r

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
