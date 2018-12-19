#!/usr/bin/python3
from collections import defaultdict

def main():
    lines = """
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.
""".split("\n")

    with open("day18-input.txt") as f:
        lines = f.readlines()

    scan = parse_lines(lines)
    part1(scan)
    scan = parse_lines(lines)
    part2(scan)


def part2(scan):
#    doit(scan, 1000000000)
    # Ran this and:
    # - 467 minutes 183141 value
    # - 494 minutes 185556 value
    # - RuntimeError: Duplicate: 183141 mins 467 resource

#    467 minutes 183141 value
#    468 minutes 183787 value
#    469 minutes 183040 value
#    470 minutes 184000 value
#    471 minutes 184896 value
#    472 minutes 184320 value
#    473 minutes 182909 value
#    474 minutes 183744 value
#    475 minutes 183168 value
#    476 minutes 182275 value
#    477 minutes 183360 value
#    478 minutes 183540 value
#    479 minutes 182649 value
#    480 minutes 180942 value
#    481 minutes 182328 value
#    482 minutes 182080 value
#    483 minutes 183612 value
#    484 minutes 185725 value
#    485 minutes 187525 value
#    486 minutes 189912 value
#    487 minutes 194449 value
#    488 minutes 195160 value
#    489 minutes 198930 value
#    490 minutes 197185 value
#    491 minutes 193672 value
#    492 minutes 191196 value
#    493 minutes 187912 value
#    494 minutes 185556 value

    values = [183141, 183787, 183040, 184000, 184896, 184320, 182909, 183744, 183168, 182275, 183360, 183540, 182649, 180942, 182328, 182080, 183612, 185725, 187525, 189912, 194449, 195160, 198930, 197185, 193672, 191196, 187912, 185556, ]

    period = 495 - 467
    offset = (1000000000-467) % period
    print("offset {} rv {}".format(offset, values[offset]))



def part1(scan):
    doit(scan, 10)


def doit(scan, steps):
    seen = defaultdict(int)

    for i in range(steps+1):
        s = str(scan)
        if s in seen:
            t = seen[s]
            raise RuntimeError("Duplicate: {} mins {} resource".format(t[0], t[1]))
        seen[s] = (scan.resource_value(), i)
        print("{} minutes {} value".format(i, scan.resource_value()))
        print(s)
        scan.tick()

    i += 1
    print("{} minutes {} value".format(i, scan.resource_value()))
    print(scan)


MAP_OPEN        = ord('.')
MAP_TREES       = ord('|')
MAP_LUMBERYARD  = ord('#')


def parse_lines(lines):
    lines = [l.rstrip().encode('ascii') for l in lines if len(l) > 1]
    return Scan(lines)

class Pt():
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def __repr__(self):
        return "{},{}".format(self.x, self.y)


    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


    def __hash__(self):
        return hash((self.x, self.y))


class Scan():
    def __init__(self, state):
        self.state = state
        self.width = len(self.state[0])
        self.height = len(self.state)

        self.counts = defaultdict(int)
        for j in range(self.height):
            for i in range(self.width):
                self.counts[self.state[j][i]] += 1


    def resource_value(self):
        return self.counts[MAP_TREES] * self.counts[MAP_LUMBERYARD]


    def __repr__(self):
        scan_str = "\n".join([row.decode('ascii') for row in self.state])
        return scan_str


    def _within(self, pt):
        return pt.x >= 0 and pt.y >= 0 and pt.x < self.width and pt.y < self.height


    def _neighbours(self, pt):
        pts = [Pt(pt.x + dx, pt.y + dy) for dx in [-1,0,1] for dy in [-1,0,1] if not(dx == 0 and dy == 0)]
        return [pt for pt in pts if self._within(pt)]


    def calc_next(current, neighbours):
        counts = defaultdict(int)
        
        for n in neighbours:
            counts[n] += 1
        if current == MAP_OPEN:
            if counts[MAP_TREES] >= 3:
                return MAP_TREES
            else:
                return current
        if current == MAP_TREES:
            if counts[MAP_LUMBERYARD] >= 3:
                return MAP_LUMBERYARD
            else:
                return current
        if current == MAP_LUMBERYARD:
            if counts[MAP_LUMBERYARD] >= 1 and counts[MAP_TREES] >= 1:
                return MAP_LUMBERYARD
            else:
                return MAP_OPEN


        return MAP_TREES



    def tick(self):
        new_state = [bytearray([0] * self.width) for _ in range(self.height)]
        for j in range(self.height):
            for i in range(self.width):
                pt = Pt(i, j)
                neighbours = [self.state[pt.y][pt.x] for pt in self._neighbours(pt)]
                current = self.state[pt.y][pt.x]
                new = Scan.calc_next(current, neighbours)
                self.counts[current] -= 1
                new_state[j][i] = new
                self.counts[new] += 1

        self.state = new_state


if __name__ == '__main__':
    main()

