#!/usr/bin/python3

def main():
    #line = '^WNE$'
    line = '^ENWWW(NEEE|SSE(EE|N))$'

    r = parse_regex(line)
    print(r)


class Regex:
    def __init__(self, toplevel):
        self.r = []
        self.toplevel = toplevel

    def __repr__(self):
        rstr = "".join([str(sr) for sr in self.r])
        if self.toplevel:
            rstr = '^' + rstr + '$'
        return rstr

class Option():
    def __init__(self):
        self.o = []

    def __repr__(self):
        return "(" + "|".join([str(so) for so in self.o]) + ")"

def parse_regex(line):
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
        return line, chunk

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
