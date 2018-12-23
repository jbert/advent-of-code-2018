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
    weakest_bot = min(bots, key=lambda b: b.r)
    print("weakest bot: {}".format(weakest_bot))
    min_step = weakest_bot.r

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

    # Assumption: max score is acheived on an edge
    edge_pts = []

    best_pts = None
    best_count = 0

    def score(pt):
        return len([b for b in bots if b.range_includes_pt(pt)])

    for b in bots:
        edge_pts = b.edge_points()
        print("B {} nep {}".format(b, edge_pts))
        for pt in edge_pts:
            count = score(pt)
            print("Best: {} {}".format(best_count, best_pts))
            if count == best_count:
                best_pts.append(pt)
            elif count > best_count:
                best_count = count
                best_pts = [pt]

    def dist(pt):
        return abs(pt.x)+abs(pt.y)+abs(pt.z)

    for v in best_vertices:
        print("best count {} at {} d {}".format(best_count, v, abs(v.x)+abs(v.y)+abs(v.z)))

    assert len(best_vertices) == 1

    v = best_vertices[0]
    assert v.x > 0
    assert v.y > 0
    assert v.z > 0
    best_d = dist(v)
    for _ in range(10):
        w = Pt(v.x-1,v.y-1,v.z-1)
        s = score(w)
        print("w {} score {} d {} w in vert: {}".format(w, s, dist(w), v in vertices))
#        if s == best_count:
        v = w
#        else:
#            break

    print("Best current v is {} d {}".format(v, dist(v)))
        


class Pt:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return "<{},{},{}>".format(self.x, self.y, self.z)

    def adjacent(self):
        return [
                Pt(self.x - 1, self.y, self.z),
                Pt(self.x + 1, self.y, self.z),
                Pt(self.x, self.y - 1, self.z),
                Pt(self.x, self.y + 1, self.z),
                Pt(self.x, self.y, self.z - 1),
                Pt(self.x, self.y, self.z + 1),
                ]

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash((self.x, self.y, self.z))



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

    def range_includes_pt(self, pt):
        return abs(self.x - pt.x) + abs(self.y - pt.y) + abs(self.z - pt.z) <= self.r

    def range_includes(self, other):
        return self.distance_to(other) <= self.r

    def distance_to_pt(self, pt):
        return abs(self.x - pt.x) + abs(self.y - pt.y) + abs(self.z - pt.z)

    def distance_to(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def edge_points(self):
        r = self.r
        pts = []
        for i in range(r+1):
            pts.append(Pt(self.x+r-i, self.y+r-i, self.z + i))
            pts.append(Pt(self.x-r+i, self.y+r-i, self.z + i))
            pts.append(Pt(self.x+r+i, self.y-r+i, self.z + i))
            pts.append(Pt(self.x-r+i, self.y-r+i, self.z + i))
            pts.append(Pt(self.x+r-i, self.y+r-i, self.z - i))
            pts.append(Pt(self.x-r+i, self.y+r-i, self.z - i))
            pts.append(Pt(self.x+r+i, self.y-r+i, self.z - i))
            pts.append(Pt(self.x-r+i, self.y-r+i, self.z - i))
        return pts

    def vertices(self):
        r = self.r
        return [
                Pt(self.x - r, self.y, self.z),
                Pt(self.x + r, self.y, self.z),
                Pt(self.x, self.y - r, self.z),
                Pt(self.x, self.y + r, self.z),
                Pt(self.x, self.y, self.z - r),
                Pt(self.x, self.y, self.z + r),
                ]

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
