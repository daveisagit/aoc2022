""" Day 19 in the AoC house - Robot Mining
time taken : >24
leaderboard 1,1

Really ambiguous phrasing meant my code was failing Blueprint 2 in the example being able to produce
13 (as opposed to the predicted 12 geodes). See the log below of how this achieved

Each robot can collect 1 of its resource type per minute. It also takes one
minute for the robot factory (also conveniently from your pack) to
construct any type of robot, although it consumes the necessary resources
available when construction begins.

    key phrase: "any type of robot" ?

So 2 of any given type is not possible, yes I get that ...

But it's a limit of 1 on the construction of robots of that type
So why not 1 of each?

    "It takes one minute for the robot factory to construct any type of robot"

This could be read as a limit on the type i.e. it takes 1 min to construct an Ore,
it takes 1 min to construct a Clay etc...
So the factory could produce 4 robots one of each type in 1 minute if there were enough funds

-------------------------------
If it had said

"It takes one minute for the robot factory to construct any robot and the factory can only
construct one robot at a time"

Then my day would have gone a lot better :-(

As it is key to solution being able to run in timely manner that only 1 robot can be built
in minute by the factory PERIOD!

-------------------------------
Example: Blueprint 2
You can see on minute 18 we could purchase: [0 0 1 1] that being 1 Obsidian and 1 Geode for [6 8 12 0]
That being a cost of 6 Ore, 8 Clay, 12 Obsidian

Min: 1  Start with | Robots: [1 0 0 0] Minerals: [0 0 0 0]   - Purchased: [0 0 0 0] for [0 0 0 0]  leaving [0 0 0 0]  + Income from Robots: [1 0 0 0]  ...  End with | Robots: [1 0 0 0] Minerals: [1 0 0 0]
Min: 2  Start with | Robots: [1 0 0 0] Minerals: [1 0 0 0]   - Purchased: [0 0 0 0] for [0 0 0 0]  leaving [1 0 0 0]  + Income from Robots: [1 0 0 0]  ...  End with | Robots: [1 0 0 0] Minerals: [2 0 0 0]
Min: 3  Start with | Robots: [1 0 0 0] Minerals: [2 0 0 0]   - Purchased: [1 0 0 0] for [2 0 0 0]  leaving [0 0 0 0]  + Income from Robots: [1 0 0 0]  ...  End with | Robots: [2 0 0 0] Minerals: [1 0 0 0]
Min: 4  Start with | Robots: [2 0 0 0] Minerals: [1 0 0 0]   - Purchased: [0 0 0 0] for [0 0 0 0]  leaving [1 0 0 0]  + Income from Robots: [2 0 0 0]  ...  End with | Robots: [2 0 0 0] Minerals: [3 0 0 0]
Min: 5  Start with | Robots: [2 0 0 0] Minerals: [3 0 0 0]   - Purchased: [1 0 0 0] for [2 0 0 0]  leaving [1 0 0 0]  + Income from Robots: [2 0 0 0]  ...  End with | Robots: [3 0 0 0] Minerals: [3 0 0 0]
Min: 6  Start with | Robots: [3 0 0 0] Minerals: [3 0 0 0]   - Purchased: [0 1 0 0] for [3 0 0 0]  leaving [0 0 0 0]  + Income from Robots: [3 0 0 0]  ...  End with | Robots: [3 1 0 0] Minerals: [3 0 0 0]
Min: 7  Start with | Robots: [3 1 0 0] Minerals: [3 0 0 0]   - Purchased: [0 1 0 0] for [3 0 0 0]  leaving [0 0 0 0]  + Income from Robots: [3 1 0 0]  ...  End with | Robots: [3 2 0 0] Minerals: [3 1 0 0]
Min: 8  Start with | Robots: [3 2 0 0] Minerals: [3 1 0 0]   - Purchased: [0 1 0 0] for [3 0 0 0]  leaving [0 1 0 0]  + Income from Robots: [3 2 0 0]  ...  End with | Robots: [3 3 0 0] Minerals: [3 3 0 0]
Min: 9  Start with | Robots: [3 3 0 0] Minerals: [3 3 0 0]   - Purchased: [0 1 0 0] for [3 0 0 0]  leaving [0 3 0 0]  + Income from Robots: [3 3 0 0]  ...  End with | Robots: [3 4 0 0] Minerals: [3 6 0 0]
Min: 10 Start with | Robots: [3 4 0 0] Minerals: [3 6 0 0]   - Purchased: [0 1 0 0] for [3 0 0 0]  leaving [0 6 0 0]  + Income from Robots: [3 4 0 0]  ...  End with | Robots: [3 5 0 0] Minerals: [3 10 0 0]
Min: 11 Start with | Robots: [3 5 0 0] Minerals: [3 10 0 0]  - Purchased: [0 0 1 0] for [3 8 0 0]  leaving [0 2 0 0]  + Income from Robots: [3 5 0 0]  ...  End with | Robots: [3 5 1 0] Minerals: [3 7 0 0]
Min: 12 Start with | Robots: [3 5 1 0] Minerals: [3 7 0 0]   - Purchased: [0 1 0 0] for [3 0 0 0]  leaving [0 7 0 0]  + Income from Robots: [3 5 1 0]  ...  End with | Robots: [3 6 1 0] Minerals: [3 12 1 0]
Min: 13 Start with | Robots: [3 6 1 0] Minerals: [3 12 1 0]  - Purchased: [0 0 1 0] for [3 8 0 0]  leaving [0 4 1 0]  + Income from Robots: [3 6 1 0]  ...  End with | Robots: [3 6 2 0] Minerals: [3 10 2 0]
Min: 14 Start with | Robots: [3 6 2 0] Minerals: [3 10 2 0]  - Purchased: [0 0 1 0] for [3 8 0 0]  leaving [0 2 2 0]  + Income from Robots: [3 6 2 0]  ...  End with | Robots: [3 6 3 0] Minerals: [3 8 4 0]
Min: 15 Start with | Robots: [3 6 3 0] Minerals: [3 8 4 0]   - Purchased: [0 0 1 0] for [3 8 0 0]  leaving [0 0 4 0]  + Income from Robots: [3 6 3 0]  ...  End with | Robots: [3 6 4 0] Minerals: [3 6 7 0]
Min: 16 Start with | Robots: [3 6 4 0] Minerals: [3 6 7 0]   - Purchased: [0 0 0 0] for [0 0 0 0]  leaving [3 6 7 0]  + Income from Robots: [3 6 4 0]  ...  End with | Robots: [3 6 4 0] Minerals: [6 12 11 0]
Min: 17 Start with | Robots: [3 6 4 0] Minerals: [6 12 11 0] - Purchased: [0 0 1 0] for [3 8 0 0]  leaving [3 4 11 0] + Income from Robots: [3 6 4 0]  ...  End with | Robots: [3 6 5 0] Minerals: [6 10 15 0]
Min: 18 Start with | Robots: [3 6 5 0] Minerals: [6 10 15 0] - Purchased: [0 0 1 1] for [6 8 12 0] leaving [0 2 3 0]  + Income from Robots: [3 6 5 0]  ...  End with | Robots: [3 6 6 1] Minerals: [3 8 8 0]
Min: 19 Start with | Robots: [3 6 6 1] Minerals: [3 8 8 0]   - Purchased: [0 0 1 0] for [3 8 0 0]  leaving [0 0 8 0]  + Income from Robots: [3 6 6 1]  ...  End with | Robots: [3 6 7 1] Minerals: [3 6 14 1]
Min: 20 Start with | Robots: [3 6 7 1] Minerals: [3 6 14 1]  - Purchased: [0 0 0 1] for [3 0 12 0] leaving [0 6 2 1]  + Income from Robots: [3 6 7 1]  ...  End with | Robots: [3 6 7 2] Minerals: [3 12 9 2]
Min: 21 Start with | Robots: [3 6 7 2] Minerals: [3 12 9 2]  - Purchased: [0 0 1 0] for [3 8 0 0]  leaving [0 4 9 2]  + Income from Robots: [3 6 7 2]  ...  End with | Robots: [3 6 8 2] Minerals: [3 10 16 4]
Min: 22 Start with | Robots: [3 6 8 2] Minerals: [3 10 16 4] - Purchased: [0 0 0 1] for [3 0 12 0] leaving [0 10 4 4] + Income from Robots: [3 6 8 2]  ...  End with | Robots: [3 6 8 3] Minerals: [3 16 12 6]
Min: 23 Start with | Robots: [3 6 8 3] Minerals: [3 16 12 6] - Purchased: [0 0 0 1] for [3 0 12 0] leaving [0 16 0 6] + Income from Robots: [3 6 8 3]  ...  End with | Robots: [3 6 8 4] Minerals: [3 22 8 9]
Min: 24 Start with | Robots: [3 6 8 4] Minerals: [3 22 8 9]  - Purchased: [0 0 0 0] for [0 0 0 0]  leaving [3 22 8 9] + Income from Robots: [3 6 8 4]  ...  End with | Robots: [3 6 8 4] Minerals: [6 28 16 13]

-------------------------------------------------
A long runner

A: 1081
Time for part A: 39.161 s
B: 2415
Time for part B: 135.102 s


"""


