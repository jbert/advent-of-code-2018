#!/usr/bin/python3
import time
import os
import heapq

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
    part1(game)


def part1(game):

    rounds = 0
    while game.isnt_over():
        rounds += 1
        if rounds % 100:
            os.system("clear")
            print(rounds)
            print(game)
        game.tick()

    print("NO COLLISION!: {}".format(collision))

 

UNIT_ELF    = 'E'
UNIT_GOBLIN = 'G'
MAP_FLOOR   = '.'
MAP_WALL    = '#'


class Unit():
    def __init__(self, pt, c):
        self.pt = pt
        self.c = c


    def char(self):
        return self.c


    def is_enemy(self, other):
        return self.c != other.c


    def __lt__(self, other):
        return self.pt < other.pt


    def __repr__(self):
        return "{}: {}".format(self.pt.x, self.c)


    def move(self, game):
        enemies = game.enemies(self)
        target_pts = [pt for e in enemies for pt in e.pt.adjacent_space(game)]
        # filter target pts by being empty
        target_pts = [pt for pt in target_pts if game.is_empty(pt)]
        # filter by having a path (keep paths)
        paths = [game.shortest_path_between(self.pt, t) for t in target_pts]
        paths = [p for p in paths if p is not None]
        # sort by path length (keep all shortest)
        paths = sorted(paths, key=lambda p: len(p))
        shortest_path_len = len(paths[0])
        paths = [p for p in paths if len(p) == shortest_path_len]
        steps = [p[0] for p in paths]
        steps = sorted(steps)

        print("step is {}".format(steps[0]))
        # produce first steps on shortest paths
        # sort first steps by destination reading order
        # take first step
        raise RuntimeError("a")


class Pt():
    def __init__(self, x, y, c=None):
        self.x = x
        self.y = y
        self.c = c


    def adjacent_space(self, game):
        pts = []
        pts.append(self.add(0, -1))
        pts.append(self.add(-1, 0))
        pts.append(self.add(1, 0))
        pts.append(self.add(0, 1))
        return [p for p in pts if game.contains(p) and game.contents_of(p) == MAP_FLOOR]


    def add(self, x, y):
        return Pt(self.x + x, self.y + y)


    def __repr__(self):
        return "{},{}".format(self.x, self.y)

    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.c == other.c


    def __hash__(self):
        return hash((self.x, self.y, self.c))


    # Reading order
    def __lt__(self, other):
        if self.y < other.y:
            return True
        if self.y > other.y:
            return False
        return self.x < other.x



class Game():
    def __init__(self, lines):
        lines = [l for l in lines if len(l) > 0]
        self.width = len(lines[0])
        self.units = []
        self.state = [self._parse_row(t) for t in enumerate(lines)]
        self.height = len(self.state)
        self.num_elves = len([u for u in self.units if u.c == UNIT_ELF])
        self.num_goblins = len([u for u in self.units if u.c == UNIT_GOBLIN])
        self._sort_units()
        print("width {} height {}".format(self.width, self.height))


    def shortest_path_between(self, start, dest):
        def heuristic(pt):
            # Manhattan distance, ignoring obstacles
            return abs(pt.x - dest.x) + abs(pt.y - dest.y)

        class Node():
            def __init__(self, pt, prev):
                self.pt = pt
                self.prev = prev
                self.l = 0
                if prev:
                    self.l = prev.l + 1
                self.f = heuristic(pt) + self.l

            def __lt__(self, other):
                return self.f < other.f

            def __repr__(self):
                return "{} <- {}".format(self.pt, self.prev)

        print("SPB: --------")
        # Don't go back where we've been
        visited = set()
        visited.add(str(start))
        # Edge we are exploring
        fringe = [Node(start, None)]
        # Kept as a priority queue (sorted by the A-star function 'f' in Node above)
        heapq.heapify(fringe)
        while True:
            print("--------")
            print("V: {}".format((visited)))
            for head in fringe:
                print("F: {}".format(head))

            if not len(fringe) > 0:
                # No path
                return None

            node = heapq.heappop(fringe)
            if node.pt == dest:
                break
            print("POP: {}".format(head))
            next_steps = [Node(next_pt, node) for next_pt in node.pt.adjacent_space(self) if next_pt != node.pt]
            for next_step in next_steps:
                if next_step.pt not in visited:
                    heapq.heappush(fringe, next_step)
                    visited.add(next_step.pt)
                    print("A: {}".format(next_step.pt))

        assert node.pt == dest
        path = []
        while node:
            path.append(node.pt)
            node = node.prev

        path.reverse()
        assert path[0] == start
        return path


    def is_empty(self, pt):
        # Is floor, is not a unit
        u = self.find_unit(pt)
        if u:
            return False
        return self.state[pt.y][pt.x] == MAP_FLOOR


    def contains(self,pt):
        return pt.x > 0 and pt.y > 0 and pt.x < self.width and pt.y < self.height


    def contents_of(self, pt):
        if pt.x < 0 or pt.x > self.width:
            raise RuntimeError("Bad x coord : {}".format(x))
        if pt.y < 0 or pt.y > self.height:
            raise RuntimeError("Bad y coord : {}".format(y))
        u = self.find_unit(pt)
        if u:
            return u
        return self.state[pt.y][pt.x]


    def enemies(self, unit):
        return [u for u in self.units if u.is_enemy(unit)]


    def tick(self, remove=False):
        for unit in self.units:
            unit.move(self)
        self._sort_units()


    def isnt_over(self):
        return self.num_elves > 0 and self.num_goblins > 0


    def remove_unit(self, unit):
        if unit.c == UNIT_ELF:
            self.num_elves -= 1
        elif unit.c == UNIT_GOBLIN:
            self.num_goblins -= 1
        else:
            raise RuntimeError("wtf")

        self.units = [u for u in self.units if not(u.i == unit.i and u.j == unit.j)]


    def _parse_row(self, t):
        j, line = t
        if len(line) != self.width:
            raise RuntimeError("Mismatched line length {}: {} != {}".format(i, len(line), self.width))

        def _parse_unit(t):
            i, c = t
            if c == UNIT_ELF or c == UNIT_GOBLIN:
                self.units.append(Unit(Pt(i, j), c))
                return MAP_FLOOR
            else:
                return c

        return ''.join([_parse_unit(t) for t in enumerate(line)])


    def _sort_units(self):
        self.units = sorted(self.units)


    def find_unit(self, pt, exclude=None):
        for unit in self.units:
            if id(unit) == exclude:
                continue
            if unit.pt.x == pt.x and unit.pt.y == pt.y:
                return unit
            if unit.pt.y > pt.y:      # Carts are sorted, we can stop looking
                break
        return None


    def __repr__(self):
        # Could optimise this, since carts are sorted. But why?
        def _map_char(t, j):
            i, c = t
            unit = self.find_unit(Pt(i, j))
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
