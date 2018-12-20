from day20 import parse_regex


def test_outcome():
    testcases = [
            '^WNE$',
            '^ENWWW(NEEE|SSE(EE|N))$',
#            '^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$',
#            '^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$',
#            '^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$',
            ]
    for rstr in testcases:
        r = parse_regex(rstr)
        assert str(r) == rstr