from collections import deque
from time import time

from tools.common import file_to_list

ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3

stm = time()


def parse_int(file_name):
    lines = file_to_list(file_name)
    data = []
    for line in lines:
        bp = line.split(":")
        bpi = bp[0]
        bpi = int(bpi.split(" ")[1])
        bpc = bp[1]
        od = bpc.split(".")
        bpa = [[0] * 4] * 4
        for x in range(4):
            odo = od[x].split(" ")
            bpa[x] = [int(odo[5]), 0, 0, 0]
            if len(odo) > 7:
                if odo[9] == "clay":
                    bpa[x][CLAY] += int(odo[8])
                if odo[9] == "obsidian":
                    bpa[x][OBSIDIAN] += int(odo[8])
        data.append(bpa)

    return data


blueprints = parse_int("day19.txt")


def find_max_geodes(blueprint, total_time, log_the_stuff=False):

    if log_the_stuff:
        print(f"Blueprint costs {blueprint}")

    # What is the maximum you can spend of any mineral type in a minute ?
    # there is no point in having more robots than this as you won't
    # be able to spend it. It will just create excess waste
    max_spend = [max(col) for col in zip(*[costs for costs in blueprint])]
    if log_the_stuff:
        print(f"Max spend in a minute {max_spend}")

    best_geode_count = 0

    # model the state a tulpe of minute, balance, robots 
    start = (0, 0, 0, 0, 0, 1, 0, 0, 0)
    queue = deque([start])
    already_done = set()

    while queue:

        state = queue.popleft()

        minute = state[0]
        balance = list(state[1:5])
        robots = list(state[5:])
        time_left = total_time - minute

        best_geode_count = max(best_geode_count, balance[3])

        if time_left == 0:
            # don't try to add anymore
            continue

        # prune the excess fluff for Ore, Clay and Obsidian
        # instead of pruning the tree/iterations we are saying certain branches
        # are equivalent if you ignore the waste
        # So we still consider a wasteful option if an equivalent greener
        # option has not yet been proposed
        for i in range(3):

            # there is no point in having more robots than this as you won't
            # be able to spend it. It will just create excess waste
            if robots[i] >= max_spend[i]:
                robots[i] = max_spend[i]

            # having too much which can not be spent is also waste
            if balance[i] >= time_left * max_spend[i] - robots[i] * (time_left-1):
                balance[i] = time_left * max_spend[i] - robots[i] * (time_left-1)

        # re-invent our state to be green
        state = (minute, ) + tuple(balance) + tuple(robots)

        if state in already_done:
            # if we have already done the green version of the state then there's
            # no point looking at it again
            continue

        already_done.add(state)

        # # add the branch for where we do not buy anything at all
        new_balance = [bal + rbt for bal, rbt in zip(balance, robots)]
        t = (minute + 1, ) + tuple(new_balance) + tuple(robots)
        if log_the_stuff:
            print(f"{minute} - Dont buy: Cur {balance} + Robots {robots} = New {new_balance}")
        queue.append(t)

        # add branches for each robot we could buy
        for ci, cost in enumerate(blueprint):
            check_funds = [(bal - cst) for bal, cst in zip(balance, cost)]

            if all([val >= 0 for val in check_funds]):

                # Add the income before increasing the robot count
                new_balance = [(bal + rbt) for bal, rbt in zip(check_funds, robots)]

                if log_the_stuff:
                    print(f"{minute + 1} - Buy: Cur {balance} - Cost {cost} + Robots {robots} = {new_balance}")

                # inc our robot count
                robots[ci] += 1
                if log_the_stuff:
                    print(f"{minute} - {new_balance}, Robots {robots}")

                t = (minute + 1, ) + tuple(new_balance) + tuple(robots)
                robots[ci] -= 1  # don't corrupt the next iteration

                queue.append(t)

    return best_geode_count


part_a = 0
for bi, b in enumerate(blueprints):
    best_geode = find_max_geodes(b, 24)
    part_a += (bi+1)*best_geode
print(f"A: {part_a}")

etm = time()
elapsed_time = etm - stm
print(f"Time for part A: {elapsed_time:.3f} s")


stm = time()

quality_level = 0
part_b = 1
for bi in range(3):
    bb = find_max_geodes(blueprints[bi], 32)
    part_b *= bb

print(f"B: {part_b}")

etm = time()
elapsed_time = etm - stm
print(f"Time for part B: {elapsed_time:.3f} s")
