import os
import re
import math
import numpy as np
import pandas as pd
from enum import IntEnum, auto
os.chdir('AllPuzzles/Puzzle8')
PATH_INPUT_DATA = 'input.txt'
LARGENUM = 999999


def main():
    # unpack data
    lines = read_data()
    (instr, d) = re_unpack_data(lines)

    print(instr)

    nextkey = "AAA"
    crashctr = 0
    cycles = 0
    steps = 0
    N = len(instr)
    while True:
        lr = instr[steps]
        nextkey = d[nextkey][lr]
        if nextkey == "ZZZ":
            break
        crashctr += 1  # avoid inf loop
        if crashctr > LARGENUM:
            raise Exception("Increase if you think it needs more")
        steps += 1
        if steps == N:
            cycles += 1
            steps = 0

    total_steps = cycles*N + steps + 1
    print(N)
    print(total_steps)


def re_unpack_data(lines):
    LRchain = lines[0].strip()
    lrchain_out = [0 if c == "L" else 1 for c in LRchain]

    dic = {}
    repat = re.compile(r"(?P<key>\w+) = \((?P<L>\w+), (?P<R>\w+)\)")
    for line in lines[2:]:
        # unpack line:
        m = repat.match(line)
        k = m.group("key")
        L = m.group("L")
        R = m.group("R")
        dic[k] = (L, R)

    return (lrchain_out, dic)


def read_data():
    """ read input data; split by line breaks """
    with open(PATH_INPUT_DATA, 'r', encoding="utf-8") as f:
        lines = f.readlines()
    return lines


# run code
if __name__ == "__main__":
    main()
