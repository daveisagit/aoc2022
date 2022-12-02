if __name__ == '__main__':

    with open('input/day1.txt') as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]

    elves = []
    cal = 0
    for row in lines:
        if row == "":
            elves.append(cal)
            cal = 0
        else:
            cal = cal + int(row)

    elves.append(cal)

    elves.sort(reverse=True)
    print(max(elves))
    print(sum(elves[:3]))


