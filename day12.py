#!/usr/bin/python3
import re

def main():
    lines = """initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #""".split('\n')

    with open("day12-input.txt") as f:
        lines = f.readlines()

    state, rules = parse_lines(lines)
    print("state: {}".format(state))
    print("rules: {}".format(rules))
    evo = Evo(state, rules)
    potsum = part1(evo, 200)
    print("potsum: {}".format(potsum))
    potsum = part2()
    print("potsum: {}".format(potsum))


def part2():
    # After gen 99 state is steady, offset increasing
    #  99:  10189
    # 100:  10267 (d=78)
    # 101:  10345 (d=78)
    return 10267 + (50000000000 - 100) * 78
 


def part1(evo, num_generations):
#    seen = set()
    for i in range(num_generations):
        print("{:3}: {:6} {}".format(i, evo.sum_plant_pot_numbers(), evo))
        evo.evolve()
#        s = evo.state_str()
#        if s in seen:
#            print("Repeat at {}".format(i))
#            break
#        seen.add(s)

    return evo.sum_plant_pot_numbers()


EMPTY = ord('.')
PLANT = ord('#')

class Evo():
    def __init__(self, state, rules):
        self.state = bytearray(state.encode('ascii'))
        self.rules = dict([r for r in rules if ord(r[1][0]) == PLANT])
        print("RULES: {}".format(self.rules))
        self.offset = 0


    def evolve(self):
        self.state.insert(0, EMPTY)
        self.state.insert(0, EMPTY)
        self.state.insert(0, EMPTY)
        self.state.insert(0, EMPTY)
        self.offset -=4

        self.state.append(EMPTY)
        self.state.append(EMPTY)
        self.state.append(EMPTY)
        self.state.append(EMPTY)
#        print("EVO: {}".format(self))

        new_state = bytearray(len(self.state))
        new_state [0] = EMPTY
        new_state [1] = EMPTY
        new_state [-1] = EMPTY
        new_state [-2] = EMPTY
        for i in range(2,len(self.state)-2):
            region = self.state[i-2:i+3].decode('ascii')
#            print("REGION: {}".format(region))
            new_state[i] = EMPTY
            if self.rules.get(region):
                new_state[i] = PLANT

        self.state = new_state
        self._state_trim()
        assert self.state[0] == PLANT
        assert self.state[-1] == PLANT


    def state_str(self):
        return self.state.decode('ascii')


    def _state_trim(self):
        l = self.state.index(PLANT)
        r = self.state.rindex(PLANT)
        self.offset += l
        self.state = self.state[l:r+1]


    def __repr__(self):
        return "{:3}: {}".format(self.offset, self.state.decode('ascii'))


    def sum_plant_pot_numbers(self):
        s = 0
        for i, v in enumerate(self.state):
            if v == PLANT:
                s += i + self.offset

        return s


def parse_lines(lines):
    pattern = r'^initial state: ([#\.]*)$'
    match = re.search(pattern, lines[0])
    if not match:
        raise RuntimeError("Can't match initial state: {}".format(lines[0]))
    state = match.group(1)

    rules = []
    pattern = r'^([#\.]{5}) => ([#\.])$'
    for line in lines[2:]:
        match = re.search(pattern, line)
        if not match:
            raise RuntimeError("Can't match rule: {}".format(line))
        rules.append(match.groups())

    return state, rules



if __name__ == '__main__':
    main()
