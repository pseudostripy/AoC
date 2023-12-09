import os
import re
import math
import operator as op
os.chdir('AllPuzzles/Puzzle9')
PATH_INPUT_DATA = 'input.txt'


def main():
    # unpack data
    lines = read_data()
    data = re_unpack_data(lines)

    seqans = []
    for seq in data:
        sdiffs = [seq]
        sdiff = seq
        while True:
            sdiff = [sdiff[i+1] - sdiff[i] for i in range(len(sdiff)-1)]
            sdiffs.append(sdiff)
            if len(sdiff) == 1 or sdiff[-1] == sdiff[-2]:
                break

        print(sdiffs)

        stvals = 0
        sdiffsrev = list(reversed(sdiffs))
        print(sdiffsrev[:-1])
        print(sdiffsrev)
        for i, sd in enumerate(sdiffsrev[:-1]):
            stvals = sdiffsrev[i+1][0] - sd[0]
            print(stvals)
            sdiffsrev[i+1].insert(0, stvals)

        seqans.append(stvals)

    print(seqans)
    print("pt2_sol:", sum(seqans))


def re_unpack_data(lines):
    return [[int(c) for c in line.strip().split()] for line in lines]


def read_data():
    """ read input data; split by line breaks """
    with open(PATH_INPUT_DATA, 'r', encoding="utf-8") as f:
        lines = f.readlines()
    return lines


# run code
if __name__ == "__main__":
    main()
