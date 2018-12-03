#!/usr/bin/python3

with open("day2-input.txt") as f:
    lines = f.readlines()

two_ers = 0
three_ers = 0
for id in lines:
    letter_count = dict()
    for c in id:
        letter_count.setdefault(c, 0)
        letter_count[c] += 1
    freqs = [None] * len(id)
    for letter, count in letter_count.items():
        freqs[count] = True

#    print(id)
    if freqs[2]:
#        print("Has a two")
        two_ers += 1
    if freqs[3]:
#        print("Has a three")
        three_ers += 1

print(two_ers * three_ers)


def hamming(a, b):
    if len(a) != len(b):
        raise RuntimeError("bad len")
    delta = 0
    same = list()
    for i in range(0, len(a)):
        if a[i] == b[i]:
            same.append(a[i])
        else:
            delta += 1

    return delta, ''.join(same)


for a in lines:
    for b in lines:
        delta, same = hamming(a, b)
        if delta == 1:
            print(same)

