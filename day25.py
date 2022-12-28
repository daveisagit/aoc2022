""" Day 25 in the AoC house - SNAFU
time taken :
leaderboard

"""
test_mode = 0

if test_mode:
    filename = "day25_test.txt"
else:
    filename = "day25.txt"

with open(f"input/{filename}") as f:
    lines = f.read().splitlines()

snafu_digits = "=-012"
snafu_digits_values = {
    ch: (idx-2)
    for idx, ch in enumerate(snafu_digits)
}


def snafu_to_decimal(snafu: str) -> int:
    res = 0
    for pl, ch in enumerate(reversed(snafu)):
        pl_val = (5 ** pl) * snafu_digits_values[ch]
        res += pl_val
    return res


def decimal_to_snafu(dec: int) -> str:
    res = ""
    while dec > 0:
        rem = dec % 5
        rem += 2
        dec = dec // 5
        if rem >= 5:
            dec += 1
        rem %= 5
        dig = snafu_digits[rem]
        res = dig + res
    return res


total = sum([snafu_to_decimal(snafu) for snafu in lines])
snafu_total = decimal_to_snafu(total)
print(f"Part A: {snafu_total}")




