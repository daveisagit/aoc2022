""" Day 3 in the AoC house and Dave is up early learning about the strange behaviors of fictitious elves
GO BACK TO BED DAVE!!! It's Saturday??
"""


def in_both(cmp1:str, cmp2:str) -> dict:
    """return a dict of characters and the occurrences in both strings"""
    common = {}
    for ch in cmp1:
        if ch in cmp2:
            v = common.get(ch, 0)
            v += 1
            common[ch] = v
    return common


def item_char(result: dict) -> str:
    """only expect 1 key, what is it"""
    if len(result) > 1:
        raise ValueError()
    return list(result.keys())[0]


def get_value(item: str):
    """the value of an item"""
    if item.islower():
        return ord(item)-96
    else:
        return ord(item)-38


def split_into_groups(a_list, size):
    for idx in range(0, len(a_list), size):
        yield a_list[idx:idx + size]


if __name__ == '__main__':
    with open('input/day3.txt') as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]

    rucksacks = [(line[:len(line) // 2], line[len(line)//2:]) for line in lines]
    duplicates = [in_both(rucksack[0],rucksack[1]) for rucksack in rucksacks]
    just_items = [item_char(duplicate) for duplicate in duplicates]
    values = [get_value(item) for item in just_items]
    print(sum(values))

    total = 0
    for group in split_into_groups(lines, 3):
        r1 = in_both(group[0], group[1])
        s1 = "".join([k for k in r1])
        r2 = in_both(group[1], group[2])
        s2 = "".join([k for k in r2])
        r = in_both(s1, s2)
        total = total + get_value(item_char(r))
    print(total)





