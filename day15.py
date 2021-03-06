#!/usr/bin/python3
import time
import os
import heapq

def main():
    lines = """
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######
""".split("\n")

    with open("day15-input.txt") as f:
        lines = f.readlines()

    game = Game(lines)
#    part1(game, True)
    part2(lines)


def part2(lines):
    elf_attack_power = 4
    while True:
        game = Game(lines, elf_attack_power)
        rounds = 0
        num_elves = game.num_elves
        while True:
            all_units_moved = game.tick()
            if all_units_moved:
                rounds += 1
            os.system("clear")
            print("EP: {}".format(elf_attack_power))
            print(game)

            if game.num_elves < num_elves:
                break
            if game.num_goblins == 0:
                hp_sum = sum([u.hp for u in game.units])
                outcome = hp_sum * rounds
                print("Done! EP {} rounds {} hp sum {} outcome {}".format(elf_attack_power, rounds, hp_sum, outcome))
                return
        elf_attack_power += 1


def part1(game, clear=False):

    rounds = 0
    last_time = time.time()
    now = last_time
    hp_sum = sum([u.hp for u in game.units])
    while game.isnt_over():
        print("--------")
        print("Rounds {}: {} elves {} goblins {} hpsum {:5} sec".format(rounds, game.num_elves, game.num_goblins, hp_sum, now - last_time))
        print(game)
        last_time = now
        all_units_moved = game.tick()
        hp_sum = sum([u.hp for u in game.units])
        now = time.time()
        if all_units_moved:
            rounds += 1
        else:
            break
        if clear:
            os.system("clear")
        else:
            print("-" * 40)
#        input("Tick...")

    print("Rounds {}: {} elves {} goblins {} hpsum {:5} sec".format(rounds, game.num_elves, game.num_goblins, hp_sum, now - last_time))
    print(game)
    outcome = hp_sum * rounds
    print("hp sum {} round {} outcome {}".format(hp_sum, rounds, outcome))
    return (rounds, hp_sum, outcome)

 

UNIT_ELF    = 'E'
UNIT_GOBLIN = 'G'
MAP_FLOOR   = '.'
MAP_WALL    = '#'


class Unit():
    def __init__(self, pt, c):
        self.pt = pt
        self.c = c
        self.hp = 200
        self.attack_power = 3

    def dead(self):
        return self.hp <= 0

    def char(self):
        return self.c


    def is_enemy(self, other):
        return self.c != other.c


    def enemy(self):
        if self.c == UNIT_ELF:
            return UNIT_GOBLIN
        elif self.c == UNIT_GOBLIN:
            return UNIT_ELF
        else:
            raise RuntimeError("wtf")


    def __lt__(self, other):
        return self.pt < other.pt


    def __repr__(self):
        return "{}: {} - {}".format(self.c, self.pt, self.hp)


    def move(self, game):
        attackable_enemies = game.adjacent_enemies(self)
        #print("SELF {} : AE - {}".format(self, attackable_enemies))
        if not attackable_enemies:
            enemies = game.enemies(self)
            if enemies:
                did_move = True
                self._do_move(game, enemies)
                attackable_enemies = game.adjacent_enemies(self)
            else:
                did_move = False
        if attackable_enemies:
            self._do_attack(game, attackable_enemies)
            did_move = True

        return did_move

    def _do_attack(self, game, attackable_enemies):
        min_hp = min(attackable_enemies, key=lambda e: e.hp).hp
        attackable_enemies = [ae for ae in attackable_enemies if ae.hp == min_hp]
        attackable_enemies = sorted(attackable_enemies)
        enemy = attackable_enemies[0]
        enemy.hp -= self.attack_power
        if enemy.dead():
            game.remove_unit(enemy)
        #print("{} attack {}".format(self, enemy))


    def _breadth_first_search(self, game, target_pts):
        target_set = set(target_pts)

        first_steps = game.adjacent_spaces(self.pt)
        for first_step in first_steps:
            if first_step in target_set:
                return (first_step, first_step)

        fringe = [(step, step) for step in first_steps]
        seen = set()
        #print("BFS {} -> {}".format(self.pt, target_pts))
        while fringe:
            #print("F: {}".format(fringe))
            #print("S: {}".format(sorted(list(seen))))
            new_fringe = []
            for t in fringe:
                (pt, first_step) = t
                steps = [(p, first_step) for p in game.adjacent_spaces(pt) if p not in seen]
                for (pt, _) in steps:
                    seen.add(pt)
                hits = []
                for (pt, first_step) in steps:
                    #print("JB test {} in {}".format(pt, target_set))
                    if pt in target_set:
                        #print("HIT")
                        hits.append((pt, first_step))
                if hits:
                    hits = sorted(hits)
                    #print("RET {}".format(hits[0]))
                    return hits[0]

                new_fringe += steps

            fringe = new_fringe

        return None

    def _do_move(self, game, enemies):
        # filter target pts by being empty
        target_pts = sorted([pt for e in enemies for pt in game.adjacent_spaces(e.pt)])
        # filter by having a path (keep paths)


        # Breadth-first search of pts, tagging each with the start step
        hit = self._breadth_first_search(game, target_pts)
        if not hit:
            return 
        (target, step) = hit

        assert game.is_empty(step)
        assert target in target_pts

        # take first step
        #print("{} move {}".format(self, steps[0]))
        game.move_unit(self, step)


class Pt():
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def manhattan(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)


    def add(self, x, y):
        return Pt(self.x + x, self.y + y)


    def __repr__(self):
        return "{},{}".format(self.x, self.y)

    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


    def __hash__(self):
        return hash((self.x, self.y))


    # Reading order
    def __lt__(self, other):
        if self.y < other.y:
            return True
        if self.y > other.y:
            return False
        return self.x < other.x



