import os
import re
os.chdir('AllPuzzles/Puzzle5')
PATH_INPUT_DATA = 'input.txt'
NEWLINE = "\n"
DOUBLE_NEWLINE = NEWLINE + NEWLINE


def main():
    # unpack data
    lines = read_data()
    seeds = re_unpack_seeds(lines[0])
    maps = "".join(lines[1:]).split(sep=DOUBLE_NEWLINE)

    # create chained lookups
    almanac = []
    for mp in maps:
        dmap = map_to_dict(mp)
        almanac.append(dmap)

    # lookup values
    seedloc = [almanac_lookup(almanac, s) for s in seeds]
    print("seed locations: ", seedloc)
    print("solution_pt1: ", min(seedloc))


def almanac_lookup(al, v):
    for d in al:
        v = mapped_or_self(d, v)
    return v


def mapped_or_self(dbds, k):
    for (vlb, klb, sz) in dbds:
        if k >= klb and k < (klb + sz):
            i = (k - klb)
            return vlb + i
    return k


def map_to_dict(mp):
    d = []
    sets = mp.strip().split(sep=NEWLINE)[1:]  # ignore name
    for strset in sets:
        d.append(to_intlist(strset.split()))
    return d


def to_intlist(strlist):
    return list(map(int, strlist))


def re_unpack_seeds(line):
    pattern = r"\d+"
    return to_intlist(re.findall(pattern, line.removeprefix("seeds: ")))


def read_data():
    """ read input data; split by line breaks """
    with open(PATH_INPUT_DATA, 'r', encoding="utf-8") as f:
        lines = f.readlines()
    return lines


# run code
if __name__ == "__main__":
    main()
