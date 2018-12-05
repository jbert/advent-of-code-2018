#!/usr/bin/python3
import string

def main():
    with open("day5-input.txt") as f:
        polymer = f.readline()

#    polymer = polymer = 'dabAcCaCBAcCcaDA\n'
    polymer = polymer.rstrip('\n')
    polymer = list(polymer)
#    part1(polymer)
    part2(polymer)


def part1(polymer):
    polymer = fully_reduce(polymer)
    print(len(polymer))


def fully_reduce(polymer):
    changed = True
    while changed:
        changed, polymer = reduce(polymer)
#    print("Reduced: {}".format(polymer))
    return polymer


def part2(polymer):
    min_len = len(polymer)
    for c in string.ascii_lowercase:
        filtered = [x for x in polymer if x.lower() != c]
        trimmed = fully_reduce(filtered)
        if len(trimmed) < min_len:
            min_len = len(trimmed)
        print("{}: {}".format(c, len(trimmed)))

    print("min is {}".format(min_len))


def reduce(polymer):
#    print("L {}: {}".format(len(polymer), ''.join(polymer)))
    deletions = []
    i = 0
    l = len(polymer)-1
    while i < l:
        if polymer[i].swapcase() == polymer[i+1]:
            deletions.append(i)
            i += 2
        i += 1

#    print(deletions)
    deletions.reverse()
    for i in deletions:
        del(polymer[i+1])
        del(polymer[i])

    return not not deletions, polymer

if __name__ == "__main__":
    main()
