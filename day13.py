#!/usr/bin/python3
import re
import os
from collections import deque
import time

def main():
    lines = r"""/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   """.split('\n')

    with open("day13-input.txt") as f:
        lines = f.readlines()

    runner = Runner(lines)
    part1(runner)
    part2(runner)


def part1(runner):
    steps = 0
    while True:
        steps += 1
        if steps % 100:
            print(steps)
#        os.system("clear")
#        print(runner)
        collision = runner.tick()
        if collision:
            break

    print("NO COLLISION!: {}".format(collision))

 
def part2(runner):
    steps = 0
    while True:
        steps += 1
        if steps % 100:
            print(steps)
#        os.system("clear")
#        print(runner)
        runner.tick(True)
        if len(runner.carts) < 2:
            break

    print("LAST CART STANDING!: {}".format(runner.carts[0]))
 

TURN_LEFT       = 0
TURN_RIGHT      = 1
TURN_STRAIGHT   = 2

class Cart():
    def __init__(self,i,j,c):
        self.i = i
        self.j = j
        self.c = c
        self.turns = deque([TURN_LEFT, TURN_STRAIGHT, TURN_RIGHT])


    def char(self):
        return self.c


    def __repr__(self):
        return "{},{}: {}".format(self.i, self.j, self.c)


    def move(self, state):
#        print("{} moving".format(self))
        if self.c == CART_UP:
            self.j -= 1
        elif self.c == CART_DOWN:
            self.j += 1
        elif self.c == CART_LEFT:
            self.i -= 1
        elif self.c == CART_RIGHT:
            self.i += 1
        else:
            raise RuntimeError("WTF? [{}]".format(self.c))

        track = state[self.j][self.i]
        self._turn(track)


    def _turn(self, track):
#        print("{}: {}".format(self, track))
        if track == TRACK_VERT:
            assert self.c == CART_UP or self.c == CART_DOWN
        elif track == TRACK_HORIZ:
            assert self.c == CART_LEFT or self.c == CART_RIGHT
        elif track == TRACK_CTL:
            if self.c == CART_UP:
                self.c = CART_LEFT
            elif self.c == CART_DOWN:
                self.c = CART_RIGHT
            elif self.c == CART_RIGHT:
                self.c = CART_DOWN
            elif self.c == CART_LEFT:
                self.c = CART_UP
            else:
                raise RuntimeError("Whoops cart [{}] track [{}]".format(self.c, track))
        elif track == TRACK_CTR:
            if self.c == CART_UP:
                self.c = CART_RIGHT
            elif self.c == CART_DOWN:
                self.c = CART_LEFT
            elif self.c == CART_LEFT:
                self.c = CART_DOWN
            elif self.c == CART_RIGHT:
                self.c = CART_UP
            else:
                raise RuntimeError("Whoops cart [{}] track [{}]".format(self.c, track))
        elif track == TRACK_INTER:
            turn = self.turns[0]
            self.turns.rotate(-1)
            if turn == TURN_LEFT:
                self._turn_left()
            elif turn == TURN_RIGHT:
                # Two wrongs don't make a right...
                self._turn_left()
                self._turn_left()
                self._turn_left()
            elif turn == TURN_STRAIGHT:
                # If a tree turns in a forest...
                pass
            else:
                raise RuntimeError("wtf?")
        else:
            raise RuntimeError("{}: Unknown track [{}]".format(self, track))

#        print("Turn return with self {}".format(self))


    def _turn_left(self):
        order = '<v>^<'
        idx = order.index(self.c)
        self.c = order[idx+1]



CART_UP     = '^'
CART_DOWN   = 'v'
CART_LEFT   = '<'
CART_RIGHT  = '>'
TRACK_VERT  = '|'
TRACK_HORIZ = '-'
TRACK_INTER = '+'
TRACK_CTL = '\\'
TRACK_CTR = '/'

class Runner():
    def __init__(self, lines):
        self.width = len(lines[0])
        self.carts = []
        self.state = [self._parse_row(t) for t in enumerate(lines)]
        self.height = len(self.state)
        self._sort_carts()
        print("width {} height {}".format(self.width, self.height))


    def tick(self, remove=False):
        for cart in self.carts:
            cart.move(self.state)
            if self.find_cart(cart.i, cart.j, id(cart)):
                if remove:
                    self.carts = [c for c in self.carts if not(c.i == cart.i and c.j == cart.j)]
                else:
                    return cart
        self._sort_carts()

        return None

    def _parse_row(self, t):
        j, line = t
        if len(line) != self.width:
            raise RuntimeError("Mismatched line length {}: {} != {}".format(i, len(line), self.width))

        def _parse_cart(t):
            i, c = t
            if c == CART_UP or c == CART_DOWN:
                self.carts.append(Cart(i, j, c))
                return TRACK_VERT
            elif c == CART_LEFT or c == CART_RIGHT:
                self.carts.append(Cart(i, j, c))
                return TRACK_HORIZ
            else:
                return c

        return ''.join([_parse_cart(t) for t in enumerate(line)])


    def _sort_carts(self):
        # Top first, then left to right
        self.carts = sorted(self.carts, key=lambda c: (c.j, c.i))


    def find_cart(self, i, j, exclude=None):
        for cart in self.carts:
            if id(cart) == exclude:
                continue
            if cart.i == i and cart.j == j:
                return cart
            if cart.j > j:      # Carts are sorted, we can stop looking
                break
        return None


    def __repr__(self):
        # Could optimise this, since carts are sorted. But why?
        def _map_char(t, j):
            i, c = t
            cart = self.find_cart(i, j)
            if cart is not None:
                return cart.char()
            else:
                return c

        map = ''
        for j in range(self.height):
            map += ''.join([_map_char(t, j) for t in enumerate(self.state[j])])
            map += '\n'
#        map = "\n".join(self.state)
        carts = '\n'.join([str(cart) for cart in self.carts])
        return map + "\n" + carts



if __name__ == '__main__':
    main()
