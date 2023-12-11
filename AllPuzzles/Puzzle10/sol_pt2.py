import os
import re
import math
import operator as op
from enum import IntEnum, auto
os.chdir('AllPuzzles/Puzzle10')
PATH_INPUT_DATA = 'input.txt'
LARGENUM = 1_000_000
JOINER = ""


class PointDir:
    def __init__(self, i, j, entry):
        self.x = i
        self.y = j
        self.entry = entry

    def set_exit(self, ext):
        self.exit = ext

    @property
    def xy(self):
        return (self.x, self.y)

    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.entry})"

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}, {self.entry})"


class CD(IntEnum):
    """Cardinal direction"""
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()


def main():
    # unpack data
    lines = read_data()
    data = re_unpack_data(lines)

    scoord = find_s_coord(data)

    print(scoord)

    # get on this code level
    if PATH_INPUT_DATA == "sample.txt":
        srep = 'F'
        data[scoord[0]][scoord[1]] = srep
        pd = PointDir(scoord[0], scoord[1], CD.WEST)
    elif PATH_INPUT_DATA == "sample2.txt":
        srep = '7'
        data[scoord[0]][scoord[1]] = srep
        pd = PointDir(scoord[0], scoord[1], CD.NORTH)
    elif PATH_INPUT_DATA == 'input.txt':  # input init
        srep = 'F'
        data[scoord[0]][scoord[1]] = srep
        pd = PointDir(scoord[0], scoord[1], CD.WEST)
    elif PATH_INPUT_DATA == "sampleA.txt":
        srep = 'F'
        data[scoord[0]][scoord[1]] = srep
        pd = PointDir(scoord[0], scoord[1], CD.SOUTH, CD.EAST)
    else:
        raise Exception("add manual init")

    inds = [pd]  # start indices
    totctr = 0
    while (totctr < LARGENUM):
        pd = get_next_pos(data, pd)
        if pd.x == inds[0].x and pd.y == inds[0].y:
            break  # full loop
        inds.append(pd)
        totctr += 1

    # now we have the path, make these stand out:
    data2 = data.copy()
    for i, line in enumerate(data):
        for j, c in enumerate(line):
            if any((i, j) == p.xy for p in inds):
                data2[i][j] = c
            else:
                data2[i][j] = '.'
    for line in data2:
        print(JOINER.join(line))

    # traverse and add * for winning?
    for pd in inds:
        insides = get_insides(data, pd)
        for ins in insides:
            ix, iy = ins  # shorthand
            if ix >= len(data2) or iy >= len(data2[0]):
                continue  # "i" would be OOB
            if data2[ix][iy] != '.':
                continue  # part of our loop
            data2[ix][iy] = '*'

    print("\nAfter fixing:\n")
    for line in data2:
        print(JOINER.join(line))

    # now deal with internal stuff:
    data3 = data2.copy()
    for i, line in enumerate(data2):
        for j, c in enumerate(line):
            if c != '.':
                continue  # already done
            if is_star_surrounded(data2, (i, j)):
                data3[i][j] = '*'

    print("\nAfter internal:\n")
    for line in data2:
        print(JOINER.join(line))

    totcnt = 0
    for line in data2:
        for c in line:
            if c == '*':
                totcnt += 1
    print(totcnt)
    # print(inds)
    # pathlen = len(inds)
    # print(pathlen)
    # print("sol:", pathlen/2)

    # print(seqans)
    # print("pt1_sol:", sum(seqans))


def is_star_surrounded(d, inds):
    Nrows = len(d)
    Ncols = len(d[0])
    i, j = inds
    safeR = False
    for jj in range(j, Ncols):
        if d[i][jj] == '.':
            continue  # keep going until collision
        elif d[i][jj] != '*':
            return False  # letter collision (from outer)
        elif d[i][jj] == '*':
            safeR = True
            break
    if not safeR:
        return False  # probably outer bdry, no collision

    safeL = False
    for jj in range(j, 0, -1):
        if d[i][jj] == '.':
            continue  # keep going until collision
        elif d[i][jj] != '*':
            return False  # letter collision (from outer)
        elif d[i][jj] == '*':
            safeL = True
            break
    if not safeL:
        return False  # probably outer bdry, no collision

    safeB = False
    for ii in range(i, Nrows):
        if d[ii][j] == '.':
            continue  # keep going until collision
        elif d[ii][j] != '*':
            return False  # letter collision (from outer)
        elif d[ii][j] == '*':
            safeB = True
            break
    if not safeB:
        return False  # probably outer bdry, no collision

    safeT = False
    for ii in range(i, 0, -1):
        if d[ii][j] == '.':
            continue  # keep going until collision
        elif d[ii][j] != '*':
            return False  # letter collision (from outer)
        elif d[ii][j] == '*':
            safeT = True
            break
    if not safeT:
        return False  # probably outer bdry, no collision
    return True  # surely?


