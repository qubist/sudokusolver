import unittest
from board import *

class TestBoardMethods(unittest.TestCase):

    def test_loadBoard(self):
        m2 = Board()
        m2.loadBoard("board6.txt")
        self.assertEqual(f"{m2}",
'''
 7 . 9 | 1 . 2 | . 3 .
 . 6 8 | . . 5 | 2 . .
 . . 5 | . . . | 6 . .
 ------+-------+------
 . 2 . | 6 9 4 | 3 . .
 . . . | 2 . 1 | . . .
 . . 1 | 5 7 3 | . 4 .
 ------+-------+------
 . . 6 | . . . | 1 . .
 . . 2 | 4 . . | 7 8 .
 . 7 . | 8 2 9 | 4 . 5
''')

    def test_getTile(self):
        b = Board()
        b.loadBoard("board6.txt")
        self.assertEqual(b.getTile(0,0), "7")
        self.assertEqual(b.getTile(0,1), ".")
        self.assertEqual(b.getTile(5,5), "3")
        self.assertEqual(b.getTile(2,8), ".")
        self.assertEqual(b.getTile(5,8), "9")


    def test_setTile(self):
        b = Board()
        b.loadBoard("board6.txt")
        b.setTile(0,5,"8")
        self.assertEqual(b.getTile(0,5), "8")
        b.setTile(0,5,"4")
        self.assertEqual(b.getTile(0,5), "4")
        b.setTile(8,8,"aligator")
        self.assertEqual(b.getTile(8,8), "aligator")


    def test_setTileByBoxIDAndIndex(self):
        b = Board()
        b.loadBoard("board6.txt")
        b.setTileByBoxIDAndIndex(2,5,"8")
        self.assertEqual(b.getTile(8,1), "8")

    def test_getRow(self):
        m2 = Board()
        m2.loadBoard("board6.txt")
        self.assertEqual(m2.getRow(2),['.', '.', '5', '.', '.', '.', '6', '.', '.'])
        self.assertEqual(m2.getRow(0),['7', '.', '9', '1', '.', '2', '.', '3', '.'])
        self.assertRaises(OffBoardException, lambda: m2.getRow(9))
        g = Board()
        g.loadBoard("board6.txt")
        g.prepare()
        self.assertEqual(g.getRow(8), ['123456789', '7', '123456789', '8', '2', '9', '4', '123456789', '5'])

    def test_getColumn(self):
        m2 = Board()
        m2.loadBoard("board6.txt")
        self.assertEqual(m2.getColumn(2),['9', '8', '5', '.', '.', '1', '6', '2', '.'])
        self.assertEqual(m2.getColumn(0),['7', '.', '.', '.', '.', '.', '.', '.', '.'])
        self.assertRaises(OffBoardException, lambda: m2.getColumn(9))
        g = Board()
        g.loadBoard("board6.txt")
        g.prepare()
        self.assertEqual(g.getColumn(2), ['9', '8', '5', '123456789', '123456789', '1', '6', '2', '123456789'])


    def test_getBox(self):
        m2 = Board()
        m2.loadBoard("board6.txt")
        self.assertEqual(m2.getBox(1),['1', '.', '2', '.', '.', '5', '.', '.', '.'])
        self.assertEqual(m2.getBox(0),['7', '.', '9', '.', '6', '8', '.', '.', '5'])
        self.assertEqual(m2.getBox(4),['6', '9', '4', '2', '.', '1', '5', '7', '3'])
        self.assertEqual(m2.getBox(8),['1', '.', '.', '7', '8', '.', '4', '.', '5'])
        self.assertRaises(OffBoardException, lambda: m2.getBox(9))
        g = Board()
        g.loadBoard("board6.txt")
        g.prepare()
        self.assertEqual(g.getBox(2), ['123456789', '3', '123456789', '2', '123456789', '123456789', '6', '123456789', '123456789'])

    def test_prepare(self):
        m2 = Board()
        m2.loadBoard("board6.txt")
        m2.prepare()
        #print(m2.tiles[1])
        #print(m2)
        pass

    def test_isSure(self):
        m2 = Board()
        m2.loadBoard("board6.txt")
        m2.prepare()
        self.assertEqual(m2.isSure(m2.getTile(0,0)), True)
        self.assertEqual(m2.isSure(m2.getTile(1,0)), False)

    def test_calculateBoxID(self):
        m = Board()
        self.assertEqual(m.calculateBoxID(1,2), 0)
        self.assertEqual(m.calculateBoxID(0,0), 0)
        self.assertEqual(m.calculateBoxID(7,8), 8)
        self.assertEqual(m.calculateBoxID(4,5), 4)

    def test_removeImpossibles(self):
        m2 = Board()
        m2.loadBoard("board6.txt")
        m2.prepare()
        # Nothing should be removed from a sure tile
        m2.removeImpossibles(0,0)
        self.assertEqual(m2.getTile(0,0), "7")
        # Impossibles should be removed
        m2.removeImpossibles(1,0)
        self.assertEqual(m2.getTile(1,0), "4")

    # def test_removeAll(self):
    #     b = Board()
    #     b.loadBoard("board6.txt")
    #     b.prepare()
    #     b.removeAll()
    def test_reduceHard(self):
        b = Board()
        b.loadBoard("board103.txt")
        b.prepare()
        b.reduce(False)
        self.assertEqual(f"{b}",
'''
 4 7 1 | 5 6 9 | 3 8 2
 9 5 2 | 3 4 8 | 1 6 7
 3 6 8 | 2 1 7 | 4 9 5
 ------+-------+------
 8 9 5 | 1 3 6 | 7 2 4
 2 4 6 | 8 7 5 | 9 3 1
 7 1 3 | 9 2 4 | 8 5 6
 ------+-------+------
 6 2 4 | 7 8 3 | 5 1 9
 5 8 7 | 6 9 1 | 2 4 3
 1 3 9 | 4 5 2 | 6 7 8
'''
)

    def test_reduceZ(self):
        b = Board()
        b.loadBoard("board70.txt")
        b.prepare()
        b.reduce(False)

    def test_isLegalList(self):
        b = Board()
        self.assertTrue(b.isLegalList(['.', '.', '5', '.', '.', '.', '6', '.', '.']))
        self.assertFalse(b.isLegalList(['5', '.', '5', '.', '.', '.', '6', '.', '.']))
        self.assertTrue(b.isLegalList(['123', '.', '5', '.', '.', '.', '6', '.', '.']))

    def test_isLegalBoard(self):
        b = Board()
        b.loadBoard("board70.txt")
        b.prepare()
        self.assertTrue(b.isLegalBoard())
        b.reduce(False)
        self.assertTrue(b.isLegalBoard())
        b.setTile(0,0,"1")
        b.setTile(0,1,"1")
        self.assertFalse(b.isLegalBoard())

    def test_randomBoard(self):
        b = Board()
        b.randomBoard(30)
        self.assertTrue(b.isLegalBoard())


    def test_make(self):
        b = Board()
        # may take a while to run!
        b.make(30)
        self.assertTrue(b.isLegalBoard())
        print(b)

if __name__ == '__main__':
    unittest.main()
