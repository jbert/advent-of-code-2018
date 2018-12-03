#!/usr/bin/python3
import re

def main():
    with open("day3-input.txt") as f:
        lines = f.readlines()

    claims = [parse_claim_to_rect(line) for line in lines]

    print("Got {} claims".format(len(claims)))
    part1(claims)
#    part2(claims)

def part1(claims):

    width = 1000
    height = 1000
    whole_region = Rect(None, 0, 0, width, height)
    depth = 2
    print("Building...")
    qt = QuadTree(depth, whole_region, claims)
    print("Built...")
    overcommitted = 0
    for i in range(0, width):
#            print("=== i, j: {},{}".format(i,j))
        for j in range(0, height):
#            print("=== i, j: {},{}".format(i,j))
            rects = qt.rects_at(i, j)
            within = 0
            for rect in rects:
                if rect.contains(i, j):
                    within += 1
                    if within >= 2:
                        overcommitted += 1
                        break

    print("overcommitted is {}".format(overcommitted))

def part2(claims):
    for a in claims:
        intersects = [b for b in claims if b.intersect(a) is not None]
        if len(intersects) == 1:
            print("does not intersect: {}".format(a))
        print("{} has {}".format(a.idx, len(intersects)))


class QuadTree():


    def __init__(self, depth, region, rects):
        self.region = region
        self.rects = rects
        self.depth = 2
        self._create_children()
#        print("region {}".format(self))


    def __repr__(self):
        return "{} step ({},{})".format(self.region, self.w_step, self.h_step)


    def _create_children(self):
        self.children = None

        if self.depth == 0:
            return
        small_primes = [7, 5, 3, 2]
        self.w_step = 0
        self.h_step = 0
        for p in small_primes:
            if self.region.width > p and self.region.width % p == 0:
                self.w_step = self.region.width // p
            if self.region.height > p and self.region.height % p == 0:
                self.h_step = self.region.height // p
        if self.w_step == 0 or self.h_step == 0:
            return

        self.children = []
        for i in range(self.region.left, self.region.right(), self.w_step):
            col = []
            for j in range(self.region.top, self.region.bottom(), self.h_step):
                region = Rect(None, i, j, self.w_step, self.h_step)
                region_rects = [rect for rect in self.rects if region.intersect(rect) is not None]
                col.append(QuadTree(self.depth - 1, region, region_rects))
            self.children.append(col)


    def rects_at(self, i, j):
#        print("{}".format(self))
#        print("rx i {} j {}".format(i, j));
        if not self.region.contains(i, j):
            raise RuntimeError("Point not in quadtree region")
        if self.children is None:
            return self.rects
        isub = (i - self.region.left) // self.w_step
        jsub = (j - self.region.top) // self.h_step
#        print("rx isub {} jsub {}".format(isub, jsub));
        return self.children[isub][jsub].rects_at(i, j)



def parse_claim_to_rect(line):
    pattern = r"^#(\d+) @ (\d+),(\d+): (\d+)x(\d+)\n?$"
    match = re.search(pattern, line)
    if not match:
        raise RuntimeError("Failed to match line: {}".format(line))

    (idx, left, top, width, height) = [int(s) for s in match.groups()]
    return Rect(idx, left, top, width, height)


class Rect():

    def __init__(self, idx, left, top, width, height):
        self.idx = idx
        if self.idx is None:
            self.idx = id(self)
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def right(self):
        return self.left + self.width

    def bottom(self):
        return self.top + self.height

    def __repr__(self):
        return "#{} @ {},{}: {}x{}".format(self.idx, self.left, self.top, self.width, self.height)


    def intersect(self, other):
        """Return the rect which is the intersection, or None"""
        s = self
        o = other

        if o.left < s.left:
            (o, s) = (s, o)
        if s.right() <= o.left:
            return None

        ileft = o.left
        iwidth = s.right() - o.left

        if o.top < s.top:
            (o, s) = (s, o)
        if s.bottom() <= o.top:
            return None

        itop = o.top
        iheight = s.bottom() - o.top

        idx = None

        return Rect(idx, ileft, itop, iwidth, iheight)


    def contains(self, x, y):
        return self.left <= x and x < self.right() and self.top <= y and y < self.bottom()


if __name__ == "__main__":
    main()
