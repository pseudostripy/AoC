import os
import re
os.chdir('AllPuzzles/Puzzle5')
PATH_INPUT_DATA = 'input.txt'
# PATH_INPUT_DATA = 'sample.txt'
NEWLINE = "\n"
DOUBLE_NEWLINE = NEWLINE + NEWLINE
LARGENUM = 100000000000
DOPRINT = True


def main():
    # unpack data
    lines = read_data()
    seedpairs = re_unpack_seeds(lines[0])
    maps = "".join(lines[1:]).split(sep=DOUBLE_NEWLINE)

    # create chained lookups
    almanac = []
    for mp in maps:
        almanac.append(forwards_map_partition_filled(mp))

    seedparts = []
    for (st, sz) in seedpairs:
        seedparts.append((st, st+(sz-1)))  # cvt to partition incl

    if DOPRINT:
        print(seedparts)

    next_input_intervals = seedparts
    for dep, mp in enumerate(almanac):
        bds, vals = zip(*mp)
        if DOPRINT:
            print(f"bds{dep}", bds)
            print(f"vals{dep}", vals)

        sti, sto = get_input_intervals(mp, next_input_intervals, dep)
        if DOPRINT:
            print(f"sti{dep}", sti)
            print(f"sto{dep}", sto)
        next_input_intervals = sto  # prep next in chain
        print("")
        debug = 1

    # ... maybe..
    answer = min([x[0] for x in next_input_intervals])
    print("sol2 answer: ", answer)


def get_input_intervals(mp, stintervals, depth):
    fixin = []  # fixed input intervals
    fixout = []
    bds, vals = zip(*mp)

    for (lhs, rhs) in stintervals:
        # first index higher than lowerbd
        b1 = next(i for i, b in enumerate(bds) if b > lhs) - 1
        b2 = next(i for i, b in enumerate(bds) if b > rhs)
        lindlhs = b1
        uindlhs = b1 + 1  # index of nearest (higher) bds to LHS
        lindrhs = b2 - 1  # index of nearest (lower) bds to RHS
        uindrhs = b2

        if (uindrhs - lindlhs == 1):
            # lies within one boundary set
            oplhs = vals[lindlhs] + (lhs - bds[lindlhs])
            oprhs = vals[lindrhs] + (rhs - bds[lindrhs])
            op = (oplhs, oprhs)
            if (lindlhs != lindrhs):
                raise Exception("bug here")
            fixin.append((lhs, rhs))
            fixout.append(op)
            test = fixout[-1]
            if test[1] < 0:
                pass
        else:
            # new trimmed st interval
            newrhs = bds[uindlhs] - 1
            fixin.append((lhs, newrhs))  # new first interval
            oplhs = vals[lindlhs] + (lhs - bds[lindlhs])
            oprhs = vals[lindlhs] + (newrhs - bds[lindlhs])
            newop = (oplhs, oprhs)
            fixout.append(newop)

            # add internal intervals
            for i in range(uindlhs, lindrhs):  # rng-incl
                newlhs = bds[i]
                newrhs = bds[i + 1] - 1
                fixin.append((newlhs, newrhs))
                oplhs = vals[i]
                oprhs = oplhs + (newrhs - newlhs)
                newop = (oplhs, oprhs)
                fixout.append(newop)

            # new trimmed end interval
            newlhs = bds[lindrhs]
            fixin.append((newlhs, rhs))
            oplhs = vals[lindrhs]
            oprhs = vals[lindrhs] + (rhs - bds[lindrhs])
            newop = (oplhs, oprhs)
            fixout.append(newop)
    return (fixin, fixout)


def forwards_map_partition_filled(mp):
    d = []
    sets = mp.strip().split(sep=NEWLINE)[1:]  # ignore name
    for strset in sets:
        d.append(to_intlist(strset.split()))

    # add missing "forwards partitions":
    ss1 = sorted(d, key=lambda x: x[1])
    sprev_end = ss1[0][1]
    spart = []
    if ss1[0][1] != 0:
        spart.append((0, 0))  # partition_start, part_mapped_value
    for (d, s, sz) in ss1:
        if (s != sprev_end):
            # fill partition with identity
            spart.append((sprev_end, sprev_end))
        spart.append((s, d))    # append this data
        sprev_end = s + sz      # update next end
    spart.append((sprev_end, sprev_end))  # open-ended top partition
    spart.append((LARGENUM, LARGENUM))  # some high bound
    return spart


def to_intlist(strlist):
    return list(map(int, strlist))


def re_unpack_seeds(line):
    pattern = r"\d+"
    seedpairs = re.findall(pattern, line.removeprefix("seeds: "))
    sts = to_intlist(seedpairs[0::2])
    szs = to_intlist(seedpairs[1::2])
    return zip(sts, szs)


def read_data():
    """ read input data; split by line breaks """
    with open(PATH_INPUT_DATA, 'r', encoding="utf-8") as f:
        lines = f.readlines()
    return lines


# run code
if __name__ == "__main__":
    main()
