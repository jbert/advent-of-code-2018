#!/usr/bin/python3
import string
from collections import deque

def main():

    num_marbles = 25
    for (num_players, num_marbles) in [[9, 25], [10, 1618], [13, 7999], [17, 1104], [21,6111], [30, 5807], [448, 71628]]:
        high_score = part1(num_marbles, num_players)
        print("{}, {}: {}".format(num_players, num_marbles, high_score))


class Circle():
    def __init__(self, num_players):
        self.circle = deque([0])
        self.last_number = 0
        self.current = 0        # index, not value

        self.num_players = num_players
        self.current_player = 0
        self.scores = [0] * self.num_players


    def move(self):
        self.last_number += 1
        v = self.last_number
        if v % 23 == 0:
            score = v
            score += self._remove_at(self.current - 7)
        else:
            self._insert_at(self.current + 2, v)
            score = 0

        self.scores[self.current_player] += score
        self.current_player = (self.current_player + 1) % self.num_players
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


    def high_score(self):
        return max(self.scores)

    
    def __repr__(self):
        return "{} [{}]: {} {}".format(self.high_score(), self.current_player+1, self.circle[self.current], self.circle)


def part1(num_marbles, num_players):
    c = Circle(num_players)
    for i in range(num_marbles-1):
#        print(c)
        c.move()
    return c.high_score()


if __name__ == "__main__":
    main()
