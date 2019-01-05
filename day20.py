#!/usr/bin/python3
import sys

def main():
    line = '^WNE$'
    sys.setrecursionlimit(100000)
    line = '^ENWWW(NEEE|SSE(EE|N))$'

    line = '^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$'

    with open("day20-input.txt") as f:
        line = f.readline()

    r = parse_regex(line)
    part1(r)


def part1(r):
    m = Map(r)
    print(m)
    print("Map distance: {}".format(m.distance()))


class Map:
    def __init__(self, r):
        self.r = r
        self._build()

    def distance(self):
        return 0

    def _build(self):
        rooms = dict()

        max_len = 0
        def _f(pos):
            seen = rooms.get(pos.location())
            if seen:
                pos.plen = seen.plen
                return
            rooms[pos.location()] = pos
            pos.plen += 1
            nonlocal max_len
            if pos.plen > max_len:
                max_len = pos.plen
            print("P: {} ML: {}".format(pos, max_len))

        p = Pos(0, 0, _f)
        _f(p)
        self.r.walk(p)

        self.max_len = max_len - 1

    def distance(self):
        return self.max_len


class Room:
    def __init__(self, x, y):
        self.n = None
        self.e = None
        self.s = None
        self.w = None


class Regex:
    def __init__(self, is_toplevel):
        self.r = []
        self.is_toplevel = is_toplevel

    def __repr__(self):
        rstr = "".join([str(sr) for sr in self.r])
        if self.is_toplevel:
            rstr = '^' + rstr + '$'
        return rstr

    def walk(self, p):
        for sr in self.r:
            sr.walk(p)


class Literal:
    def __init__(self, s):
        self.s = s

    def __repr__(self):
        return self.s

    def walk(self, p):
        for c in self.s:
            if c == 'N':
                p.n()
            elif c == 'E':
                p.e()
            elif c == 'W':
                p.w()
            elif c == 'S':
                p.s()
            else:
                raise RuntimeError("wtf")


class Option():
    def __init__(self):
        self.o = []

    def __repr__(self):
        return "(" + "|".join([str(so) for so in self.o]) + ")"

    def walk(self, p):
        p.save()
        for so in self.o:
            so.walk(p)
            p.restore()


class Pos():
    def __init__(self, x, y, f, plen=0):
        self.x = x
        self.y = y
        self.f = f
        self.plen = plen

    def n(self):
        self.y -= 1
        self.f(self)

    def s(self):
        self.y += 1
        self.f(self)

    def w(self):
        self.x -= 1
        self.f(self)

    def e(self):
        self.x += 1
        self.f(self)

    def __repr__(self):
        return "{},{} ({})".format(self.x, self.y, self.plen)

    def location(self):
        return "{},{}".format(self.x, self.y)

    def save(self):
        print("SAVE: plen {}".format(self.plen))
        self._save_x = self.x
        self._save_y = self.y
        self._save_plen = self.plen

    def restore(self):
        self.x = self._save_x
        self.y = self._save_y
        self.plen = self._save_plen
        print("REST: plen {}".format(self.plen))


def parse_regex(line):
    line = line.rstrip()
    news = set('NESW')

    def _parse_regex(line, toplevel):
        r = Regex(toplevel)
        while line and line[0] != ')' and line[0] != '|':
            if line[0] in news:
                line, chunk = _parse_literal(line)
                r.r.append(chunk)
            elif line[0] == '(':
                line, o = _parse_option(line[1:])
                r.r.append(o)
            else:
                raise RuntimeError("Failed to parse: {}".format(line[0]))

        return line, r

    def _parse_option(line):
        o = Option()

        # hack to support empty option
        while line:
            line, r = _parse_regex(line, False)
            o.o.append(r)
            if line[0] == '|':
                line = line[1:]
            elif line[0] == ')':
                break
            else:
                raise RuntimeError("Failed to parse: {}".format(line[0]))

        assert line[0] == ')'
        return line[1:], o


    def _parse_literal(line):
        chunk = ''
        while line and line[0] in news:
            chunk += line[0]
            line = line[1:]
        l = Literal(chunk)
        return line, l

    if line[0] != '^':
        raise RuntimeError("No start of line marker")
    if line[-1] != '$':
        raise RuntimeError("No end of line marker")
    line = line[1:-1]

    line, r = _parse_regex(line, True)
    assert line == ''

    return r
    

if __name__ == '__main__':
    main()
