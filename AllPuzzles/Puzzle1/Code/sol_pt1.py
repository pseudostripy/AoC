import re
import os
os.chdir('AllPuzzles/Puzzle1')

with open('Data/puzzle1_input.txt','r') as f:
    lines = f.readlines()

two_digit_numbers = []
for line in lines:
    m = re.findall(pattern=r"\d", string=line)      # find all single-digits
    if not m: raise Exception("String has no digits; cannot create key")
    two_digit_numbers.append(int(m[0] + m[-1]))           # if str has only 1 digit, this still works

print(f"line_keys = {two_digit_numbers}")
print(f"puzzle result: {sum(two_digit_numbers)}")