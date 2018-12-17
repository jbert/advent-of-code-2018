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
    program = parse_program(buf)

    instructions = {
            "addr": lambda a, b, c: Instruction("addr", a, False, b, False, c, do_add),
            "addi": lambda a, b, c: Instruction("addi", a, False, b, True, c, do_add),

            "mulr": lambda a, b, c: Instruction("mulr", a, False, b, False, c, do_mul),
            "muli": lambda a, b, c: Instruction("muli", a, False, b, True, c, do_mul),

            "banr": lambda a, b, c: Instruction("banr", a, False, b, False, c, do_ban),
            "bani": lambda a, b, c: Instruction("bani", a, False, b, True, c, do_ban),

            "borr": lambda a, b, c: Instruction("borr", a, False, b, False, c, do_bor),
            "bori": lambda a, b, c: Instruction("bori", a, False, b, True, c, do_bor),

            "setr": lambda a, b, c: Instruction("setr", a, False, b, False, c, do_set),
            "seti": lambda a, b, c: Instruction("seti", a, True, b, False, c, do_set),

            "gtir": lambda a, b, c: Instruction("gtir", a, True, b, False, c, do_gt),
            "gtri": lambda a, b, c: Instruction("gtri", a, False, b, True, c, do_gt),
            "gtrr": lambda a, b, c: Instruction("gtrr", a, False, b, False, c, do_gt),

            "eqir": lambda a, b, c: Instruction("eqir", a, True, b, False, c, do_eq),
            "eqri": lambda a, b, c: Instruction("eqri", a, False, b, True, c, do_eq),
            "eqrr": lambda a, b, c: Instruction("eqrr", a, False, b, False, c, do_eq),
            }

    part1(samples, instructions.values())
    part2(samples, instructions, program)


def part2(samples, instructions, program):

    isa = discover_opcodes(samples, instructions)
    regs = [0] * 4
    for args in program:
        opcode = args[0]
        inst_name = isa[opcode]
        inster = instructions[inst_name]
        inst = inster(args[1],args[2],args[3])
        inst.execute(regs)

    print("REG 0: {}".format(regs[0]))


def discover_opcodes(samples, instructions):
    opcode_options = [set(instructions.keys()).copy() for _ in range(16)]

    print("Got {} samples".format(len(samples)))
    for sample in samples:
        print(sample)
        args = sample.args
        opcode = args[0]
        options = opcode_options[opcode].copy()
        if len(options) > 1:
            for name in options:
                inster = instructions[name]
                inst = inster(args[1], args[2], args[3])
                regs = sample.before.copy()
                inst.execute(regs)
                if regs != sample.after:
                    #print("F: {} {}".format(opcode, name))
                    opcode_options[opcode].remove(name)
                #else:
                    #print("S: {} {}".format(opcode, name))

    for opcode, options in enumerate(opcode_options):
        print("{} => {}".format(opcode, options))

    done = False
    while not done:
#        for opcode, options in enumerate(opcode_options):
#            print("{} => {}".format(opcode, options))

        done = True
        # Take a copy for iteration
        for opcode, options in enumerate(opcode_options.copy()):
            if len(options) == 1:
                name = list(options)[0]
                for to_remove_opcode in range(16):
                    if opcode != to_remove_opcode:
                        try:
                            opcode_options[to_remove_opcode].remove(name)
                        except KeyError:
                            pass
            else:
                # We've seen a > 1, we aren't done yet
                done = False

    isa = [None] * 16
    for opcode, options in enumerate(opcode_options):
        assert len(options) == 1
        print("{} => {}".format(opcode, options))
        isa[opcode] = list(options)[0]

    return isa



def part1(samples, instructions):
    triple_match_samples = 0
    for sample in samples:
        #print("S: {} -> {} ({})".format(sample.before, sample.after, sample.args))
        num_matches = 0
        for inster in instructions:
            regs = sample.before.copy()
            args = sample.args
            inst = inster(args[1], args[2], args[3])
            inst.execute(regs)
            if regs == sample.after:
                #print("Matches: {}".format(inst.name))
                num_matches += 1
        if num_matches >= 3:
            triple_match_samples += 1

    print("{} / {} tms".format(triple_match_samples, len(samples)))



def parse_program(buf):
    def _parse_line(l):
        return [int(s) for s in l.split(" ")]

    start = buf.rindex("After:")
    buf = buf[start:]
    start = buf.index("\n\n")
    buf = buf[start:]
    return [_parse_line(l) for l in buf.split("\n") if len(l) > 0]


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


    def __repr__(self):
        return "{} -> {} ({})".format(self.before, self.after, self.args)


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
