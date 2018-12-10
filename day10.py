#!/usr/bin/python3
import re
import time
import os

def main():

    lines = """position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>""".split("\n")

    pts = parse_lines(lines)
    part1(pts)


class Pt():

    def __init__(self,x,y,dx,dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy


    def __repr__(self):
        return "({},{}) v ({},{})".format(self.x,self.y,self.dx,self.dy)


    def tick(self):
        self.x += self.dx
        self.y += self.dy


class Screen():
    def __init__(self, left, top, w, h):
        self.left = left
        self.top = top
        self.width = w
        self.height = h
        self.clear()


    def clear(self):
        nums = [ord('.')] * self.height
        col = bytearray(nums)
        self.screen = [col.copy() for _ in range(self.width)]


    def plot(self,x,y):
        print("P: {},{}".format(x, y))
        x -= self.left
        y -= self.top
        if x > 0 and y > 0 and x < self.width and y < self.height:
            self.screen[x][y] = ord('#')


    def draw(self):
        self._clear_screen()
        for j in range(self.height):
            row = bytearray([self.screen[i][j] for i in range(self.width)])
            print(row.decode('ascii'))


    def _clear_screen(self):
        # $ clear | hd
#        magic="1b5b334a1b5b481b5b324a"
#        print(bytearray.fromhex(magic))
#        os.system("clear")
        pass


def part1(pts):
    width = max(pts, key=lambda pt: pt.x).x
    height = max(pts, key=lambda pt: pt.y).y

    print("w {} h {}".format(width, height))

    s = Screen(-width, -height, 2*width, 2*height)
    for i in range(10):
        s.clear()
        for pt in pts:
            print("w {} h {}".format(pt.x,pt.y))
            s.plot(pt.x,pt.y)
            pt.tick()
        s.draw()
        time.sleep(1)



def parse_lines(lines):

    def parse_line(line):
        pattern = r"^position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>$"
        match = re.search(pattern, line)
        if not match:
            raise RuntimeError("Failed to match line: {}".format(line))
        (x, y, dx, dy) = [int(s) for s in match.groups()]
        return Pt(x,y,dx,dy)

    pts = [parse_line(l) for l in lines]
#    print(pts)
    return pts


if __name__ == "__main__":
    main()
