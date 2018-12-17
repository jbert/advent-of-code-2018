#!/usr/bin/python3
from re import finditer
from ast import literal_eval

def main():
    buf = """
Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]
"""

    with open("day16-input.txt") as f:
        buf = f.read()

    samples = parse_samples(buf)

    instructions = [
            lambda a, b, c: Instruction("addr", a, False, b, False, c, do_add),
            lambda a, b, c: Instruction("addi", a, False, b, True, c, do_add),

            lambda a, b, c: Instruction("mulr", a, False, b, False, c, do_mul),
            lambda a, b, c: Instruction("muli", a, False, b, True, c, do_mul),

            lambda a, b, c: Instruction("banr", a, False, b, False, c, do_ban),
            lambda a, b, c: Instruction("bani", a, False, b, True, c, do_ban),

            lambda a, b, c: Instruction("borr", a, False, b, False, c, do_bor),
            lambda a, b, c: Instruction("bori", a, False, b, True, c, do_bor),

            lambda a, b, c: Instruction("setr", a, False, b, False, c, do_set),
            lambda a, b, c: Instruction("seti", a, True, b, False, c, do_set),

            lambda a, b, c: Instruction("gtir", a, True, b, False, c, do_gt),
            lambda a, b, c: Instruction("gtri", a, False, b, True, c, do_gt),
            lambda a, b, c: Instruction("gtrr", a, False, b, False, c, do_gt),

            lambda a, b, c: Instruction("eqir", a, True, b, False, c, do_eq),
            lambda a, b, c: Instruction("eqri", a, False, b, True, c, do_eq),
            lambda a, b, c: Instruction("eqrr", a, False, b, False, c, do_eq),
            ]

    triple_match_samples = 0
    for sample in samples:
        print("S: {} -> {} ({})".format(sample.before, sample.after, sample.args))
        num_matches = 0
        for inster in instructions:
            regs = sample.before.copy()
            args = sample.args
            inst = inster(args[1], args[2], args[3])
            inst.execute(regs)
            if regs == sample.after:
                print("Matches: {}".format(inst.name))
                num_matches += 1
        if num_matches >= 3:
            triple_match_samples += 1

    print("{} / {} tms".format(triple_match_samples, len(samples)))



def parse_samples(buf):
#Before: [3, 2, 1, 1]
#9 2 1 2
#After:  [3, 2, 2, 1]
    samples = []
    pattern = r"Before:\s+(.*)\n(.*)\nAfter:\s+(.*)"
#    pattern = r"Before:\s+(\[[^\n]+)[^\n]+\nAfter:\s+(\[[^\n]+)\n"
#    pattern = r"Before: (\[(?:\d+,? ?){4}\])\n\d+ \d+ \d+ \d+\nAfter: (\[(?:\d+,? ?){4}\])\n"
    for match in finditer(pattern, buf):
        before = literal_eval(match.group(1))
        args = [int(s) for s in match.group(2).split(" ")]
        after = literal_eval(match.group(3))
        samples.append(Sample(before, args, after))

    return samples


class Sample():
    def __init__(self, before, args, after):
        self.before = before
        self.args = args
        self.after = after


def do_add(a, b):
    return a + b


def do_mul(a, b):
    return a * b


def do_ban(a, b):
    return a & b


def do_bor(a, b):
    return a | b


def do_set(a, b):
    return a


def do_gt(a, b):
    if a > b:
        return 1
    else:
        return 0


def do_eq(a, b):
    if a == b:
        return 1
    else:
        return 0


class Machine():
    def __init__(self):
        self.regs = [0] * 4
        self.ip = 0

    def step():
        instruction = self.instructions[self.ip]
        self.ip += 1
        instruction.execute(self.regs)


class Instruction():
    def __init__(self, name, a, ia, b, ib, c, run):
        self.name = name
        self.a = a
        self.ia = ia
        self.b = b
        self.ib = ib
        self.c = c
        self.run = run


    def execute(self, regs):
        a = Instruction._fetch(self.a, self.ia, regs)
        b = Instruction._fetch(self.b, self.ib, regs)
        regs[self.c] = self.run(a, b)


    def _fetch(val, immediate, regs):
        if immediate:
            return val
        else:
            return regs[val]


if __name__ == '__main__':
    main()
