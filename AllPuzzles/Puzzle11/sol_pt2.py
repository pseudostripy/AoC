import os
import re
import math
import numpy as np
from enum import IntEnum, auto
os.chdir('AllPuzzles/Puzzle11')
PATH_INPUT_DATA = 'input.txt'

k = 1000000  # line_factor


def main():
    # unpack data
    lines = read_data()
    inds, data = re_unpack_data(lines)

    print_grid(data)
    print_grid(inds)

    pdbest = []  # pair-dist best
    for i, ip1 in enumerate(inds):
        for j, ip2 in enumerate(inds[i+1:]):  # triangular
            n1, p1 = ip1  # undo tuple
            n2, p2 = ip2
            sum = 0
            # traverse down then right:
            xst, yst = p1
            xend, yend = p2

            # down first should always be safe:
            for ti in range(xst + 1, xend + 1):
                sum += data[ti, yst]

            # now do left/right to target
            if yst < yend:
                # standard tgt to-the-right
                for tj in range(yst + 1, yend + 1):
                    sum += data[xend, tj]
            else:
                # tgt to the left
                for tj in range(yst - 1, yend - 1, -1):
                    sum += data[xend, tj]
            pdbest.append(((n1, n2), sum))

    print(pdbest)
    totsum = 0.0
    for N, s in pdbest:
        totsum += s
    print(totsum)


def re_unpack_data(lines):
    data2 = []
    totcnt = -1
    empty_rows = []
    test = [[1 if c == '.' else -1 for c in line] for line in lines]
    din = np.array(test)
    for i, row in enumerate(din):
        if all(row >= 0):
            empty_rows.append(i)

    # fix empty row/cols
    empty_cols = []
    for j, col in enumerate(din.T):
        if (all(col >= 0)):
            empty_cols.append(j)

    # print(din)
    for i in empty_rows:
        for j, v in enumerate(din[i, :]):
            if j in empty_cols:
                din[i, j] = 2*k
            else:
                din[i, j] = k
    # print("\n\n\n\n")
    # print(din)
    for j in empty_cols:
        for i, v in enumerate(din[:, j]):
            if i in empty_rows:
                continue  # handled above
            else:
                din[i, j] = k  # multi-connection
    print("\n\n\n\n")
    print(din)

    # get nicer to look at:
    totcnt = 1
    inds = []
    for i, row in enumerate(din):
        for j, v in enumerate(row):
            if v < 0:
                inds.append((totcnt, (i, j)))
                totcnt += 1
                din[i, j] = 1  # fix pass-through

    return (inds, din)


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