def get_insides(data, pd):
    # assumes we're always traversing anti-clockwise
    c = data[pd.x][pd.y]

    pds = []
    if pd.entry == CD.WEST:
        pds.append((pd.x + 1, pd.y))  # keep-things-below
    elif pd.entry == CD.EAST:
        pds.append((pd.x - 1, pd.y))  # keep-things-above
    elif pd.entry == CD.NORTH:
        pds.append((pd.x, pd.y - 1))  # keep-things-right
    elif pd.entry == CD.SOUTH:
        pds.append((pd.x, pd.y + 1))  # keep-things-left

    if pd.entry == pd.exit:  # '|', '-'
        return pds  # already handled all relevant ones

    if pd.exit == CD.NORTH:
        pds.append((pd.x, pd.y - 1))  # keep-things-left
    elif pd.exit == CD.SOUTH:
        pds.append((pd.x, pd.y + 1))  # keep-things-right
    elif pd.exit == CD.EAST:
        pds.append((pd.x - 1, pd.y))  # keep-things-above
    else:
        pds.append((pd.x + 1, pd.y))  # keep-things-below
    return pds


def get_next_pos(data, pd):
    c = data[pd.x][pd.y]

    if pd.x == 4 and pd.y == 3:
        test = 1

    if c == '|':
        if pd.entry == CD.NORTH:  # "entered travelling North"
            pd.set_exit(CD.NORTH)
            return PointDir(pd.x - 1, pd.y, pd.exit)
        elif pd.entry == CD.SOUTH:
            pd.set_exit(CD.SOUTH)
            return PointDir(pd.x + 1, pd.y, pd.exit)
        else:
            raise Exception("Shouldn't be trying to enter '|' from EW")

    if c == '-':
        if pd.entry == CD.WEST:
            pd.set_exit(CD.WEST)
            return PointDir(pd.x, pd.y - 1, pd.exit)
        elif pd.entry == CD.EAST:
            pd.set_exit(CD.EAST)
            return PointDir(pd.x, pd.y + 1, pd.exit)
        else:
            raise Exception("Shouldn't be trying to enter '-' from NS")

    if c == 'L':
        if pd.entry == CD.SOUTH:
            pd.set_exit(CD.EAST)
            return PointDir(pd.x, pd.y + 1, pd.exit)
        elif pd.entry == CD.WEST:
            pd.set_exit(CD.NORTH)
            return PointDir(pd.x - 1, pd.y, pd.exit)
        else:
            raise Exception("Shouldn't be trying to enter 'L' going N or E")

    if c == 'J':
        if pd.entry == CD.SOUTH:
            pd.set_exit(CD.WEST)
            return PointDir(pd.x, pd.y - 1, pd.exit)
        elif pd.entry == CD.EAST:
            pd.set_exit(CD.NORTH)
            return PointDir(pd.x - 1, pd.y, pd.exit)
        else:
            raise Exception("Shouldn't be trying to enter 'J' going N or W")

    if c == '7':
        if pd.entry == CD.EAST:
            pd.set_exit(CD.SOUTH)
            return PointDir(pd.x + 1, pd.y, pd.exit)
        elif pd.entry == CD.NORTH:
            pd.set_exit(CD.WEST)
            return PointDir(pd.x, pd.y - 1, pd.exit)
        else:
            raise Exception("Shouldn't be trying to enter '7' going S or W")

    if c == 'F':
        if pd.entry == CD.WEST:
            pd.set_exit(CD.SOUTH)
            return PointDir(pd.x + 1, pd.y, pd.exit)
        elif pd.entry == CD.NORTH:
            pd.set_exit(CD.EAST)
            return PointDir(pd.x, pd.y + 1, pd.exit)
        else:
            raise Exception("Shouldn't be trying to enter 'F' going S or E")

    raise Exception("Unhandled case or shouldn't get here!")


def find_s_coord(data):
    for i, line in enumerate(data):
        if 'S' in line:
            return (i, line.index('S'))
    raise Exception("Couldn't find 'S'")


def re_unpack_data(lines):
    return [[c for c in line.strip()] for line in lines]


def read_data():
    """ read input data; split by line breaks """
    with open(PATH_INPUT_DATA, 'r', encoding="utf-8") as f:
        lines = f.readlines()
    return lines


# run code
if __name__ == "__main__":
    main()
