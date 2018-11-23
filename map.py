class OffMapException(Exception):
    pass

class Map:
    def __init__(self, filename):
        self.filename = filename
        self.tiles = [["\0" for x in range(9)] for y in range(9)]

    def loadMap(self):
        try:
            file = open(self.filename)
            y = 0      # y is different than lineno as some lines may be comments
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

    # returns a list of all items in a given row, 0 through 8
    # starting from the top
    def getRow(self, row):
        if row > 8:
            raise OffMapException
        return self.tiles[row]

    # returns a list of all items in a given column, 0 through 8
    # starting from the left
    def getColumn(self, column):
        if column > 8:
            raise OffMapException
        out = []
        for x in self.tiles:
            out += x[column]
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
            raise OffMapException
        out = []
        xStart = x = boxID%3*3
        y = int(boxID/3)*3
        yEnd = y + 3
        xEnd = x + 3
        while y < yEnd:
            while x < xEnd:
                out += self.tiles[y][x]
                x += 1
            y+= 1
            x = xStart
        return out

    # print out a map pretty
    def __str__(self):
        out = "\n"
        h = 1 # horizontal lines
        for x in self.tiles:
            v = 1 # vertical lines
            for y in x:
                out += f"{y}"
                if v%3 == 0 and v <= 8:
                    out += " | "
                v += 1
            if h%3 == 0 and h <= 8:
                out += "\n----+-----+----"
            h += 1
            out += "\n"
        return out


if __name__ == '__main__':
    m2 = Map("map6.txt")
    m2.loadMap()
    print(m2)
    print(m2.getRow(2))
    print(m2.getColumn(2))
    print(m2.getColumn(0))
