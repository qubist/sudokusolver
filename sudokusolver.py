class OffBoardException(Exception):
    pass

class Board:
    def __init__(self, filename):
        self.filename = filename
        self.tiles = [["\0" for x in range(9)] for y in range(9)]

    def loadBoard(self):
        try:
            file = open(self.filename)
            y = 0
            for line in file:
                if (y >= 9):
                    parts = line.split()

                else:
                    if (len(line) < 10):
                        print(f"Line {y} of map is malformed")
                        exit(1)
                    for x in range(9):
                        self.tiles[y][x] = line[x]#, x, y
                y += 1
            file.close()
        except:
            print(f"Could not load map file {self.filename}")
            exit(1)

    # gets tile
    def getTile(self, x, y): return self.tiles[y][x]

    # sets a tile
    def setTile(self, x, y, value): self.tiles[y][x] = value

    # sets a tile by box ID and index
    def setTileByBoxIDAndIndex(self, boxID, index, value):
        x = boxID%3*3
        y = int(boxID/3)*3

        yi = int(index/3)
        xi = index%3

        x += xi
        y += yi

        self.setTile(x,y,value)

    # returns a list of all items in a given row, 0 through 8
    # starting from the top
    def getRow(self, row):
        if row > 8:
            raise OffBoardException
        return self.tiles[row]

    # returns a list of all items in a given column, 0 through 8
    # starting from the left
    def getColumn(self, x):
        if x > 8:
            raise OffBoardException
        out = []
        for y in self.tiles:
            out += [y[x]]
        return out

    # Gets a list of all the items in a given box. Boxes like so:
    # 0 | 1 | 2
    #---+---+---
    # 3 | 4 | 5
    #---+---+---
    # 6 | 7 | 8
    def getBox(self,boxID):
        # check if boxID is valid
        if boxID > 8:
            raise OffBoardException
        out = []
        xStart = x = boxID%3*3
        y = int(boxID/3)*3
        yEnd = y + 3
        xEnd = x + 3
        while y < yEnd:
            while x < xEnd:
                out += [self.getTile(x,y)]
                x += 1
            y+= 1
            x = xStart
        return out

    def prepare(self):
        for y in self.tiles:
            x = 0
            while x < 9:
                if y[x] == ".": y[x] = "123456789"
                x += 1

    # returns whether the tile is "sure" (the tile has only one value)
    def isSure(self,tile):
        return len(tile)==1

    def calculateBoxID(self, x,y):
        return int(y/3)*3 + int(x/3)

    # If the tile isn't sure, removes numbers from the tile
    # which we see as sure in the current tile's column, row, or
    # box. Returns number of numbers removed.
    def removeImpossibles(self, x, y):
        tile = self.getTile(x,y)

        ## Discovery by number elimination ###
        originalLength = len(tile)
        # don't do anything and return 0 if tile is sure
        if self.isSure(tile):
            return 0
        # add numbers we see to a big list
        c = self.getColumn(x)
        r = self.getRow(y)
        b = self.getBox(self.calculateBoxID(x,y))
        l = c + r + b
        # strip unsure tiles from the list
        l = [possib for possib in l if len(possib) == 1]
        # walk through the list and remove numbers we find from
        # current tile
        for possib in l:
            tile = tile.replace(possib,"")
        self.setTile(x,y, tile)

    def discoverByUniqueIn(self, x,y):
        ### Discovery by exclusion ####
        ## Box
        changeCount = 0
        if x%3 == 2 and y%3 == 2: # only do this once per box
            boxID = self.calculateBoxID(x,y)
            box = self.getBox(boxID)
            # make a dictionary of the possible values and how many
            # of them we see in a given box
            counts = {
            "1" : 0,
            "2" : 0,
            "3" : 0,
            "4" : 0,
            "5" : 0,
            "6" : 0,
            "7" : 0,
            "8" : 0,
            "9" : 0
            }
            # walk all the possibilities in the box and tally them up
            # in the dictionary
            for tile in box:
                for possibility in list(tile):
                    counts[possibility] += 1
            # walk back through the possibilities and when finding one
            # which is unique (tallied only once ^), we know it's sure
            for index in range(9):
                for possibility in list(box[index]):
                    if counts[possibility] == 1:
                        self.setTileByBoxIDAndIndex(boxID,index,possibility)

        ## Row
        if x == 8: # only do this once per row (at the end of each row)
            row = self.getRow(y)
            counts = {"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"9":0}
            for tile in row:
                for possibility in list(tile):
                    counts[possibility] += 1
            # walk back through the possibilities and when finding one
            # which is unique, we know it's sure
            for spot in range(9): # (spot because we wanna be careful with x)
                for possibility in list(row[spot]):
                    if counts[possibility] == 1:
                        self.setTile(spot,y,possibility)

        ## Column
        if y == 8: # only do this once per column (at the bottom of each column)
            column = self.getColumn(x)
            counts = {"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"9":0}
            for tile in column:
                for possibility in list(tile):
                    counts[possibility] += 1
            # walk back through the possibilities and when finding one
            # which is unique, we know it's sure
            for spot in range(9):
                for possibility in list(column[spot]):
                    if counts[possibility] == 1:
                        self.setTile(x,spot,possibility)

    def solve(self, debug=0):
        after = "something"; before = "something else" # to start
        while after != before:
            before = f"{self}"
            for y in range(9):
                for x in range(9):
                    self.removeImpossibles(x,y)
            if debug:
                print("reduce by remove impossibles:")
                after = f"{self}"
                if before != after:
                    print(self)
                else:
                    print("no change")
            for y in range(9):
                for x in range(9):
                    self.discoverByUniqueIn(x,y)
            after = f"{self}"
            if debug:
                print("reduce by discover unique:")
                if before!=after:
                    print(after)
                else:
                    print("no change")
            print(after)
            # import time; time.sleep(.15) # option for looking cool

    # print out a map pretty
    def __str__(self):
        out = "\n"
        h = 1 # horizontal lines
        for x in self.tiles:
            v = 1 # vertical lines
            for y in x:
                #if len(y) != 1: out += " ."
                #else: out += f" {y}"
                out += f" {y}" # Turn this on instead of the two lines above it to see all possibilities of unsure tiles instead of a "."!
                if v%3 == 0 and v <= 8:
                    out += " |"
                v += 1
            if h%3 == 0 and h <= 8:
                out += "\n ------+-------+------"
            h += 1
            out += "\n"
        return out
