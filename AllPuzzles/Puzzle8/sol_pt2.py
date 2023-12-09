import os
import re
import math
import numpy as np
import pandas as pd
from enum import IntEnum, auto
os.chdir('AllPuzzles/Puzzle8')
PATH_INPUT_DATA = 'input.txt'
LARGENUM = 99999999


def main():
    # unpack data
    lines = read_data()
    (instr, d) = re_unpack_data(lines)

    print(instr)

    nextkeys = [k for k in d.keys() if k.endswith("A")]
    # nextkeys = ['HVA', 'LBA', 'FXA', 'GHA', 'PSA', 'AAA']  # debug speed

    first_round = []
    print(nextkeys)
    for nk in nextkeys:
        first_round.append(find_cycle(instr, d, nk))

    for (vals, cycst, cyclen) in first_round:
        print(cycst, cyclen)

    # this was a useful block to understand indices of repetition
    # second_round = []
    # for rd1i, (vals, cycst, cyclen) in enumerate(first_round):
    #     zvals = [i for i, v in enumerate(vals[cycst:]) if v[0][-1] == "Z"]
    #     second_round.append(zvals)
    #     print(f"Rd{rd1i}, numz = {len(zvals)}")
    #     print(zvals, vals[zvals[0]+cycst])

    # so I need a number which is factorizable by:
    satels = [cyclen for (_, _, cyclen) in first_round]  # satisfiabiity
    print(satels)
    ans = math.lcm(*satels)
    print("lowest_common_multiple:", ans)

    # crashctr = 0
    # cycles = 0
    # steps = 0
    # N = len(instr)
    # while True:
    #     lr = instr[steps]
    #     nextkeys = [d[nk][lr] for nk in nextkeys]
    #     if all((nk[-1] == "Z") for nk in nextkeys):
    #         break  # exit condition
    #     crashctr += 1  # avoid inf loop
    #     if crashctr > LARGENUM:
    #         raise Exception("Increase if you think it needs more")
    #     steps += 1
    #     if steps == N:
    #         cycles += 1
    #         steps = 0

    # total_steps = cycles*N + steps + 1
    # print(N)
    # print(total_steps)


def find_cycle(instr, d, st):
    cyclic_set = []

    crashctr = 0
    cycles = 0
    steps = 0
    N = len(instr)
    nk = st  # nextkey
    while True:
        # check for cycle
        node = (nk, steps)
        if node in cyclic_set:
            print("Found a cycle!")
            break
        cyclic_set.append((nk, steps))

        # get next turn
        lr = instr[steps]
        nk = d[nk][lr]

        # incr ctrs
        crashctr += 1  # avoid inf loop
        if crashctr > LARGENUM:
            raise Exception("Increase if you think it needs more")
        steps += 1
        if steps == N:
            cycles += 1
            steps = 0

    cycle_st = cyclic_set.index(node)
    cyclen = len(cyclic_set) - cycle_st
    return cyclic_set, cycle_st, cyclen


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
