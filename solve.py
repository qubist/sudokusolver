import sys
from board import *

# takes string filename and returns solved
def solve(file):
    b = Board(file)
    b.loadBoard()
    b.prepare()
    b.reduce()
    return b

if __name__ == "__main__":
   print(solve(sys.argv[1]))