class Game():
    def __init__(self, lines, elf_attack_power=3):
        lines = [l.rstrip() for l in lines if len(l) > 0]
        self.width = len(lines[0])
        self.units = []
        self.state = [self._parse_row(t) for t in enumerate(lines)]
        self.height = len(self.state)
        self.num_elves = len([u for u in self.units if u.c == UNIT_ELF])
        self.num_goblins = len([u for u in self.units if u.c == UNIT_GOBLIN])
        for u in self.units:
            if u.c == UNIT_ELF:
                u.attack_power = elf_attack_power
        self._sort_units()

    def move_unit(self, unit, dest):
        unit.pt = dest
        self._sort_units()

    def contains(self,pt):
        return pt.x > 0 and pt.y > 0 and pt.x < self.width and pt.y < self.height


    def adjacent_pts(self, pt):
        pts = []
        pts.append(pt.add(0, -1))
        pts.append(pt.add(-1, 0))
        pts.append(pt.add(1, 0))
        pts.append(pt.add(0, 1))
        return [p for p in pts if self.contains(p)]


    def adjacent_enemies(self, unit):
        pts = self.adjacent_pts(unit.pt)
        return [self.find_unit(p) for p in pts if self.contents_of(p) == unit.enemy()]


    def adjacent_spaces(self, pt):
        pts = self.adjacent_pts(pt)
        return [p for p in pts if self.is_empty(p)]


    def shortest_paths_to(self, start, targets):
        # The heuristic is a lower bound on the distance
        # Path to the targets - heuristic-nearest first
        # Cull any targets who are heuristic-further than the current shortest path
        # - they cannot be closer
        targets = sorted(targets, key=lambda p: p.manhattan(start))
        paths = []
        while targets:
            dest = targets[0]
            del(targets[0])
            path = self.shortest_path_between(start, dest)
            if path:
                paths.append(path)
                path_len = len(path)
                targets = [t for t in targets if t.manhattan(start) <= path_len]

        return paths

    def shortest_path_between(self, start, dest):
        def heuristic(pt, prev):
            # We 'reading order' step:
            # so weight 0,1,2,3 for up/left/right/down
            weight = 0
            if prev:
                prev_pt = prev.pt
                if pt.y < prev_pt.y:
                    weight = 0
                elif pt.y > prev_pt.y:
                    weight = 3
                elif pt.x < prev_pt.x:
                    weight = 1
                else:
                    weight = 2
            return weight + dest.manhattan(pt)

        class Node():
            def __init__(self, pt, prev):
                self.pt = pt
                self.prev = prev
                self.l = 0
                if prev:
                    self.l = prev.l + 1
                self.f = heuristic(pt, prev) + self.l

            def __lt__(self, other):
                if self.f < other.f:
                    return True
                if self.f > other.f:
                    return False
                return self.pt < other.pt

            def __repr__(self):
                return "{} f {} <- {}".format(self.pt, self.f, self.prev)

        # Don't go back where we've been
        visited = set()
        visited.add(start)
        # Edge we are exploring
        fringe = [Node(start, None)]
        # Kept as a priority queue (sorted by the A-star function 'f' in Node above)
        heapq.heapify(fringe)
        while True:
            #print("F: {}".format(fringe))
            if not len(fringe) > 0:
                # No path
                return None

            node = heapq.heappop(fringe)
            #print("N: {}".format(node))
            if node.pt == dest:
                break
            next_steps = [Node(next_pt, node) for next_pt in self.adjacent_spaces(node.pt) if next_pt != node.pt]
            #print("NS: {}".format(next_steps))
            for next_step in next_steps:
                if next_step.pt not in visited:
                    heapq.heappush(fringe, next_step)
                    visited.add(next_step.pt)
                    #print("A: {}".format(next_step.pt))

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


    def contents_of(self, pt):
        if pt.x < 0 or pt.x > self.width:
            raise RuntimeError("Bad x coord : {}".format(x))
        if pt.y < 0 or pt.y > self.height:
            raise RuntimeError("Bad y coord : {}".format(y))
        u = self.find_unit(pt)
        if u:
            return u.c
        return self.state[pt.y][pt.x]


    def enemies(self, unit):
        return [u for u in self.units if u.is_enemy(unit)]


    def tick(self):
        all_did_move = True
        for unit in self.units:
            if unit.dead():
                continue
            did_move = unit.move(self)
            if not did_move:
                all_did_move = False
                break
        self._sort_units()
        return all_did_move


    def isnt_over(self):
        return self.num_elves > 0 and self.num_goblins > 0


    def remove_unit(self, unit):
        if unit.c == UNIT_ELF:
            self.num_elves -= 1
        elif unit.c == UNIT_GOBLIN:
            self.num_goblins -= 1
        else:
            raise RuntimeError("wtf")

        self.units = [u for u in self.units if not(u.pt == unit.pt)]


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

        sorted_units = self.units.copy()

        map = ''
        for j in range(self.height):
            map += ''.join([_map_char(t, j) for t in enumerate(self.state[j])])
            map += '\t'
            while sorted_units and sorted_units[0].pt.y == j:
                u = sorted_units[0]
                del(sorted_units[0])
                map += str(u) + ", "
            map += '\n'
    #        map = "\n".join(self.state)
        return map
#        units = '\n'.join([str(unit) for unit in self.units])
#        return map + "\n" + units


if __name__ == '__main__':
    main()
