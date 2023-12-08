import os
import re
import math
import numpy as np
import pandas as pd
from enum import IntEnum, auto
os.chdir('AllPuzzles/Puzzle7')
PATH_INPUT_DATA = 'input.txt'
CARDCONVERT = {"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10}


class HT(IntEnum):
    """Hand-Type (priority)"""
    HIGHCARD = auto()
    PAIR = auto()
    TWOPAIR = auto()
    TRIPS = auto()
    HOUSE = auto()
    QUADS = auto()
    FIVEKIND = auto()


def main():
    # unpack data
    lines = read_data()
    data = re_unpack_data(lines)

    gamehands = []
    for (hand, bid) in data:
        gamehands.append((get_hand_type(hand), hand, bid))

    check_for_duplicates(data)  # throw error

    # sort based on type then highness
    sorted_hands = sorted(gamehands, key=lambda x: (int(x[0]), x[1]))
    for h in sorted_hands:
        print(h)

    rank = []
    bids = []
    for i, dat in enumerate(sorted_hands):
        rank.append(i + 1)
        bids.append(dat[2])
    score = [r*b for r, b in zip(rank, bids)]

    print("ranks:", rank)
    print("bids:", bids)
    print("scores:", score)
    print("pt1 solution: ", sum(score))


def get_hand_type(hnd):
    htots = sorted(
        list(filter(lambda x: x != 0, np.bincount(hnd))), reverse=True)
    f = htots[0]
    if f == 5:
        return HT.FIVEKIND
    if f == 4:
        return HT.QUADS
    if f == 3:
        if htots[1] == 2:
            return HT.HOUSE
        return HT.TRIPS
    if f == 2:
        if htots[1] == 2:
            return HT.TWOPAIR
        return HT.PAIR
    return HT.HIGHCARD


def check_for_duplicates(data):
    hds, _ = zip(*data)
    seen = []
    for h in hds:
        if not h in seen:
            seen.append(h)
        else:
            raise Exception("no code for handling duplicates")
    print("stlen: ", len(hds), "   endlen: ", len(seen))


def re_unpack_data(lines):
    handsbids = []
    for line in lines:
        (strhand, bid) = line.split()
        hand = [card_as_num(c) for c in strhand]  # NOSORT, BAD!
        handsbids.append((hand, int(bid)))
    return handsbids


def card_as_num(c):
    try:
        return int(c)
    except:
        return int(CARDCONVERT[c])


def read_data():
    """ read input data; split by line breaks """
    with open(PATH_INPUT_DATA, 'r', encoding="utf-8") as f:
        lines = f.readlines()
    return lines


# run code
if __name__ == "__main__":
    main()
