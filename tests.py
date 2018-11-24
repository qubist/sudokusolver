import unittest
from map import *

class TestMapMethods(unittest.TestCase):

    def test_loadMap(self):
        m2 = Map("map6.txt")
        m2.loadMap()
        self.assertEqual(f"{m2}",
'''
7.9 | 1.2 | .3.
.68 | ..5 | 2..
..5 | ... | 6..
----+-----+----
.2. | 694 | 3..
... | 2.1 | ...
..1 | 573 | .4.
----+-----+----
..6 | ... | 1..
..2 | 4.. | 78.
.7. | 829 | 4.5
''')

    def test_getRow(self):
        m2 = Map("map6.txt")
        m2.loadMap()
        self.assertEqual(m2.getRow(2),['.', '.', '5', '.', '.', '.', '6', '.', '.'])
        self.assertEqual(m2.getRow(0),['7', '.', '9', '1', '.', '2', '.', '3', '.'])
        self.assertRaises(OffMapException, lambda: m2.getRow(9))

    def test_getColumn(self):
        m2 = Map("map6.txt")
        m2.loadMap()
        self.assertEqual(m2.getColumn(2),['9', '8', '5', '.', '.', '1', '6', '2', '.'])
        self.assertEqual(m2.getColumn(0),['7', '.', '.', '.', '.', '.', '.', '.', '.'])
        self.assertRaises(OffMapException, lambda: m2.getColumn(9))

    def test_getBox(self):
        m2 = Map("map6.txt")
        m2.loadMap()
        self.assertEqual(m2.getBox(1),['1', '.', '2', '.', '.', '5', '.', '.', '.'])
        self.assertEqual(m2.getBox(0),['7', '.', '9', '.', '6', '8', '.', '.', '5'])
        self.assertEqual(m2.getBox(4),['6', '9', '4', '2', '.', '1', '5', '7', '3'])
        self.assertEqual(m2.getBox(8),['1', '.', '.', '7', '8', '.', '4', '.', '5'])
        self.assertRaises(OffMapException, lambda: m2.getBox(9))

    def test_prepare(self):
        m2 = Map("map6.txt")
        m2.loadMap()
        m2.prepare()
        #print(m2.tiles[1])
        #print(m2)
        pass

    def test_isSure(self):
        m2 = Map("map6.txt")
        m2.loadMap()
        m2.prepare()
        self.assertEqual(m2.isSure(m2.getTile(0,0)), True)
        self.assertEqual(m2.isSure(m2.getTile(1,0)), False)
if __name__ == '__main__':
    unittest.main()
