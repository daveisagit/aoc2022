if __name__ == '__main__':

    """
        X   Y   Z
    A   3   6   0
    B   0   3   6
    C   6   0   3
    """

    score_map = {
        "AX": 3 + 1,
        "AY": 6 + 2,
        "AZ": 0 + 3,
        "BX": 0 + 1,
        "BY": 3 + 2,
        "BZ": 6 + 3,
        "CX": 6 + 1,
        "CY": 0 + 2,
        "CZ": 3 + 3,
    }

    with open('input/day2.txt') as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    rounds = [line[0]+line[2] for line in lines]

    scores = [score_map[a_round] for a_round in rounds]
    print(sum(scores))

    """
        X   Y   Z
    A   Z   X   Y
    B   X   Y   Z
    C   Y   Z   X
    """

    choice_map = {
        "AX": "Z",
        "AY": "X",
        "AZ": "Y",
        "BX": "X",
        "BY": "Y",
        "BZ": "Z",
        "CX": "Y",
        "CY": "Z",
        "CZ": "X",
    }

    rounds_2 = [a_round[0]+choice_map[a_round] for a_round in rounds]
    scores = [score_map[a_round] for a_round in rounds_2]
    print(sum(scores))
