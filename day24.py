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
    print(battle)
#    print("Immune System:\n{}".format(battle.immune))
#    print("Infection::\n{}".format(battle.infection))
    while not battle.is_finished():
        battle.fight()
    print("\n-----Finished")
    print(battle)


class Battle:
    def __init__(self, immune, infection):
        self.immune = immune
        self.infection = infection


    def __repr__(self):
        msg = ["Immune System:"]
        if len(self.immune) == 0:
            msg.append("No groups remain")
        else:
            msg += [str(g) for g in self.immune]

        msg = ["Infection:"]
        if len(self.infection) == 0:
            msg.append("No groups remain")
        else:
            msg += [str(g) for g in self.infection]

        return "\n".join(msg)


    def is_finished(self):
        return len(self.immune) == 0 or len(self.infection) == 0


    def fight(self):
        print()
        self.infection = sorted(self.infection, key=lambda g: g._target_choose_order())
        self.immune = sorted(self.immune, key=lambda g: g._target_choose_order())
        available = self.immune.copy()
        for g in self.infection:
            g._select_target(available)
        available = self.infection.copy()
        for g in self.immune:
            g._select_target(available)

        fighters = sorted(self.infection + self.immune, key=lambda g: g.initiative)
        for f in fighters:
            if f.is_dead():
                continue
            f._attack_target()


        self.immune = [g for g in self.immune if not g.is_dead()]
        self.infection = [g for g in self.infection if not g.is_dead()]


class Group:
    def __init__(self, gid, gtype, num, hp, traits, dmg, dtype, initiative):
        self.id = gid
        self.gtype = gtype
        self.num = num
        self.hp = hp
        self.dmg = dmg
        self.dtype = dtype
        self.initiative = initiative
        self.target = None

        self.weak = set(traits["weak"])
        self.immune = set(traits["immune"])


    def damage_calc(self, other):
        dmg = self.effective_power()
        if other.weak_to(self.dtype):
            dmg *= 2
        if other.immune_to(self.dtype):
            dmg = 0
        return dmg


    def is_dead(self):
        return self.num <= 0


    def immune_to(self, dtype):
        return dtype in self.immune


    def _attack_target(self):
        if self.target is None:
            return
        print("{} group {} attacks defending group {}".format(self.gtype, self.id, self.target.id))
        dmg = self.damage_calc(self.target)
        self.target.apply_damage(dmg)


    def apply_damage(self, dmg):
        num_killed = dmg // self.hp
        self.num -= num_killed
        print("{} dmg to {} - {} killed {} left".format(dmg, self, num_killed, self.num))


    def weak_to(self, dtype):
        return dtype in self.weak


    def effective_power(self):
        return self.num * self.dmg


    def _select_target(self, available):
        self.target = None
        if not available:
            return available
        self.target = max(available, key=lambda g: self._target_attractiveness(g))
        available = [g for g in available if g.id != self.target.id]
        print("{} group {} would deal defending group {} {} damage".format(self.gtype, self.id, self.target.id, self.damage_calc(self.target)))
        return available


    def _target_attractiveness(self, other):
        return (self.damage_calc(other), other.effective_power(), other.initiative)


    def _target_choose_order(self):
        return (self.effective_power(), self.initiative)


    def __repr__(self):
        target_id = None
        if self.target:
            target_id = self.target.id
        return "Group {}: contains {} groups with {} hp (target: {})".format(self.id, self.num, self.hp, target_id)



def parse_lines(lines):
    lines = [l for l in lines if len(l) > 0]
    if lines[0] != "Immune System:":
        raise RuntimeError("First line wrong? : {}".foramt(lines[0]))
    lines = lines[1:]

    pattern = r"(\d+) units each with (\d+) hit points \(([^\(]+)\) with an attack that does (\d+) (\w+) damage at initiative (\d+)"
    groups = []
    gid = 1
    gtype = 'Immune'
    while lines:
        if lines[0] == "Infection:":
            immune = groups.copy()
            groups = []
            gid = 1
            gtype = 'Infection'
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

        g = Group(gid, gtype, num, hp, tdict, dmg, dtype, initiative)
        groups.append(g)
        lines = lines[1:]
        gid += 1

    infection = groups

    return Battle(immune, infection)




if __name__ == '__main__':
    main()
