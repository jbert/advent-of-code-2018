#!/usr/bin/python3
import string
import time
from collections import deque

def main():

    num_marbles = 25
    for (num_players, num_marbles) in [
            [9, 25],
            [10, 1618],
            [13, 7999],
            [17, 1104],
            [21,6111],
            [30, 5807],
            [448, 71628],
            [448, 7162800],
        ]:
        high_score = part1(num_marbles, num_players)
        print("{}, {}: {}".format(num_players, num_marbles, high_score))


class Circle():
    def __init__(self, num_players):
        self.circle = deque([1, 0])
        self.last_number = 1

        self.num_players = num_players
        self.current_player = 0
        self.scores = [0] * self.num_players


    def move(self):
        self.last_number += 1
        v = self.last_number
        if v % 23 == 0:
            score = v
            self.circle.rotate(7)
            score += self.circle.popleft()

        else:
            self.circle.rotate(-2)
            self.circle.appendleft(v)
#            self.circle.rotate(-1)
            score = 0

        self.scores[self.current_player] += score
        self.current_player = (self.current_player + 1) % self.num_players
        return 1


    def high_score(self):
        return max(self.scores)

    
    def __repr__(self):
        return "{} [{}]: {}".format(self.high_score(), self.current_player+1, self.circle)


def part1(num_marbles, num_players):
    c = Circle(num_players)
    last = time.time()
    last_ops = 0
    interval = 5.0
    for i in range(num_marbles-1):
#        print(c)
        c.move()
        now = time.time()
        if now - last > interval:
            print("{}% {}: {} ops/sec".format((100 * i) // num_marbles, i, (i-last_ops) / interval))
            last = now
            last_ops = i
    return c.high_score()


if __name__ == "__main__":
    main()
