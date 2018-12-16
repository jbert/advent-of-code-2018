from day15 import Game, Pt, Unit, part1


def test_outcome():
    testcases = [
            ("""
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######
""", 47, 590, 27730),
            ("""
#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######
""", 37, 982, 36334),
            ("""
#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######
""", 46, 859, 39514),
            ("""
#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######
""", 35, 793, 27755),
            ("""
#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######
""", 54, 536, 28944),
            ("""
#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########
""", 20, 937, 18740),
            ]
    for tc in testcases:
        (lines, expected_rounds, expected_hp_sum, expected_outcome) = tc
        lines = lines.split("\n")
        game = Game(lines)
        (rounds, hp_sum, outcome) = part1(game)
        assert(rounds == expected_rounds)
        assert(hp_sum == expected_hp_sum)
        assert(outcome == expected_outcome)

def test_path():
    testcases = [
            (Pt(1,1), Pt(2,2), 3, """
####
#..#
#..#
####"""),

            (Pt(1,1), Pt(3,3),  5, """
#####
#...#
#...#
#...#
#####"""),
            (Pt(1,1), Pt(3,3),  5, """
#####
#...#
#.#.#
#...#
#####"""),
            (Pt(1,1), Pt(4,4),  7, """
######
#....#
#..#.#
#.#..#
#....#
######"""),
            (Pt(1,1), Pt(5,5),  9, """
#######
#.....#
#...#.#
#..#..#
#.....#
#.....#
#######"""),
            (Pt(1,1), Pt(5,5),  11, """
#######
#.....#
#...#.#
####..#
#....##
#.....#
#######"""),
            ]

    for tc in testcases:
        (start, finish, pathlen, lines) = tc
        lines = lines.split("\n")

        game = Game(lines)
        path = game.shortest_path_between(start, finish)
        assert(path is not None)
        assert(path[0] == start)
        assert(path[-1] == finish)
        assert(pathlen == len(path))
        print("path is {}".format(path))

def test_path_exact():
    testcases = [
            ([(1,1),(2,1),(2,2)], """
####
#..#
#..#
####
"""),
            ([(2,1),(1,1),(1,2)], """
####
#..#
#..#
####
"""),
            ([(3,1),(2,1),(1,1),(1,2),(1,3),(1,4),(2,4),(3,4),(3,5),(4,5),(5,5),(5,4)], """
#######
#.....#
#...#.#
#.#####
#...#.#
#.....#
#######
"""),
            ]

    for tc in testcases:
        (expected_path, lines) = tc
        lines = lines.split("\n")
        expected_path = [Pt(t[0],t[1]) for t in expected_path]
        start = expected_path[0]
        finish = expected_path[-1]

        game = Game(lines)
        path = game.shortest_path_between(start, finish)
        print("path is {}".format(path))
        assert(len(path) == len(expected_path))
        assert(path == expected_path)

