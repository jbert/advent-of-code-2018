#!/usr/bin/python3
import re
from collections import defaultdict

def main():
    lines = """
Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
""".split('\n')

    battle = parse_lines(lines)
    part1(battle)


def part1(battle):
    print("Immune System:\n{}".format(battle.immune))
    print("Infection::\n{}".format(battle.infection))


class Battle:
    def __init__(self, immune, infection):
        self.immune = immune
        self.infection = infection


class Group:
    def __init__(self, num, hp, traits, dmg, dtype, initiative):
        self.num = num
        self.hp = hp
        self.traits = traits
        self.dmg = dmg
        self.dtype = dtype


    def __repr__(self):
        return "{} groups with {} hp".format(self.num, self.hp)


def parse_lines(lines):
    lines = [l for l in lines if len(l) > 0]
    if lines[0] != "Immune System:":
        raise RuntimeError("First line wrong? : {}".foramt(lines[0]))
    lines = lines[1:]

    pattern = r"(\d+) units each with (\d+) hit points \(([^\(]+)\) with an attack that does (\d+) (\w+) damage at initiative (\d+)"
    groups = []
    while lines:
        if lines[0] == "Infection:":
            immune = groups.copy()
            groups = []
            lines = lines[1:]
        match = re.search(pattern, lines[0])
        if not match:
            raise RuntimeError("Didn't match : {}".format(lines[0]))
        num, hp, traits, dmg, dtype, initiative = match.groups()
        num, hp, dmg, initiative = map(int, [num, hp, dmg, initiative])

        traits = traits.split('; ')
        tpattern = r"(weak|immune) to ([\w ,]+)+"
        tdict = defaultdict(list)
        for trait in traits:
            tmatch = re.search(tpattern, trait)
            if not match:
                raise RuntimeError("Didn't match : {}".format(trait))
            trait_type, twords = tmatch.groups()
            tdict[trait_type] += twords.split(", ")

        g = Group(num, hp, tdict, dmg, dtype, initiative)
        groups.append(g)
        lines = lines[1:]

    infection = groups

    return Battle(immune, infection)




if __name__ == '__main__':
    main()
