
from tools.common import DequeMulti


def test_multi_deque():
    de = DequeMulti([1, 2, 3, 4, 5, 6, 7, 8, 9])
    assert de.multi_pop(3) == [7, 8, 9]
    assert de.multi_popleft(3) == [1, 2, 3]
    assert len(de) == 3

    de.extend([1, 2, 3, 4])
    assert de.multi_pop(5) == [6, 1, 2, 3, 4]

    de.multi_appendleft([7, 8, 9])
    assert de.multi_popleft(4) == [7, 8, 9, 4]

    de.extendleft([7, 8, 9])
    assert de.multi_popleft(4) == [9, 8, 7, 5]
