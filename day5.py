#!/usr/bin/python3

def main():
    with open("day5-input.txt") as f:
        polymer = f.readline()

#    polymer = polymer = 'dabAcCaCBAcCcaDA\n'
    polymer = polymer.rstrip('\n')
    polymer = list(polymer)
    part1(polymer)

def part1(polymer):
    changed = True
    while changed:
        print(len(polymer))
        changed, polymer = reduce(polymer)
#    print("Reduced: {}".format(polymer))


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
