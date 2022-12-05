
from tools.common import DequeMulti


def test_multi_deque():
    de = DequeMulti([1, 2, 3, 4, 5, 6, 7, 8, 9])
    assert de.multi_pop(3) == [7, 8, 9]
    assert de.multi_popleft(3) == [1, 2, 3]
    assert len(de) == 3

    de.extend([1, 2, 3, 4])
    assert de.contents() == [4, 5, 6, 1, 2, 3, 4]
    assert de.multi_pop(5) == [6, 1, 2, 3, 4]

    de.multi_appendleft([7, 8, 9])
    assert de.contents() == [7, 8, 9, 4, 5]
    assert de.multi_popleft(4) == [7, 8, 9, 4]

    de.extendleft([7, 8, 9])
    assert de.contents() == [9, 8, 7, 5]
    assert de.multi_popleft(4) == [9, 8, 7, 5]
    assert de.contents() == []

    de.extendleft([7, 8, 9])
    assert de.contents() == [9, 8, 7]
    de.multi_appendleft([1, 2])
    assert de.contents() == [1, 2, 9, 8, 7]
    de.extend([3, 4])
    assert de.contents() == [1, 2, 9, 8, 7, 3, 4]
    de.multi_append([5, 6])
    assert de.contents() == [1, 2, 9, 8, 7, 3, 4, 5, 6]

    a_str = de.contents_as_string()
    assert a_str == "129873456"

    assert list(a_str) == ["1", "2", "9", "8", "7", "3", "4", "5", "6"]

    de = DequeMulti(list(a_str))
    de.rotate(3)
    a_str = de.contents_as_string()
    assert a_str == "456129873"
