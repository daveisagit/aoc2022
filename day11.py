""" Day 11 in the AoC house - Monkey Business
time taken 1hr
leaderboard 2,2

Clue:
Worry levels are no longer divided by three after each item is inspected;
you'll need to find another way to keep your worry levels manageable.

Also hinted from the input as all the divisibility test factors were prime numbers

Not using a modulo results in way too high integers to process in a timely manner

"""
import math
from collections import deque

from tools.common import file_to_list


class Monkey:

    def __init__(self, starting_items, operation, div_test, true_monkey, false_monkey):
        self.items = deque()
        self.operation: str = operation
        self.div_test: int = div_test
        self.true_monkey: int = true_monkey
        self.false_monkey: int = false_monkey

        self.items.extendleft(starting_items)
        self.inspections: int = 0

    def __repr__(self):
        return f"{self.items} Op:{self.operation} Div Test:{self.div_test} Inspections:{self.inspections}"

    def around(self):
        """ ... People say we monkey around, but were too busy singing ...."""
        while len(self.items) > 0:
            self.inspect_next_item()

    def inspect_next_item(self):
        """Monkey see, monkey do
        We can stay within modulo monkey_modulus to manage our worry levels"""
        self.inspections += 1
        new_worry_level = eval(self.operation, {}, {"old": self.items.pop()}) // CALM_FACTOR
        new_worry_level %= monkey_modulus
        if new_worry_level % self.div_test == 0:
            next_monkey = self.true_monkey
        else:
            next_monkey = self.false_monkey
        monkeys[next_monkey].items.appendleft(new_worry_level)


def parse_input():
    lines = file_to_list("day11.txt")
    for idx, line in enumerate(lines):
        if idx % 7 == 0:
            pass
        if idx % 7 == 1:
            starting_items = line.split(":")[1].strip().split(",")
            starting_items = [int(i) for i in starting_items]
        if idx % 7 == 2:
            op = line.split(":")[1].strip().split("=")[1].strip()
        if idx % 7 == 3:
            div_test = int(line.split("by")[1].strip())
        if idx % 7 == 4:
            true_m = int(line.split("monkey")[1].strip())
        if idx % 7 == 5:
            false_m = int(line.split("monkey")[1].strip())
            monkey = Monkey(starting_items, op, div_test, true_m, false_m)
            monkeys.append(monkey)


monkeys = []
parse_input()
# the LCM of all the divisibility tests
# in order to contain our worry levels
monkey_modulus = math.lcm(*[m.div_test for m in monkeys])
CALM_FACTOR = 3


def monkey_go_round():
    """Process a round of monkiness and tally the inspections.
    We can stay within modulo monkey_modulus for worry levels"""
    for monkey in monkeys:
        monkey.around()


# Part A - CALM_FACTOR = 3, 20 iterations
for r in range(20):
    monkey_go_round()

most_active = sorted([m.inspections for m in monkeys], reverse=True)[:2]
print(f"A) {math.prod(most_active)}")

# Part B - reset starting state and lower the CALM_FACTOR to 1, 10K iterations
monkeys = []
parse_input()
CALM_FACTOR = 1
for r in range(10000):
    monkey_go_round()
most_active = sorted([m.inspections for m in monkeys], reverse=True)[:2]
print(f"A) {math.prod(most_active)}")
