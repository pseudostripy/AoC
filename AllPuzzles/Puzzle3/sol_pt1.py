import os
os.chdir('AllPuzzles/Puzzle3')
PATH_INPUT_DATA = 'input.txt'


class Pnum:
    def __init__(self, irow, jst, jend, num):
        self.irow = irow    # row of number
        self.jst = jst      # start col of number
        self.jend = jend    # final col of number
        self.num = num
        self.symbolic = None

    def set_is_symbolic(self, bval):
        self.symbolic = bval
        return self

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

    for pnum in pnums:
        # check for symbols
        anysym = False
        for (i, j) in pnum.search_box(board_sz):
            if not board[i][j].isdigit() and not board[i][j] == '.':
                anysym = True
                break

        pnum.set_is_symbolic(anysym)

    for p in pnums:
        print(p.num, p.symbolic)
    total = sum(p.num for p in pnums if p.symbolic)
    print(total)


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
