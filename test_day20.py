from day20 import parse_regex, Map, Room, Pos
from itertools import count
import pytest


def test_parse():
    testcases = [
            '^WNE$',
            '^ENWWW(NEEE|SSE(EE|N))$',
            '^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$',
            '^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$',
            '^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$',
            ]
    for rstr in testcases:
        r = parse_regex(rstr)
        assert str(r) == rstr


def test_path():
    testcases = [
            ('^WNE$', 3),
            ('^ENWWW(NEEE|SSE(EE|N))$', 10),
            ('^E(N|S)EE$', 3),
            ('^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$', 18),
            ('^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$', 23),
            ('^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$', 31),
            ]
    for t in testcases:
        print("TC: {}".format(t))
        (rstr, expected_distance) = t
        r = parse_regex(rstr)
        assert str(r) == rstr
        m = Map(r)
        distance = m.distance()
        assert distance == expected_distance


def test_room():
    idx_iter = count(1, 1)
    a = Room(Pos(0, 0), idx_iter)
    b = Room(Pos(0, 2), idx_iter)
    with pytest.raises(AssertionError):
        a.join(b)
    a = Room(Pos(0, 0), idx_iter)
    b = Room(Pos(0, 1), idx_iter)
    a.join(b)
