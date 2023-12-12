import os
import re
import math
import numpy as np
from enum import IntEnum, auto
os.chdir('AllPuzzles/Puzzle11')
PATH_INPUT_DATA = 'input.txt'


def main():
    # unpack data
    lines = read_data()
    ldata = re_unpack_data(lines)
    data = np.array(ldata)
    inds = [(i, j) for (i, j), v in np.ndenumerate(data) if v]

    print_grid(data)
    print_grid(inds)

    pdbest = []  # pair-dist best
    for i, p1 in enumerate(inds):
        for j, p2 in enumerate(inds[i+1:]):  # triangular
            d = abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])
            pdbest.append(d)
    print(pdbest)
    print(sum(pdbest))


def re_unpack_data(lines):
    data2 = []
    for i, line in enumerate(lines):
        data2.append(line)
        if all(c == '.' for c in line):
            data2.append(line)  # empty row duplicate

    # now do the same for columns:
    data2T = np.array(data2).T.tolist()
    print_grid(data2)

    nrow = len(data2)
    mcol = len(data2[0])

    # annoying meme w/ python vs numpy chararray handling
    data2_nostrings = [[0 if c == '.' else 1 for c in line] for line in data2]
    d = np.array(data2_nostrings)

    for j in range(mcol):
        col = d[:, j]
        if j == 0:
            dout = col
        else:
            dout = np.column_stack((dout, col))
        if np.all(col == 0):
            dout = np.column_stack((dout, col))  # again

    totcnt = 1
    for i, row in enumerate(dout):
        for j, v in enumerate(row):
            if v:
                dout[i, j] = totcnt
                totcnt += 1

    print(dout)
    return dout


def print_grid(grd):
    for line in grd:
        print(line)


def read_data():
    """ read input data; split by line breaks """
    with open(PATH_INPUT_DATA, 'r', encoding="utf-8") as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


# run code
if __name__ == "__main__":
    main()
