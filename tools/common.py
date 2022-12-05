import collections as col


def reverse_string(in_str: str) -> str:
    """Python reversing by slices"""
    return in_str[::-1]


def file_to_list(filename: str):
    """Read text file to list of strings"""
    with open(f"input/{filename}") as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


class DequeMulti(col.deque):
    """extend deque for multiple items"""

    def multi_pop(self, amount=1):
        res = []
        for idx in range(amount):
            res.insert(0, self.pop())
        return res

    def multi_popleft(self, amount=1):
        res = []
        for idx in range(amount):
            res.append(self.popleft())
        return res

    def multi_append(self, stuff: list):
        """same as extend"""
        for thing in stuff:
            self.append(thing)

    def multi_appendleft(self, stuff: list):
        """not the same as extendleft which appendsleft 1 at a time
        and so reverses the order of stuff
        This will add the block of stuff to left without reversing"""
        for thing in reversed(stuff):
            self.appendleft(thing)


def in_both(cmp1: str, cmp2: str) -> dict:
    """return a dict of characters and the occurrences in both strings"""
    common = {}
    for ch in cmp1:
        if ch in cmp2:
            v = common.get(ch, 0)
            v += 1
            common[ch] = v
    return common


def get_value(item: str):
    """the value of an item a=1 ...  z=26 , A=27 , etc .."""
    if item.islower():
        return ord(item)-96
    else:
        return ord(item)-38


def split_into_groups(a_list, size):
    """Split a list into groups"""
    for idx in range(0, len(a_list), size):
        yield a_list[idx:idx + size]
