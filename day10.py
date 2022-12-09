""" Day 10 in the AoC house
time taken 1/2 hr
leaderboard 2,2

James must have found his laptop ok whilst unpacking
Feels a lot easier than the curve might suggest
"""
from tools.common import file_to_list

lines = file_to_list("day10.txt")

x_history = [1]
for line in lines:
    x = x_history[-1]
    # don't really need to check for noop, could just always append 1 tick
    # but who knows what part b might entail
    if line == "noop":
        x_history.append(x)
    if line.startswith("addx"):
        val = int(line.split(" ")[1])
        x_history.append(x)
        x_history.append(x + val)

# Cycle 1 is based at index 0
# so start at 19 (for cycle 20)
# and multiply x by i+1 (not i)
print("A", sum([(i + 1) * x for i, x in enumerate(x_history) if i % 40 == 19]))

for r in range(len(x_history) // 40):
    crt = []
    for i in range(40):
        sp = x_history[i + (r * 40)]
        if sp-1 <= i <= sp+1:
            crt.append("#")
        else:
            crt.append(" ")
    print("".join(crt))

