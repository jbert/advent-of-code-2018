#!/usr/bin/python3
import re
import time
import os

def main():
    lines = """
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
""".split("\n")

#    with open("day17-input.txt") as f:
#        lines = f.readlines()

    scan = parse_lines(lines)
    part1(scan)


def part1(scan):
    while scan.has_change():
        print(scan)
        scan.tick()
        time.sleep(0.1)
        os.system("clear")

    print("Water tiles: {}".format(scan.water_tiles()))


class Scan():
    def __init__(self):
        self.horiz = []
        self.vert = []
        self.xmin = 500
        self.xmax = 500
        self.ymin = 0
        self.ymax = 0
        self.ywater = 0
        self.xwater = 500

        self.new_water = [(self.xwater, self.ywater)]


    def has_change(self):
        return len(self.new_water) > 0


    def tick(self):
        pass
        #for pt in self.new_water:


    def add_horiz(self, y, xlo, xhi):
        self.xmin = min(self.xmin, xlo)
        self.xmax = max(self.xmax, xhi)
        self.ymin = min(self.ymin, y)
        self.ymax = max(self.ymax, y)
        self.horiz.append((y, xlo, xhi))


    def add_vert(self, x, ylo, yhi):
        self.xmin = min(self.xmin, x)
        self.xmax = max(self.xmax, x)
        self.ymin = min(self.ymin, ylo)
        self.ymax = max(self.ymax, yhi)
        self.vert.append((x, ylo, yhi))


    def finish_load(self):
        self._render_all()


    def _poke(self, x, y, c):
        self.scan[y-self.ymin+1][x-self.xmin+1] = ord(c)


    def _height(self):
        return self.ymax - self.ymin + 3


    def _width(self):
        return self.xmax - self.xmin + 3


    def __repr__(self):
        header = "xmin {} xmax {} ymin {} ymax {}".format(self.xmin, self.xmax, self.ymin, self.ymax)
        scan_str = "\n".join([row.decode('ascii') for row in self.scan])
        return header + "\n" + scan_str


    def _render_all(self):
        self.scan = [bytearray(b'.' * self._width()) for _ in range(self._height())]
        for h in self.horiz:
            y, xlo, xhi = h
            for x in range(xlo, xhi+1):
                self._poke(x, y, '#')
        for v in self.vert:
            x, ylo, yhi = v
            for y in range(ylo, yhi+1):
                self._poke(x, y, '#')
        self._poke(self.xwater, self.ywater, '+')



def parse_lines(lines):
    lines = [l for l in lines if len(l) > 0]
    pattern = r"[xy]=(\d+), [xy]=(\d+)\.\.(\d+)"

    scan = Scan()
    for line in lines:
        match = re.search(pattern, line)
        if not match:
            raise RuntimeError("can't parse line: {}".format(line))
        const, lo, hi = [int(s) for s in match.groups()]
        if line[0] == 'x':
            scan.add_vert(const, lo, hi)
        elif line[0] == 'y':
            scan.add_horiz(const, lo, hi)
        else:
            raise RuntimeError("wtf: {}".format(line))

    scan.finish_load()

    return scan


if __name__ == '__main__':
    main()
