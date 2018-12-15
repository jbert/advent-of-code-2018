#!/usr/bin/python3
import time

def main():
    test_cases = [(5, '0124515891'), (18, '9251071085'), (2018, '5941429882')]
    for tc in test_cases:
        num_recipes, expected_next_ten = tc
        expected_next_ten = [int(s) for s in expected_next_ten]
        next_ten = part1(num_recipes)
        print("Got {} expected {} ok? {}".format(next_ten, expected_next_ten, next_ten == expected_next_ten))
    num_recipes = 84601 
    answer = part1(num_recipes)
    print("ANSWER for {}: {}".format(num_recipes, ''.join([str(d) for d in answer])))

    def str_to_seq(s):
        return [int(s) for s in seq]

    seq_test_cases = [('51589', 9),('01245', 5),('92510', 18),('59414', 2018)]
    for tc in seq_test_cases:
        seq, expected_found_at = tc
        seq = str_to_seq(seq)
        found_at = part2(seq)
        print("Got {} expected {} ok? {}".format(found_at, expected_found_at, found_at == expected_found_at))

    seq = '084601'
    seq_answer = part2(str_to_seq(seq))
    print("ANSWER for {}: {}".format(seq, seq_answer))

def part1(num_recipes):
    recipes = [3, 7]
    current = [0, 1]
    while len(recipes) < num_recipes + 10:
        current_vals = [recipes[current[0]], recipes[current[1]]]
        recipe_sum = sum(current_vals)
        recipes += [int(s) for s in str(recipe_sum)]
#        print(recipes)
        current = [(c + current_vals[i] + 1) % len(recipes) for i, c in enumerate(current)]

    return recipes[num_recipes:num_recipes+10]


def part2(seq):
    seq = bytearray(seq)
    print("SEQ is {}".format(seq))
    recipes = bytearray()
    recipes.append(3)
    recipes.append(7)
    current = [0, 1]
    last_time = time.time()
    while True:
        current_vals = [recipes[current[0]], recipes[current[1]]]
        recipe_sum = sum(current_vals)
        recipes += bytearray([int(s) for s in str(recipe_sum)])
        len_recipes = len(recipes)
        now = time.time()
        if len_recipes % 100000 == 0:
            print("{}: {}".format(len_recipes, now - last_time))
            last_time = now
#        print(recipes)
        current = [(c + current_vals[i] + 1) % len_recipes for i, c in enumerate(current)]
        try:
#            idx = recipes.rindex(seq)
#            return idx
            idx = recipes[-20:].rindex(seq)
            return len(recipes)-len(recipes[-20:])+idx
        except ValueError:
            pass



if __name__ == '__main__':
    main()
