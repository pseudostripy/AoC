import re
import os
os.chdir('AllPuzzles/Puzzle1')

# static
wordnums = "zero,one,two,three,four,five,six,seven,eight,nine".split(sep=',')
# path_input_data = 'Data/puzzle1_pt2_example.txt'
path_input_data = 'Data/puzzle1_input.txt'

print(wordnums)

def main():
    """Puzzle01: Decode lines into keys and sum each line key

    digits are in numerical or word-equiv format.
    'key', i.e. two_digit_number is formed by concatenation of first 
    and last digits into single number.
    if just 1 digit in str, this is both first and last digit.
    """
    
    # read input data
    with open(path_input_data,'r') as f:
        lines = f.readlines()

    # build regex
    wn_for_regex = '|'.join(wordnums)
    capdigit = r"\d|" + wn_for_regex
    pattern_str = f"(?=({capdigit}))"  # "include overlapping matches". lookahead for a defined match and capture it where we stand.
    repat = re.compile(pattern_str)

    # run code
    two_digit_numbers = []
    for line in lines:
        matches = repat.findall(line)      # find all single-digits
        two_digit_numbers.append(allmatches_to_key(matches))

    print(f"line_keys = {two_digit_numbers}")
    print(f"Number of keys: {len(two_digit_numbers)}")
    print(f"puzzle result: {sum(two_digit_numbers)}")

def allmatches_to_key(ms):
    if not ms: raise Exception("String has no digits; cannot create key")
    dfirst = as_str_digit(ms[0])
    dlast = as_str_digit(ms[-1])
    return int(dfirst + dlast) # make key

def as_str_digit(dstr):
    """convert 'one','two' etc. to '1','2' where appropriate"""
    if dstr.isnumeric():
        return dstr
    return str(wordnums.index(dstr)) # should always exist; throws value_err otherwise.

# run code
if __name__ == "__main__":
    main()