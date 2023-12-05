import os
import re
os.chdir('AllPuzzles/Puzzle4')
PATH_INPUT_DATA = 'input.txt'


def main():
    lines = read_data()
    total = 0
    cardwins = []
    for line in lines:
        (cid, wins, yours) = re_unpack(line)
        your_winning_nums = [x for x in yours if x in wins]
        cardwins.append(len(your_winning_nums))

    ncards = [1 for i in range(len(cardwins))]  # preallocate orig cards
    for i, n in enumerate(cardwins):
        for j in range(1, n+1):
            ncards[i+j] += ncards[i]

    total = sum(ncards)
    print(total)


def re_unpack(line):
    pattern = r"Card\s+(?P<caseid>\d+):(?P<winning>.*?)\|(?P<yournums>.*)"
    m = re.match(pattern, line)

    # unpack regex results
    caseid = m.group("caseid")
    wins = m.group("winning").strip().split()
    yours = m.group("yournums").strip().split()
    return (caseid, wins, yours)


def read_data():
    """ read input data; split by line breaks """
    with open(PATH_INPUT_DATA, 'r', encoding="utf-8") as f:
        lines = f.readlines()
    return lines


# run code
if __name__ == "__main__":
    main()
