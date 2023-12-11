import os
import re
import math
import operator as op
from enum import IntEnum, auto
os.chdir('AllPuzzles/Puzzle10')
PATH_INPUT_DATA = 'input.txt'
LARGENUM = 1_000_000


class PointDir:
    def __init__(self, i, j, frm):
        self.x = i
        self.y = j
        self.frm = frm

    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.frm})"

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}, {self.frm})"


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

    srep = '7'
    data[scoord[0]][scoord[1]] = srep
    pd = PointDir(scoord[0], scoord[1], CD.EAST)
    inds = [pd]  # start indices
    totctr = 0
    while (totctr < LARGENUM):
        pd = get_next_pos(data, pd)
        if pd.x == inds[0].x and pd.y == inds[0].y:
            break  # full loop
        inds.append(pd)
        totctr += 1

    print(inds)
    pathlen = len(inds)
    print(pathlen)
    print("sol:", pathlen/2)

    # print(seqans)
    # print("pt1_sol:", sum(seqans))


def get_next_pos(data, pd):
    c = data[pd.x][pd.y]
    if c == '|':
        if pd.frm == CD.NORTH:
            return PointDir(pd.x + 1, pd.y, CD.NORTH)
        elif pd.frm == CD.SOUTH:
            return PointDir(pd.x - 1, pd.y, CD.SOUTH)
        else:
            raise Exception("Shouldn't be trying to enter '|' from EW")

    if c == '-':
        if pd.frm == CD.WEST:
            return PointDir(pd.x, pd.y + 1, CD.WEST)
        elif pd.frm == CD.EAST:
            return PointDir(pd.x, pd.y - 1, CD.EAST)
        else:
            raise Exception("Shouldn't be trying to enter '-' from NS")

    if c == 'L':
        if pd.frm == CD.NORTH:
            return PointDir(pd.x, pd.y + 1, CD.WEST)
        elif pd.frm == CD.EAST:
            return PointDir(pd.x - 1, pd.y, CD.SOUTH)
        else:
            raise Exception("Shouldn't be trying to enter 'L' from SW")

    if c == 'J':
        if pd.frm == CD.NORTH:
            return PointDir(pd.x, pd.y - 1, CD.EAST)
        elif pd.frm == CD.WEST:
            return PointDir(pd.x - 1, pd.y, CD.SOUTH)
        else:
            raise Exception("Shouldn't be trying to enter 'J' from SE")

    if c == '7':
        if pd.frm == CD.WEST:
            return PointDir(pd.x + 1, pd.y, CD.NORTH)
        elif pd.frm == CD.SOUTH:
            return PointDir(pd.x, pd.y - 1, CD.EAST)
        else:
            raise Exception("Shouldn't be trying to enter '7' from NE")

    if c == 'F':
        if pd.frm == CD.EAST:
            return PointDir(pd.x + 1, pd.y, CD.NORTH)
        elif pd.frm == CD.SOUTH:
            return PointDir(pd.x, pd.y + 1, CD.WEST)
        else:
            raise Exception("Shouldn't be trying to enter 'F' from NW")

    raise Exception("Unhandled case or shouldn't get here!")


def find_s_coord(data):
    for i, line in enumerate(data):
        if 'S' in line:
            return (i, line.index('S'))
    raise Exception("Couldn't find 'S'")


def re_unpack_data(lines):
    return [[c for c in line] for line in lines]


def read_data():
    """ read input data; split by line breaks """
    with open(PATH_INPUT_DATA, 'r', encoding="utf-8") as f:
        lines = f.readlines()
    return lines


# run code
if __name__ == "__main__":
    main()
