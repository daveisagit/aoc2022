""" Day 17 in the AoC house - Tetris on Wheels
time taken: 4 hrs
leaderboard: 1,1

"""
from time import time
import numpy as np
from tools.common import file_to_list

stm = time()

lines = file_to_list("day17.txt")
funnel_width = 7
working_area = np.empty((0, funnel_width), dtype=int)
banked = 0
rock_count = -1
jet_index = -1

rock_images = [
    [
        "####"
    ],
    [
        " # ",
        "###",
        " # ",
    ],
    [
        "  #",
        "  #",
        "###",
    ],
    [
        "#",
        "#",
        "#",
        "#"
    ],
    [
        "##",
        "##",
    ],

]


def parse_input():
    j = ""
    for line in lines:
        j += line
    return j


jet_stream = parse_input()
# jet_stream = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"


def make_rock_window(idx, offset=2):
    """Return a window funnel width for the rock pattern
    the rows will vary based on the shape"""
    img = rock_images[idx]
    wdw = np.zeros((len(img), funnel_width), dtype=int)
    for ri, line in enumerate(reversed(img)):
        for ci, ch in enumerate(line):
            if ch == "#":
                wdw[ri, ci + offset] = 1
    return wdw


def there_is_a_collision(rock_window, at_row):
    test_window = add_working_area(rock_window, at_row)
    return has_collided(test_window)


def add_working_area(rock_window, at_row):
    """Superimpose (i.e. add) the portion of the working_area at_row
    same height returned"""
    rock_height = len(rock_window)
    wdw = working_area[at_row: at_row + rock_height, :]
    whw_height = len(wdw)
    if rock_height > whw_height:
        pad_zeros = np.zeros((rock_height - whw_height, funnel_width), dtype=int)
        wdw = np.concatenate((wdw, pad_zeros))
    return rock_window + wdw


def has_collided(rock_window):
    """if there are any elements > 1 then we have collided"""
    return (rock_window > 1).sum() > 0


def add_rock_to_working_area(rock_window, at_row):
    """Once landed/stopped we need to add it to the working area"""
    global working_area
    h = len(rock_window)
    extra_rows = at_row - len(working_area) + h
    if extra_rows > 0:
        extra_space = np.zeros((extra_rows, funnel_width), dtype=int)
        working_area = np.concatenate((working_area, extra_space))
    for ri, row in enumerate(rock_window):
        for ci, e in enumerate(row):
            working_area[at_row + ri, ci] += e


def parse_input():
    j = ""
    for line in lines:
        j += line
    return j


def row_as_text(row):
    text_map = {
        1: "#", 0: "."
    }
    return "".join([text_map.get(x, "?") for x in row])


def draw_working_area(inc_idx=False):
    height = current_height()
    print(f"Rock count {rock_count + 1}")
    print(f"Height: {banked + len(working_area)}")
    for idx, row in enumerate(reversed(working_area)):
        if inc_idx:
            print(f"{height - idx:8d} {row_as_text(row)}")
        else:
            print(f"|{row_as_text(row)}|")
    if not inc_idx:
        print("+-------+")


def jet_adjustment(rock_window, direction):
    """Given shift the image left/right as required and if there is room to do so"""
    if direction == "<":
        if sum(rock_window[:, 0]) == 0:
            # room to move
            proposed_rock_window = np.roll(rock_window, -1, axis=1)
            if there_is_a_collision(proposed_rock_window, current_row):
                # but existing rocks prevent it
                return rock_window.copy()
            else:
                # jet moves it
                return proposed_rock_window
        else:
            # no room to move
            return rock_window.copy()
    if direction == ">":
        if sum(rock_window[:, -1]) == 0:
            # room to move
            proposed_rock_window = np.roll(rock_window, 1, axis=1)
            if there_is_a_collision(proposed_rock_window, current_row):
                # but existing rocks prevent it
                return rock_window.copy()
            else:
                # jet moves it
                return proposed_rock_window
        else:
            # no room to move
            return rock_window.copy()


def prune_working_area():
    """Look for the lowest column with rock in. Any lower than that can pruned and banked"""
    global working_area, banked
    if len(working_area) > 0:
        heights = []
        for idx in range(funnel_width):
            col = working_area[:, idx]
            non_zeros = np.nonzero(col)[0]
            if len(non_zeros) > 0:
                heights.append(max(non_zeros))
            else:
                return
        trim_line = min(heights)
        working_area = working_area[trim_line:]
        banked += trim_line


def carry_on():
    """When to stop"""
    if rock_count + 1 >= 10000:
        return False
    return True


def current_height():
    return len(working_area) + banked


prv_rock_count = 0
prv_height = 0
height_remainders = {}

# part_b mods
rock_mod = 1745
height_mod = 2783
settles_after = 1758

while carry_on():

    prune_working_area()
    rock_count += 1  # it's initialised at -1 so this is a counter of what has landed

    if rock_count == 2022:
        print(f"A: {current_height()}")

    rock_index = rock_count % len(rock_images)
    rock = make_rock_window(rock_index)
    falling = True
    current_row = len(working_area) + 3

    while falling:
        jet_index += 1
        jet_index %= len(jet_stream)

        if jet_index == 0 and rock_count > 0:
            print(f"Top row {row_as_text(working_area[-1])} Current rock index:{rock_index} Rocks Landed: {rock_count} {rock_count - prv_rock_count} Height: {current_height()} {current_height() - prv_height}")
            prv_rock_count = rock_count
            prv_height = current_height()

        if settles_after + rock_mod <= rock_count < settles_after + (rock_mod * 2):
            rock_count_cc = rock_count % rock_mod
            height = current_height()
            height_cc = height % height_mod
            height_remainders[rock_count_cc] = height_cc

        jet = jet_stream[jet_index]
        rock = jet_adjustment(rock, jet)

        if there_is_a_collision(rock, current_row - 1):
            add_rock_to_working_area(rock, current_row)
            falling = False

        if current_row == 0 and banked == 0:
            # we've hit the floor
            add_rock_to_working_area(rock, 0)
            falling = False
        else:
            current_row -= 1


def predict_height(after_rocks):
    """Use the data gathered from the repeating pattern"""
    # from 3503 rocks, height= 5592 every 1745 rocks adds 2783 to the height
    quot = after_rocks // rock_mod
    remainder = after_rocks % rock_mod
    height_remainder = height_remainders[remainder]
    predicted_height = quot * height_mod + height_remainder
    return predicted_height


after_this_many_rocks = 1000000000000
part_b = predict_height(after_this_many_rocks)
print(f"Prediction after {after_this_many_rocks} is {part_b}")
