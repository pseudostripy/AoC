from itertools import groupby
from collections import defaultdict
import os
os.chdir('AllPuzzles/Puzzle3')
PATH_INPUT_DATA = 'input.txt'


class AdjacentSymbol:
    def __init__(self, i, j, ch, parent):
        self.i = i
        self.j = j
        self.pos = (i, j)
        self.ch = ch
        self.parent = parent  # helpful for searches later

    def __str__(self):
        return f"{self.pos}"

    @property
    def num(self):
        return self.parent.num  # wrapper


class Pnum:
    def __init__(self, irow, jst, jend, num):
        self.irow = irow    # row of number
        self.jst = jst      # start col of number
        self.jend = jend    # final col of number
        self.inds = (irow, jst)
        self.num = num
        self.syms = []
        self.stars = []

    def __str__(self) -> str:
        return f"{self.num}:({self.irow},{self.jst}):"

    def add_sym(self, i, j, c):
        asym = AdjacentSymbol(i, j, c, self)
        self.syms.append(asym)
        if c == "*":
            self.stars.append(asym)
        return self

    @property
    def has_stars(self):
        return self.stars != []

    @property
    def is_symbolic(self):
        return self.syms != []

    def search_box(self, board_sz):
        # these are EXCLUSIVE bounds (+2 = +1 for "right-cell" and +1 for exclusive)
        # just re-search row 0 if we have to
        strow = max(0, self.irow - 1)
        endrow = min(board_sz[0], self.irow + 2)
        stcol = max(0, self.jst - 1)
        endcol = min(board_sz[1], self.jend + 2)  # exclusive range

        # all index pairs to check for symbols
        return [(i, j) for j in range(stcol, endcol) for i in range(strow, endrow)]


def main():
    lines = read_data()
    board = [[c for c in line.strip()]
             for line in lines]    # get into m x n char array

    pnums = []  # array of start/end indices for each number

    # loop over all characters and check
    for i, line in enumerate(board):    # row, line
        lhs = None
        rhs = None
        for j, c in enumerate(line):    # col, char
            if c.isdigit():
                rhs = j
                if lhs is None:
                    lhs = j

                # number can finish at the very end of line
                if j == len(line) - 1:
                    pnums.append(new_number(i, line, lhs, rhs))
                    lhs = rhs = None  # reset for next look

            else:
                # not a digit
                if lhs is None:
                    continue  # no numbers yet; keep searching

                # found an end of number
                pnums.append(new_number(i, line, lhs, rhs))
                lhs = rhs = None  # reset for next look

    # now check nums for symbols:
    board_rows = len(board)
    board_cols = len(board[0])  # assumes rectangular
    board_sz = (board_rows, board_cols)

    # find all adjacent symbols to this number
    for pnum in pnums:
        for (i, j) in pnum.search_box(board_sz):
            c = board[i][j]
            if not c.isdigit() and not board[i][j] == '.':
                pnum.add_sym(i, j, c)  # adds to extra list if '*' symbol

    # filter and unpack groups
    astars = [asym for p in pnums for asym in p.stars]  # all star symbols
    grps = full_group_by(astars, lambda x: x.pos)
    gears = [(g[0].parent, g[1].parent) for _, g in grps if len(g) == 2]
    gear_ratios = [g[0].num*g[1].num for g in gears]

    # solve and output
    total_pt1 = sum([p.num for p in pnums if p.is_symbolic])
    total_pt2 = sum(gear_ratios)
    print(f"Part 1 total: {total_pt1}")
    print(f"Part 2 total: {total_pt2}")


def full_group_by(l, key=lambda x: x):
    d = defaultdict(list)
    for item in l:
        d[key(item)].append(item)
    return d.items()


def new_number(irow, line, lhs, rhs):
    # case: found a number complete
    # convert list of char-digits into single number
    num = int("".join(line[lhs:rhs+1]))
    return Pnum(irow, lhs, rhs, num)


def read_data():
    """ read input data; split by line breaks """
    with open(PATH_INPUT_DATA, 'r', encoding="utf-8") as f:
        lines = f.readlines()
    return lines


# run code
if __name__ == "__main__":
    main()
