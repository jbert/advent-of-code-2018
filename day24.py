#!/usr/bin/python3
import re
from collections import defaultdict

debug = False


def main():
    lines = """
Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
""".split('\n')

    with open("day24-input.txt") as f:
        lines = f.readlines()

#    with open("day24-alternate.txt") as f:
#        lines = f.readlines()

    global debug
#    debug = True
    part1(lines, 0)
    part2(lines)


def part1(lines, boost):
    battle = parse_lines(lines)
    battle.boost_immune(boost)
    print(battle)
    if debug:
        print("Immune System:\n{}".format(battle.immune))
        print("Infection::\n{}".format(battle.infection))
    while not battle.is_finished():
        battle.fight()
        print("\n-----")
        print(battle)
    print("Winning side has: {} units".format(battle.winning_side_units()))


def part2(lines):

    def _immune_win(boost):
        battle = parse_lines(lines)
        battle.boost_immune(boost)
        round = 0
        while not battle.is_finished():
            # if round % 1000:
            #    print("-----")
            #    print(battle)
            battle.fight()
            round += 1
        return len(battle.infection) == 0, battle.winning_side_units()

    for boost in range(1, 100):
        print("{} {}".format(boost, _immune_win(boost)))

    boost = 1
    badlo = 0
    goodhi = 100000
    last_num_units = None
    while True:
        boost = (goodhi-badlo) // 2 + badlo
        print("{} {} {}".format(badlo, goodhi, boost))
        if boost == badlo:
            print("Done! boost {} units {}".format(goodhi, last_num_units))
            break

        result, num_units = _immune_win(boost)
        last_num_units = num_units
        if result:
            goodhi = boost
        else:
            badlo = boost


class Battle:
    def __init__(self, immune, infection):
        self.immune = immune
        self.infection = infection
        self._no_kills_this_turn = False

    def boost_immune(self, boost):
        for u in self.immune:
            u.add_boost(boost)

    def __repr__(self):
        msg = ["Immune System:"]
        if len(self.immune) == 0:
            msg.append("No groups remain")
        else:
            msg += [str(g) for g in self.immune]

        msg.append("Infection:")
        if len(self.infection) == 0:
            msg.append("No groups remain")
        else:
            msg += [str(g) for g in self.infection]

        return "\n".join(msg)

    def winning_side_units(self):
        if len(self.immune) > 0 and len(self.infection) > 0:
            return None

        s = 0
        s += sum([u.num for u in self.immune])
        s += sum([u.num for u in self.infection])

        return s

    def is_finished(self):
        return len(self.immune) == 0 or len(self.infection) == 0 or self._no_kills_this_turn

    def fight(self):
        self._kills_this_turn = False

        def _num_units(g):
            return sum([u.num for u in g])

        before_immune = _num_units(self.immune)
        before_infection = _num_units(self.infection)

        if debug:
            print()

        self.infection = sorted(self.infection, key=lambda g: g._target_choose_order(), reverse=True)
        self.immune = sorted(self.immune, key=lambda g: g._target_choose_order(), reverse=True)

        available = self.immune.copy()
        for g in self.infection:
            available = g._select_target(available)

        available = self.infection.copy()
        for g in self.immune:
            available = g._select_target(available)

        fighters = sorted(self.infection + self.immune, key=lambda g: g.initiative, reverse=True)
        for f in fighters:
            if f.is_dead():
                continue
            f._attack_target()

        self.immune = [g for g in self.immune if not g.is_dead()]
        self.infection = [g for g in self.infection if not g.is_dead()]
        #print(before_immune, before_infection, _num_units(self.immune), _num_units(self.infection))
        self._no_kills_this_turn = (before_immune == _num_units(self.immune) and (before_infection == _num_units(self.infection)))


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

    def add_boost(self, boost):
        self.dmg += boost

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
        if debug:
            print("{} group {} attacks defending group {}".format(self.gtype, self.id, self.target.id))
        dmg = self.damage_calc(self.target)
        self.target.apply_damage(dmg)

    def apply_damage(self, dmg):
        num_killed = dmg // self.hp
        self.num -= num_killed
        if debug:
            print("{} dmg to {} - {} killed {} left".format(dmg, self, num_killed, self.num))

    def weak_to(self, dtype):
        return dtype in self.weak

    def effective_power(self):
        return self.num * self.dmg

    def _select_target(self, available):
        self.target = None
        if not available:
            return available
        target = max(available, key=lambda g: self._target_attractiveness(g))
        if not self.damage_calc(target) > 0:
            return available
        self.target = target
        available = [g for g in available if g.id != self.target.id]
        if debug:
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
    lines = [l.rstrip() for l in lines if len(l) >= 2]
    if lines[0] != "Immune System:":
        raise RuntimeError("First line wrong? : {}".format(lines[0]))
    lines = lines[1:]

    pattern = r"(\d+) units each with (\d+) hit points (?:\(([^\(]+)\) )?with an attack that does (\d+) (\w+) damage at initiative (\d+)"
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

        tdict = defaultdict(list)
        if traits:
            traits = traits.split('; ')
            tpattern = r"(weak|immune) to ([\w ,]+)+"
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
