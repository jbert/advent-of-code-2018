#!/usr/bin/python3
import sys

def main():
    #line = '^WNE$'
    sys.setrecursionlimit(100000)
    line = '^ENWWW(NEEE|SSE(EE|N))$'

    with open("day20-input.txt") as f:
        line = f.readline()

    r = parse_regex(line)
    print(r)
    print(r.distance())


class Regex:
    def __init__(self, toplevel):
        self.r = []
        self.toplevel = toplevel

    def __repr__(self):
        rstr = "".join([str(sr) for sr in self.r])
        if self.toplevel:
            rstr = '^' + rstr + '$'
        return rstr

    def distance(self):
        return self._distance

    def set_distance(self):
        self._distance = sum([r.distance() for r in self.r])

class Literal:
    def __init__(self, s):
        self.s = s

    def __repr__(self):
        return self.s

    def distance(self):
        return self._distance

    def set_distance(self):
        self._distance = len(self.s)


class Option():
    def __init__(self):
        self.o = []

    def __repr__(self):
        return "(" + "|".join([str(so) for so in self.o]) + ")"

    def distance(self):
        return self._distance

    def set_distance(self):
        m = min([r.distance() for r in self.o])
        if m == 0:
            self._distance = 0
        else:
            self._distance = max([r.distance() for r in self.o])

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

        r.set_distance()
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
        o.set_distance()
        return line[1:], o


    def _parse_literal(line):
        chunk = ''
        while line and line[0] in news:
            chunk += line[0]
            line = line[1:]
        l = Literal(chunk)
        l.set_distance()
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
