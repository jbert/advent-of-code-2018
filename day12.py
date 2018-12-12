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
    potsum = part1(evo, 20)
    print("potsum: {}".format(potsum))


def part1(evo, num_generations):
    for _ in range(num_generations):
        print(evo)
        print(evo.sum_plant_pot_numbers())
        evo.evolve()

    return evo.sum_plant_pot_numbers()


EMPTY = ord('.')
PLANT = ord('#')

class Evo():
    def __init__(self, state, rules):
        self.state = bytearray(state.encode('ascii'))
        self.rules = dict([r for r in rules if ord(r[1][0]) == PLANT])
        print("RULES: {}".format(self.rules))
        self.left = 0


    def evolve(self):
        self.state.insert(0, EMPTY)
        self.state.insert(0, EMPTY)
        self.left -=2
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
#        self._state_trim()


    def _state_trim(self):
        l = self.state.index(PLANT)
        r = self.state.rindex(PLANT)
        self.left += l
        self.state = self.state[l:r+2]


    def __repr__(self):
        return "{:3}: {}".format(self.left, self.state.decode('ascii'))


    def sum_plant_pot_numbers(self):
        s = 0
        for i, v in enumerate(self.state):
            if v == PLANT:
                s += i + self.left

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
