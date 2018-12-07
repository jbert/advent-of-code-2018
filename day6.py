#!/usr/bin/python3
import re
from collections import defaultdict

def main():
    with open("day6-input.txt") as f:
        lines = f.readlines()

    coords = [parse_line(line) for line in lines]

#    coords = [ [1, 1], [1, 6], [8, 3], [3, 4], [5, 5], [8, 9] ]
    pts = [Point(t[0], t[1]) for t in enumerate(coords)]
    print(pts)
#    part1(pts)
    part2(pts)


def part2(pts):
    # moving one step can't move the total dist more than #pts
    # so track the max-possible-distance and only check when we are close

    # not sure of correct bounding box, try this (or could spiral out)
    min_x = min(pts, key=lambda t: t.x).x
    max_x = max(pts, key=lambda t: t.x).x

    min_y = min(pts, key=lambda t: t.y).y
    max_y = max(pts, key=lambda t: t.y).y

    target_tdist = 10000
    max_possible_tdist = None

    def calc_tdist(coord):
        return sum([pt.mdist(coord) for pt in pts])

    safe_area = 0
    num_pts = len(pts)
    for i in range(min_x, max_x):
        for j in range(min_y, max_y):
            if max_possible_tdist is None or max_possible_tdist >= target_tdist:
                max_possible_tdist = calc_tdist((i, j))
            if max_possible_tdist < target_tdist:
                safe_area += 1
            max_possible_tdist += num_pts

    print("SA: {}".format(safe_area))


def parse_line(line):
    pattern = r"(\d+), (\d+)"
    match = re.search(pattern, line)
    if not match:
        raise RuntimeError("Failed to match line: {}".format(line))
    x, y = map(int, match.groups())
    return (x, y)


def part1(pts):
    min_x = min(pts, key=lambda t: t.x).x
    max_x = max(pts, key=lambda t: t.x).x

    min_y = min(pts, key=lambda t: t.y).y
    max_y = max(pts, key=lambda t: t.y).y

    print("min({} {}) max({} {})".format(min_x, min_y, max_x, max_y))

    areas = defaultdict(int)
    coords = [(i, j) for i in range(min_x, max_x) for j in range(min_y, max_y)]

    def nearest_pt_label(coord):
        dist_labels = sorted([(pt.mdist(coord), pt.label) for pt in pts])
        d, l = dist_labels[0]
        if dist_labels[1][0] == d:
            return None
        else:
            return l

    for label in [nearest_pt_label(coord) for coord in coords]:
        if label is not None:
            areas[label] += 1

    print("Areas: {}".format(areas))
    print(max(areas.items(), key=lambda t: t[1]))


class Point():

    def __init__(self, label, t):
        self.label = label
        self.x = t[0]
        self.y = t[1]

    def mdist(self, t):
        return abs(self.x - t[0]) + abs(self.y - t[1])

    def __repr__(self):
        return "P{}({}, {})".format(self.label, self.x, self.y)

if __name__ == "__main__":
    main()
