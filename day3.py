#!/usr/bin/python3
import re

def main():
    with open("day3-input.txt") as f:
        lines = f.readlines()

    claims = [parse_claim_to_rect(line) for line in lines]

#    for claim in claims:
#        print(claim)
    test_lines = [
            "#1 @ 1,3: 4x4",
            "#2 @ 3,1: 4x4",
            "#3 @ 5,5: 2x2",
            ]
    test_rects = [parse_claim_to_rect(line) for line in test_lines]
    overlap = test_rects[0].intersect(test_rects[1])
    print("overlap is {}".format(overlap))


def parse_claim_to_rect(line):
    pattern = r"^#(\d+) @ (\d+),(\d+): (\d+)x(\d+)\n?$"
    match = re.search(pattern, line)
    if not match:
        raise RuntimeError("Failed to match line: {}".format(line))

    (idx, left, top, width, height) = [int(s) for s in match.groups()]
    return Rect(idx, left, top, width, height)


class Rect():

    def __init__(self, idx, left, top, width, height):
        self.id = idx
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def right(self):
        return self.left + self.width

    def bottom(self):
        return self.top + self.height

    def __repr__(self):
        return "#{} @ {},{}: {}x{}".format(self.id, self.left, self.top, self.width, self.height)


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


if __name__ == "__main__":
    main()
