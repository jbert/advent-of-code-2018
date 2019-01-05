#!/usr/bin/python3
import sys
from queue import Queue
from itertools import count


def main():
    line = '^WNE$'
    sys.setrecursionlimit(100000)
    line = '^ENWWW(NEEE|SSE(EE|N))$'

    line = '^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$'

    line = '^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$'
#    with open("day20-input.txt") as f:
#        line = f.readline()

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
        start = self.rooms[Pos(0, 0).location()]

        todo = Queue()
        todo.put((start, 0, None))
        seen = set()
        seen.add(start)

        max_distance = 0
        while not todo.empty():
            (room, distance, direction) = todo.get()
            print("visit {} dist {} dir {}".format(room, distance, direction))
            if distance > max_distance:
                max_distance = distance
            for adjacent_room in room.adjacent:
                if adjacent_room not in seen:
                    todo.put((adjacent_room, distance + 1, room.pos.direction_to(adjacent_room.pos)))
                    seen.add(adjacent_room)

        return max_distance

    def __repr__(self):
        lines = ['#' * (2 * (self.maxx - self.minx) + 3)]
        for y in range(self.miny, self.maxx+1):
            room_line = '#'
            wall_line = '#'
            for x in range(self.minx, self.maxx+1):
                p = Pos(x, y)
                r = self.rooms[p.location()]
                doors = r.doors()
                room_line += 'X' if x == 0 and y == 0 else '.'
                wall_line += '-1G' if 'S' in doors else '#'
                room_line += '|' if 'E' in doors else '#'
                wall_line += '#'
            lines.append(room_line)
            lines.append(wall_line)
        return "\n".join(lines)

    def _build(self):
        idx_iter = count(1, 1)
        rooms = dict()

        self.minx = 0
        self.maxx = 0
        self.miny = 0
        self.maxy = 0

        def _f(pos, old_loc):
            self.minx = min(self.minx, pos.x)
            self.miny = min(self.miny, pos.y)
            self.maxx = max(self.maxx, pos.x)
            self.maxy = max(self.maxy, pos.y)

            loc = pos.location()
            try:
                room = rooms[loc]
            except KeyError:
                room = Room(pos, idx_iter)
                rooms[loc] = room

            old_room = rooms[old_loc]

            old_room.join(room)

        p = Pos(0, 0, _f)
        rooms[p.location()] = Room(p, idx_iter)
        self.r.walk(p)

        self.rooms = rooms


class Room:
    def __init__(self, pos, idx_iter):
        self.idx = next(idx_iter)
        self.adjacent = set()
        self.pos = pos.copy()
        print("NEW ROOM: {}".format(self))

    def join(self, other):
        self.adjacent.add(other)
        other.adjacent.add(self)
        print("JOIN {} <-> {}".format(self, other))
        assert self.pos.is_adjacent(other.pos)

    def __eq__(self, other):
        return self.idx == other.idx

    def __hash__(self):
        return self.idx

    def __repr__(self):
        return "R: {} {} {}".format(self.idx, self.pos, sorted(map(lambda r: r.idx, list(self.adjacent))))

    def doors(self):
        return set([self.pos.direction_to(a.pos) for a in self.adjacent])


class Pos():
    def __init__(self, x, y, f=None):
        self.x = x
        self.y = y
        self.f = f

    def n(self):
        old_loc = self.location()
        self.y -= 1
        self.f(self, old_loc)

    def s(self):
        old_loc = self.location()
        self.y += 1
        self.f(self, old_loc)

    def w(self):
        old_loc = self.location()
        self.x -= 1
        self.f(self, old_loc)

    def e(self):
        old_loc = self.location()
        self.x += 1
        self.f(self, old_loc)

    def __repr__(self):
        return "{},{}".format(self.x, self.y)

    def location(self):
        return "{},{}".format(self.x, self.y)

    def save(self):
        self._save_x = self.x
        self._save_y = self.y

    def restore(self):
        self.x = self._save_x
        self.y = self._save_y

    def is_adjacent(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) == 1

    def copy(self):
        return Pos(self.x, self.y)

    def direction_to(self, other):
        assert self.is_adjacent(other)
        if self.x == other.x:
            return 'N' if other.y < self.y else 'S'
        return 'W' if other.x < self.x else 'E'


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
        lit = Literal(chunk)
        return line, lit

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
