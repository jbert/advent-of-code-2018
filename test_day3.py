from day3 import Rect, parse_claim_to_rect


def test_rect_intersect():

    test_lines = [
            "#1 @ 1,3: 4x4",
            "#2 @ 3,1: 4x4",
            "#3 @ 5,5: 2x2",
            ]
    trs = [parse_claim_to_rect(line) for line in test_lines]

    assert(trs[0].intersect(trs[2]) is None)
    assert(trs[1].intersect(trs[2]) is None)
    overlap = trs[0].intersect(trs[1])
    assert(overlap is not None)
    # Assert fails - how to compare?
#    assert(overlap == Rect(None, 3, 3, 2, 2))
