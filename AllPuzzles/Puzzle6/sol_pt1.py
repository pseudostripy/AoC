import os
import re
import math
import numpy as np
os.chdir('AllPuzzles/Puzzle6')
PATH_INPUT_DATA = 'input.txt'


def main():
    # unpack data
    lines = read_data()
    data = re_unpack_data(lines)

    nsols = []
    for T, D in data:
        discrim = math.sqrt(T**2 - 4*D)
        xmin = 0.5*(T - discrim)
        xmax = 0.5*(T + discrim)
        x0 = int(xmin + 1 if xmin.is_integer() else math.ceil(xmin))
        xf = int(xmax - 1 if xmax.is_integer() else math.floor(xmax))
        print(x0, " <= x <= ", xf)
        nsols.append(xf - x0 + 1)

    print(nsols)
    print("solution pt1 = ", np.prod(nsols))


def to_intlist(strlist):
    return list(map(int, strlist))


def re_unpack_data(lines):
    pattern = r"\d+"
    game_time = to_intlist(re.findall(
        pattern, lines[0].removeprefix("Time: ")))
    dist_rec = to_intlist(re.findall(
        pattern, lines[1].removeprefix("Distance: ")))
    return zip(game_time, dist_rec)


def read_data():
    """ read input data; split by line breaks """
    with open(PATH_INPUT_DATA, 'r', encoding="utf-8") as f:
        lines = f.readlines()
    return lines


# run code
if __name__ == "__main__":
    main()
