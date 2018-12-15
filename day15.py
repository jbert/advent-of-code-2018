#!/usr/bin/python3
import time

def main():
    lines = """#########
#G..G..G#
#.......#
#.......#
#G..E..G#
#.......#
#.......#
#G..G..G#
#########""".split("\n")

    game = Game(lines)
    print(game)


UNIT_ELF    = 'E'
UNIT_GOBLIN = 'G'
MAP_FLOOR   = '.'
MAP_WALL    = '#'


class Unit():
    def __init__(self, i, j, c):
        self.i = i
        self.j = j
        self.c = c


    def char(self):
        return self.c


    def __repr__(self):
        return "{},{}: {}".format(self.i, self.j, self.c)


class Game():
    def __init__(self, lines):
        self.width = len(lines[0])
        self.units = []
        self.state = [self._parse_row(t) for t in enumerate(lines)]
        self.height = len(self.state)
        self._sort_units()
        print("width {} height {}".format(self.width, self.height))


    def tick(self, remove=False):
        for unit in self.units:
            unit.move(self.state)
        self._sort_units()


    def _parse_row(self, t):
        j, line = t
        if len(line) != self.width:
            raise RuntimeError("Mismatched line length {}: {} != {}".format(i, len(line), self.width))

        def _parse_unit(t):
            i, c = t
            if c == UNIT_ELF or c == UNIT_GOBLIN:
                self.units.append(Unit(i, j, c))
                return MAP_FLOOR
            else:
                return c

        return ''.join([_parse_unit(t) for t in enumerate(line)])


    def _sort_units(self):
        # Top first, then left to right
        self.units = sorted(self.units, key=lambda u: (u.j, u.i))


    def find_unit(self, i, j, exclude=None):
        for unit in self.units:
            if id(unit) == exclude:
                continue
            if unit.i == i and unit.j == j:
                return unit
            if unit.j > j:      # Carts are sorted, we can stop looking
                break
        return None


    def __repr__(self):
        # Could optimise this, since carts are sorted. But why?
        def _map_char(t, j):
            i, c = t
            unit = self.find_unit(i, j)
            if unit is not None:
                return unit.char()
            else:
                return c

        map = ''
        for j in range(self.height):
            map += ''.join([_map_char(t, j) for t in enumerate(self.state[j])])
            map += '\n'
#        map = "\n".join(self.state)
        units = '\n'.join([str(unit) for unit in self.units])
        return map + "\n" + units


if __name__ == '__main__':
    main()
