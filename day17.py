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

    last_num_still = None
    last_num_flowing = None
    tick = 0
    while True:
        if tick % 1000 == 0:
            print(scan)
        num_still = len(scan.still_water)
        num_flowing = len(scan.flowing_water)
        if num_still == last_num_still and num_flowing == last_num_flowing:
            break
        last_num_still = num_still
        last_num_flowing = num_flowing

        #print(scan)
        before = time.time()
        scan.tick()
        after = time.time()
        print("{}: F {} S {} T {:5}".format(tick, num_flowing, num_still, after-before))
        #time.sleep(0.2)
        #os.system("clear")
        #print("------")
        tick += 1

    print(scan)
    print("Water tiles: {}".format(num_flowing + num_still))


class Pt():
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def below(self):
        return Pt(self.x, self.y+1)


    def left(self):
        return Pt(self.x-1, self.y)


    def right(self):
        return Pt(self.x+1, self.y)


    def __repr__(self):
        return "{},{}".format(self.x, self.y)


    def __lt__(self, other):
        if self.y == other.y:
            return self.x < other.x
        return self.y < other.y


    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


    def __hash__(self):
        return hash((self.x, self.y))


class Scan():
    def __init__(self):
        self.horiz = []
        self.vert = []
        self.xmin = 500
        self.xmax = 500
        self.ymin = 1000
        self.ymax = 0


        self.still_water = set()
        self.flowing_water = set()


    def tick(self):

        for pt in self.flowing_water.copy():
            c = self._peek(pt)
            below = pt.below()
            cbelow = self._peek(below)
            left = pt.left()
            cleft = self._peek(left)
            right = pt.right()
            cright = self._peek(right)

            if cbelow == '.':
                self.flowing_water.add(below)
            elif cbelow == '#' or cbelow == '~':
                if cleft == '.':
                    self.flowing_water.add(left)
#                elif (cleft == '#' or cleft == '~') and cright == '|':
                elif (cleft == '#' or cleft == '~'):
                    # Have we filled a row?
                    check_pt = pt
                    while True:
                        if self._peek(check_pt) != '|':
                            break
                        check_pt = check_pt.right()
                    if self._peek(check_pt) == '#':
                        # Fill the row
                        fill_pt = pt
                        while fill_pt != check_pt:
                            self.still_water.add(fill_pt)
                            self.flowing_water.remove(fill_pt)
                            fill_pt = fill_pt.right()
                if cright == '.':
                    self.flowing_water.add(right)

        self._render_water()


    def inside(self, pt):
        return pt.x >= self.xmin and pt.x <= self.xmax and pt.y >= self.ymin and pt.y <= self.ymax


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
        self.xmin -= 1
        self.xmax += 1
        xwater = 500
        self.flowing_water.add(Pt(xwater, self.ymin))
        self._render_all()


    def _poke(self, pt, c):
#        self.scan[pt.y-self.ymin+1][pt.x-self.xmin+1] = ord(c)
#        print("x {} y {} xmin {} ymin {} xmax {} ymax {}".format(pt.x, pt.y, self.xmin, self.ymin, self.xmax, self.ymax))
        self.scan[pt.y-self.ymin][pt.x-self.xmin] = ord(c)


    def _peek(self, pt):
        if not self.inside(pt):
            return None
#        return chr(self.scan[pt.y-self.ymin+1][pt.x-self.xmin+1])
        return chr(self.scan[pt.y-self.ymin][pt.x-self.xmin])


    def _height(self):
        return self.ymax - self.ymin + 1


    def _width(self):
        return self.xmax - self.xmin + 3


    def __repr__(self):
        header = "xmin {} xmax {} ymin {} ymax {}".format(self.xmin, self.xmax, self.ymin, self.ymax)
#        water = "New: {}".format(self.new_water) + "\n" + "Old: {}".format(self.old_water)
        water = ''
        scan_str = "\n".join([row.decode('ascii') for row in self.scan])
        return header + "\n" + water + "\n" + scan_str


    def _render_all(self):
        self.scan = [bytearray(b'.' * self._width()) for _ in range(self._height())]
        for h in self.horiz:
            y, xlo, xhi = h
            for x in range(xlo, xhi+1):
                self._poke(Pt(x, y), '#')
        for v in self.vert:
            x, ylo, yhi = v
            for y in range(ylo, yhi+1):
                self._poke(Pt(x, y), '#')
        self._render_water()


    def _render_water(self):
        for pt in self.still_water:
            self._poke(pt, '~')
        for pt in self.flowing_water:
            self._poke(pt, '|')



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
