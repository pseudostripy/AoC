import re
import os
from enum import Enum
os.chdir('AllPuzzles/Puzzle2')
path_input_data = 'input.txt'

class Game:
    def __init__(self, gameid):
        self.gameid = gameid    # gameid
        self.sets = []  # preallocate list for set results

    def add_set(self,set):
        self.sets.append(set)
        return self
    
    def is_valid_game(self):
        return all([s.is_valid_set() for s in self.sets])
    
    def get_game_power(self):
        mult_total = 1
        for col in GameSet.cols:
            minreq = max(x.get_col_val(col) for x in self.sets)
            mult_total *= minreq
        return mult_total

class GameSet:
    # static
    cols = ["red", "green", "blue"]

    def __init__(self, setid):
        self.setid = id # gameid
        self.res = [0 for c in GameSet.cols] # preallocate total colour count

    def add_col(self, colstr, amt):
        self.res[GameSet.cols.index(colstr)] += amt
        return self

    def get_col_val(self, strcol):
        return self.res[GameSet.cols.index(strcol)]

    def is_valid_set(self):
        # pt1 rule:
        return (self.red <= 12 and self.green <= 13 and self.blue <= 14)

    # shorthand...
    @property
    def red(self):
        return self.res[GameSet.cols.index("red")]
    @property
    def green(self):
        return self.res[GameSet.cols.index("green")]
    @property
    def blue(self):
        return self.res[GameSet.cols.index("blue")]

def main():
    # read input data
    with open(path_input_data,'r') as f:
        lines = f.readlines()

    games = [] # all game results

    for line in lines:
        # instantiate new game obj
        gameid = (int)(re.match(r"Game (?P<id>\d+)",line)["id"])
        game = Game(gameid) 

        # get game result str
        colid = line.index(':')
        resultstr = line[colid+1:].strip()

        setstrs = [s.strip() for s in resultstr.split(';')] # list of single set results
        for i,strset in enumerate(setstrs):
            gset = GameSet(i)       # create new set
            for (amt,style) in re.findall(r"(?P<amt>\d+)\s(\w+)",strset):
                gset.add_col(style,int(amt))   # add parsed results
            game.add_set(gset)      # record complete set
        games.append(game)          # record complete game
    
    total = sum(g.get_game_power() for g in games)
    print(total)

# run code
if __name__ == "__main__":
    main()

