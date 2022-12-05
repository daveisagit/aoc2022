""" Day 5 in the AoC house. Its bladder o'clock so why not help some elves out
Slightly fortunate (maybe?) that I misread the puzzle and did part b before part a
Trickier input parsing today
"""

import copy
from dataclasses import dataclass

from tools.common import file_to_list, reverse_string


class Stack:

    def __repr__(self):
        return self.contents

    def __init__(self):
        self.contents = ""

    def push(self, sub_stack: str):
        self.contents = sub_stack + self.contents

    def pop(self, size) -> str:
        sub_stack = self.contents[:size]
        self.contents = self.contents[size:]
        return sub_stack

    def init(self):
        self.contents = reverse_string(
            self.contents.strip()
        )

    def top(self) -> str:
        return self.contents[0]


@dataclass
class Move:
    qty: int
    src: int
    trg: int


#
# Load stacks
#
lines = file_to_list("day5-stacks.txt")

stacks = []
for idx in range(0, 9):
    stacks.append(Stack())

for line in lines[:-1]:
    for idx in range(1, len(line), 4):
        stk_id = (idx-1) // 4
        ch = line[idx]
        if ch.strip():
            stacks[stk_id].push(ch)

for stack in stacks:
    stack.init()

save_init_stack = stacks.copy()

#
# Load moves
#
lines = file_to_list("day5-moves.txt")
moves = [line.split(" ") for line in lines]
moves = [Move(int(m[1]), int(m[3]) - 1, int(m[5]) - 1) for m in moves]

#
# Ready to go
#

stacks = copy.deepcopy(save_init_stack)
for move in moves:
    ss = stacks[move.src].pop(move.qty)
    ss = reverse_string(ss)
    stacks[move.trg].push(ss)

tops = [stack.top() for stack in stacks]
print("".join(tops))

stacks = copy.deepcopy(save_init_stack)
for move in moves:
    ss = stacks[move.src].pop(move.qty)
    stacks[move.trg].push(ss)

tops = [stack.top() for stack in stacks]
print("".join(tops))
