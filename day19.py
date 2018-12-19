#!/usr/bin/python3
import re
from collections import defaultdict

def main():
    lines = """
#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5
""".split("\n")

    with open("day19-input.txt") as f:
        lines = f.readlines()

    ipreg, instructions = parse_program(lines)
    #machine = Machine(ipreg, instructions)
    #part1(machine)
    machine = Machine(ipreg, instructions)
    #machine.regs[0] = 1
    part1(machine)


def part1(machine):
    print("Reg0 is {}".format(machine.run()))
    pass


class Machine():
    def __init__(self, ipreg, instructions):
        self.ipreg = ipreg
        self.instructions = instructions
        self.ip = 0
        self.regs = [0] * 6


    def step(self, debug):
        try:
            (name, inster, args) = self.instructions[self.ip]
        except IndexError:
            return False

        self.regs[self.ipreg] = self.ip
        regs_before = self.regs.copy()
        inst = inster(args[0], args[1], args[2])
        inst.execute(self.regs)
        if debug:
            print("ip={} {} {} {} {}".format(self.ip, regs_before, name, args, self.regs))

        self.ip = self.regs[self.ipreg]
        self.ip += 1
        return True


    def run(self):
        ticks = 0
        report = 100000
        debug = False
        while self.step(debug):
            ticks += 1
            debug = ticks % report == 0
            if ticks > 7577000:
                debug = True
            if debug:
                print("TICK: {}".format(ticks))
        print("Stopping at tick {}".format(ticks))

        return self.regs[0]


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
        b = 0
        if self.name[0:3] != "set":
            b = Instruction._fetch(self.b, self.ib, regs)
        regs[self.c] = self.run(a, b)


    def _fetch(val, immediate, regs):
        if immediate:
            return val
        else:
            return regs[val]


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




def parse_program(lines):
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

    def _parse_instruction(l):
        pattern = r'^(\S+)\s+(\d+)\s+(\d+)\s+(\d+)$'
        match = re.search(pattern, l)
        if not match:
            raise RuntimeError("Can't parse line: {}".format(l))
        name = match.group(1)
        args = [int(s) for s in list(match.groups())[1:]]
        inster = instructions[name]
        return (name, inster, args)

    lines = [l.rstrip() for l in lines if len(l) > 1]

    pattern = r'#ip\s+(\d)'
    match = re.search(pattern, lines[0])
    if not match:
        raise RuntimeError("No declaration on first line: {}".format(lines[0]))
    ipreg = int(match.group(1))

    instructions = [_parse_instruction(l) for l in lines[1:]]

    return (ipreg, instructions)



if __name__ == '__main__':
    main()

