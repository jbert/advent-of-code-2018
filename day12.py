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

    state, rules = parse_lines(lines)
    print("state: {}".format(state))
    print("rules: {}".format(rules))
    #part1(state, rules, 20)


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
