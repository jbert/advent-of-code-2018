#!/usr/bin/python3
import string
from collections import deque

def main():

    num_marbles = 25
    num_players = 9
    part1(num_marbles, num_players)


class Circle():
    def __init__(self, num_players):
        self.circle = deque([0])
        self.last_number = 0
        self.current = 0        # index, not value

        self.num_players = num_players
        self.next_player = 0


    def move(self):
        self.last_number += 1
        v = self.last_number
        if v % 23 == 0:
            v = self._remove_at(self.current - 7)
        else:
            self._insert_at(self.current + 2, v)
        return 1


    def _remove_at(self, pos):
        pos = pos % len(self.circle)
        v = self.circle[pos]
        del(self.circle[pos])
        self.current = pos
        return v


    def _insert_at(self, pos, v):
        pos = pos % len(self.circle)
        self.circle.insert(pos, v)
        self.current = pos

    
    def __repr__(self):
        return "{}: {}".format(self.circle[self.current], self.circle)


def part1(num_marbles, num_players):
    c = Circle(num_players)
    while True:
        c.move()
        print(c)



if __name__ == "__main__":
    main()
