#!/usr/bin/python3
import re

def main():
    with open("day3-input.txt") as f:
        lines = f.readlines()

    claims = [parse_claim_to_rect(line) for line in lines]

    print("Got {} claims".format(len(claims)))
#    for claim in claims:
#        print(claim)

#    part1(claims)
    part2(claims)

def part1(claims):

    width = 1000
    height = 1000
    step = 100
    overcommitted = 0
    for i in range(0, width, step):
        print("i: {}".format(i))
        for j in range(0, height, step):
            region = Rect(None, i, j, step, step)
            region_rects = [r for r in claims if region.intersect(r) is not None]

            for ii in range(0, step):
                for jj in range(0, step):
                    within = 0
                    for rect in region_rects:
                        if rect.contains(i+ii, j+jj):
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
