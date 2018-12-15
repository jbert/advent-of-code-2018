from day15 import Game, Pt, Unit


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
